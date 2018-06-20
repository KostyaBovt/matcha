from flask import Flask
from flask import jsonify, request
from shared import Mailer
from shared import Hasher
from shared import vdf

app = Flask(__name__)
app.config.from_pyfile('../config/app_config.py')

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

@app.route("/login", methods=['POST'])
def login():
    success = 0
    hasher = Hasher()

    email = request.json['email']
    password = request.json['password']
    password = hasher.hash_string(password)

    db = shared.database()
    sql = "select * from users where email='{:s}' and password='{:s}' and confirmed=1".format(email, password)
    db.request(sql)
    if not db.getRowCount():
        return jsonify({'success': 0, 'method': 'login'})

    user_id = db.getResult()[0]['id']
    sql = "select * from login where user_id={:d}".format(user_id)
    db.request(sql)

    if not db.getRowCount():
        # insert new token
        token = hasher.generate_hash(52)
        sql = "insert into login (user_id, token) values ({:d}, '{:s}') returning id".format(user_id, token)
        db.request(sql)
    else:
        # update last_seen
        token = db.getResult()[0]['token']
        sql = "update login set last_seen=DEFAULT where token='{:s}';".format(token)
        db.request(sql)

    if not db.getError() and db.getRowCount() == 1:
        success = 1
        
    return jsonify({'success': success, 'method': 'login', 'token': token})


@app.route("/auth", methods=['POST'])
def auth():
    success = 0

    token = request.json['token']

    db = shared.database()
    sql = "select * from login where token='{:s}';".format(token)
    db.request(sql)
    if db.getRowCount():
        success = 1 

    return jsonify({'success': success, 'method': 'auth'})

def auth_user(token):
    success = 0
    user_id = None

    db = shared.database()
    sql = "select * from login where token='{:s}';".format(token)
    db.request(sql)
    if db.getRowCount():
        success = 1
        user_id = db.getResult()[0]['user_id']

    return {'success': success, 'user_id': user_id}



@app.route("/profile/get", methods=['POST'])
def profile_get():
    success = 0
    result = []

    token = request.json['token']
    auth_result = auth_user(token)

    if not auth_result['success']:
        return jsonify({'success': success})

    user_id = auth_result['user_id']
    db = shared.database()
    
    # get user_info
    sql = """
        select users.*, users_info.*
        from users
        inner join users_info
        on users.id = users_info.user_id
        where users.id='{:d}'
    """.format(user_id)

    db.request(sql)
    if db.getRowCount():
        result = db.getResult()[0]
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    # get user_info
    sql = """
        select *
        from users_interests
        inner join interests
        on users_interests.interest_id = interests.id
        where users_interests.user_id='{:d}'
    """.format(user_id)
    vdf(sql)

    db.request(sql)
    if not db.getError():
        success = 1
        result_interests = db.getResult()
        interests_string = ""
        for interest_row in result_interests:
            separator = "" if not interests_string else ", "
            interests_string = interests_string + separator +  interest_row['interest']
        result['interests'] = interests_string    
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    return jsonify({'success': success, 'result': result})

