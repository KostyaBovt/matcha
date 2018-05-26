from flask import Flask
from flask import jsonify, request
from shared import Mailer
import hashlib


app = Flask(__name__)
app.config.from_pyfile('../config/app_config.py')

@app.route("/")
def hello():
    return jsonify({'success': 'true'})
    # return "<h1 style=''>Hello There! I am Flask Application</h1>"

@app.route("/mail")
def test_mail():
    mailer = Mailer()
    mailer.send_register_confirm("recepient_name", "kostya.bovt@gmail.com", 'email_hash', 'confirm_hash')
    return "email is send!"

@app.route("/register", methods=['POST'])
def register():
    success = 0

    email = request.json['email']
    password = request.json['password']
    password = hashlib.md5(password).hexdigest()

    db = shared.database()
    sql = "select * from users where email='{:s}'".format(email)
    db.request(sql)
    if db.getRowCount():
        return jsonify({'success': 0, 'method': 'register'})

    sql = "insert into users (email, password, confirmed) values ('{:s}', '{:s}', 0)".format(email, password)
    db.request(sql)

    if not db.getError() and db.getRowCount() == 1:
        success = 1
        
    return jsonify({'success': success, 'method': 'register', 'id': db.getLastRowId()})
