import sqlite3
import json
import requests

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()
url = 'http://localhost:9200/movies2/_bulk'

initial_data = cursor.execute("select id, imdb_rating, genre, title, plot, director, writers from movies").fetchall()

body = []
for data in initial_data:

    movie_id = data[0]

    writres_ids = data[6] or None
    if writres_ids:
        writres_ids = tuple((_id['id'] for _id in json.loads(writres_ids)))
        raw_writer_names = cursor.execute(f"select name from writers where id in {writres_ids}").fetchall()
        writer_names = ', '.join([name[0] for name in raw_writer_names])
        not_structured_writers = dict(
            cursor.execute(f"select id, name from writers where id in {writres_ids}").fetchall())
        writers = [{'id': writer_row, 'name': not_structured_writers[writer_row]} for writer_row in
                   not_structured_writers]
    else:
        writers = [{
            'id': None,
            'name': None
        }]
        writer_names = None

    raw_actor_names = cursor.execute(
        f"SELECT name from actors join movie_actors on actors.id = movie_actors.actor_id where movie_id='{movie_id}'"
    ).fetchall() or None
    if raw_actor_names:
        unpacked_actor_names = [name[0] for name in raw_actor_names]
        actor_names = ', '.join(unpacked_actor_names)
        not_structured_actors = {cursor.execute(f'select id from actors where name="{name}"').fetchone()[0]: name for
                                 name in unpacked_actor_names}
        actors = [{'id': actor_row, 'name': not_structured_actors[actor_row]} for actor_row in not_structured_actors]
    else:
        actor_names = None
        actors = [{
            'id': None,
            'name': None
        }]

    finally_data = {
        "id": data[0],
        "imdb_rating": None if data[1] == 'N/A' else float(data[1]),
        "genre": data[2],
        "title": data[3],
        "description": None if data[4] == 'N/A' else data[4],
        "director": None if data[5] == 'N/A' else data[5],
        "actors_names": actor_names,
        "writers_names": writer_names,
        "actors": actors,
        "writers": writers
    }

    action = {
        'index': {
            '_index': 'movies2'
        }
    }
    # exclude rows with the same title of movie
    # if any(row for row in set(body) if data[3] in row):
    #     continue

    body.append(json.dumps(action))
    body.append(json.dumps(finally_data))

payload = ""
for row in body:
    payload = payload + f"{row} \n"
data_for_elastic = payload.encode('utf-8')

r = requests.post(url, data=data_for_elastic, headers={"Content-Type": "application/x-ndjson"})
cursor.close()
