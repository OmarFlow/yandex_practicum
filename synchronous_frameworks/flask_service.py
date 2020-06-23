
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/client/info",  methods=['GET'])
def user_agent():

    response = jsonify(
        { 'user_agent': request.headers.get('User-Agent') }
    )

    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
