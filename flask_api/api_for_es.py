import requests
import json
from flask import Flask, jsonify, request, abort

from validator import validator

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
    validator(request.args)
    return jsonify(request.args)


if __name__ == '__main__':
    app.run(port=8000)