from flask import Flask
from flask import jsonify, request
import pprint
from application.shared import database
import psycopg2


app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({'success': 'true'})
    # return "<h1 style=''>Hello There! I am Flask Application</h1>"

@app.route("/register", methods=['POST'])
def register():
    # f = open('var_dump.txt', 'a')
    # f.write(str([request.headers, request.args, request.json, request.form, request.data]))
    # f.write('\n\n\n')
    # f.close()
    success = 'false'

    login = request.json['login']
    password = request.json['password']

    if (login == u'admin' and password == u'admin'):
        success = 'true'

    db = database()
    ret = db.getString()
    return jsonify({'success': success, 'method': 'register', 'db': ret})


if __name__ == "__main__":
    app.run(host='0.0.0.0')