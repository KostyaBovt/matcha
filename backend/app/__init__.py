from flask import Flask
from flask import jsonify, request
from shared import Mailer
from shared import Hasher
from shared import vdf

app = Flask(__name__)
app.config.from_pyfile('../config/app_config.py')

@app.route("/")
def hello():
    return jsonify({'success': 'true'})
    # return "<h1 style=''>Hello There! I am Flask Application</h1>"

@app.route("/mail")
def test_mail():
    mailer = Mailer()
    hasher = Hasher()
    mailer.send_register_confirm("recepient_name", "kostya.bovt@gmail.com", hasher.hash_string("kostya.bovt@gmail.com"), hasher.generate_hash(32))
    return "email is send!"

@app.route("/register", methods=['POST'])
def register():
    success = 0
    mailer = Mailer()
    hasher = Hasher()

    email = request.json['email']
    password = request.json['password']
    password = hasher.hash_string(password)

    db = shared.database()
    sql = "select * from users where email='{:s}'".format(email)
    db.request(sql)
    if db.getRowCount():
        return jsonify({'success': 0, 'method': 'register'})

    sql = "insert into users (email, password, confirmed) values ('{:s}', '{:s}', 0) returning id".format(email, password)
    db.request(sql)
    user_id = db.getLastRowId()


    email_hash = hasher.hash_string(email)
    confirm_hash = hasher.generate_hash(32)
    sql = "insert into confirm (user_id, email_hash, confirm_hash) values ({:d},'{:s}', '{:s}') returning id".format(user_id, email_hash, confirm_hash)
    db.request(sql)

    if not db.getError() and db.getRowCount() == 1:
        success = 1

    mailer.send_register_confirm(email, email, email_hash, confirm_hash)
        
    return jsonify({'success': success, 'method': 'register'})


@app.route("/confirm/<string:email_hash>/<string:confirm_hash>")
def confirm(email_hash, confirm_hash):

    db = shared.database()
    success = 0

    sql = "select * from confirm where email_hash='{:s}' and confirm_hash='{:s}';".format(email_hash, confirm_hash)
    db.request(sql)

    if db.getRowCount():
        success = 1
        user_id = db.getResult()[0]['user_id']
        sql = "update users set confirmed={:d} where id={:d};".format(1, user_id)
        db.request(sql)        

    return jsonify({'success': success, 'method': 'confirm'})


@app.route("/forgot", methods=['POST'])
def forgot():

    success = 0
    email = request.json['email']

    db = shared.database()

    sql = "select * from users where email='{:s}';".format(email)
    db.request(sql)

    if db.getRowCount():
        mailer = Mailer()
        hasher = Hasher()
        user_id = db.getResult()[0]['id']
        email_hash = hasher.hash_string(email)
        reset_hash = hasher.generate_hash(32)

        sql = "select * from forgot where user_id='{:d}';".format(user_id)
        db.request(sql)

        if db.getRowCount():
            sql = "update forgot set reset_hash='{:s}' where user_id={:d};".format(reset_hash, user_id)
        else:
            sql = "insert into forgot (user_id, email_hash, reset_hash) values ({:d},'{:s}', '{:s}') returning id".format(user_id, email_hash, reset_hash)
        db.request(sql)
        if not db.getError() and db.getRowCount() == 1:
            success = 1
            mailer.send_reset_password(email, email, email_hash, reset_hash)

    return jsonify({'success': success, 'method': 'forgot'})


@app.route("/check_reset/<string:email_hash>/<string:reset_hash>")
def check_reset(email_hash, reset_hash):

    db = shared.database()
    success = 0

    sql = "select * from forgot where email_hash='{:s}' and reset_hash='{:s}';".format(email_hash, reset_hash)
    db.request(sql)

    if db.getRowCount():
        success = 1

    return jsonify({'success': success, 'method': 'check_reset'})

@app.route("/reset", methods=['POST'])
def reset():
    success = 0
    hasher = Hasher()

    email_hash = request.json['email_hash']
    reset_hash = request.json['reset_hash']
    password = request.json['password']
    password = hasher.hash_string(password)
    repeat_password = request.json['repeat_password']
    repeat_password = hasher.hash_string(repeat_password)

    if password != repeat_password:
        return jsonify({'success': 0, 'method': 'reset'})

    db = shared.database()
    sql = "select * from forgot where email_hash='{:s}' and reset_hash= '{:s}';".format(email_hash, reset_hash)
    db.request(sql)
    if not db.getRowCount():
        return jsonify({'success': 0, 'method': 'reset'})

    user_id = db.getResult()[0]['user_id']
    sql = "update users set password='{:s}' where id={:d}".format(password, user_id)
    db.request(sql)

    if not db.getError() and db.getRowCount() == 1:
        success = 1
        
    return jsonify({'success': success, 'method': 'reset'})