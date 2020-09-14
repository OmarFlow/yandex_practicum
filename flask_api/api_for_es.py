import requests
import json

from flask import Flask, jsonify, request, abort

from validator import validator
from utils import query_definition

DEFAULT_SIZE = 50
DEFAULT_SORT_BY = 'id'
DEFAULT_SORT = 'asc'
DEFAULT_PAGE = 1

app = Flask('movies_service')
app.debug = True

@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id: str) -> str:
    # Код, получающий данные из ES об одном фильме
    payload = json.dumps(
        {
            "query": {
                "term": {
                    "_id": movie_id
                }
            }
        }
    )
    query = {
        "term": {
            "_id": movie_id
        }
    }

    r= requests.get(
        url='http://127.0.0.1:9200/movies/_search',
        data=payload,
        headers={"Content-Type": "application/x-ndjson"}
    )
    print(r.json())
    # # abort(404)
    #
    # result = {'id': movie_id}
    return jsonify(
        [1,2,3]
    )


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list() -> str:
    data = request.args
    validation_result = validator(data)

    if validation_result:
        return jsonify(validation_result), 422

    payload = {
        "_source": ['id', 'title', 'imdb_rating'],
        "size": data.get('limit', DEFAULT_SIZE),
        "from": data.get('page', DEFAULT_PAGE),
        "sort": {data.get('sort', DEFAULT_SORT_BY): {"order": data.get('sort_order', DEFAULT_SORT)}},
        "query": query_definition(data.get('search'))
    }

    r = requests.get('http://localhost:9200/movies/_search', json=payload)
    result = []
    for f in json.loads(r.content)['hits']['hits']:
        result.append(f['_source'])

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=8000)