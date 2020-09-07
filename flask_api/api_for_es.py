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
                "match": {
                    "field": "id",
                    "message": {
                        "query": movie_id,
                    }
                }
            }
        }
    )

    re = requests.get(
        url='http://127.0.0.1:9200/movies/_search',
        data=payload,
        headers={"Content-Type": "application/x-ndjson"}
    )
    print(re.json())
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
        "size": data['limit'] or DEFAULT_SIZE,
        "from": data['page'] or DEFAULT_PAGE,
        "sort": {data['sort'] or DEFAULT_SORT_BY: {"order": data.get('sort_order', DEFAULT_SORT)}},
        "query": query_definition(data.get('search'))
    }

    r = requests.get('http://localhost:9200/movies/_search', json=payload)
    print(r.content)



    return jsonify(
        {
            'qw': data.get('sort')
        }
    )


if __name__ == '__main__':
    app.run(debug=True, port=8000)