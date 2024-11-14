import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

from final2 import user_request_handle

@app.route('/sqlResponse', methods=['POST'])
def sqlResponse():
    user_input = flask.request.json['user_input']
    table_name = flask.request.json['table_name']
    schema_string = flask.request.json['schema_string']
   
    response = user_request_handle(schema_string, user_input, table_name)
    return response


if __name__ == '__main__':
    app.run(debug=True)
