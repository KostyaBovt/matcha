from flask import Flask
from flask import jsonify, request
from shared import Mailer
from shared import Hasher
from shared import FileSaver
from shared import vdf
import base64
import os

app = Flask(__name__)
app.config.from_pyfile('../config/app_config.py')


@app.route("/mail")
def test_mail():
    mailer = Mailer()
    hasher = Hasher()
    mailer.send_register_confirm("recepient_name", "kostya.bovt@gmail.com", hasher.hash_string("kostya.bovt@gmail.com"), hasher.generate_hash(32))
    return "email is send!"


def validate_email_exist(email):
    from validate_email import validate_email
    is_valid = validate_email(email, verify=True)
    return is_valid

def validate_password(password):
    import re
    
    result = re.match(r"^[A-Za-z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]{8,32}$", password)
    if not result:
        return False
    if re.search('[0-9]',password) is None:
        return False
    if re.search('[a-z]',password) is None:
        return False
    if re.search('[A-Z]',password) is None:
        return False
    if re.search(r"[\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]",password) is None:
        return False

    return True

def validate_username(password):
    import re
    if re.match(r"^[A-Za-z0-9\.\_\-]{1,32}$", password):
        return True
    else:
        return False

def validate_name(password):
    import re
    if re.match(r"^[A-Za-z\-]{1,32}$", password):
        return True
    else:
        return False

@app.route("/register", methods=['POST'])
def register():
    success = 0
    mailer = Mailer()
    hasher = Hasher()
    db = shared.database()

    input_error = 0

    errors = {}

    email = request.json.get('email')
    username = request.json.get('username')
    fname = request.json.get('fname')
    sname = request.json.get('sname')
    password = request.json.get('password')


    # validate email
    if not email:
        errors['email'] = 'email must be specified'
        input_error = 1   
    elif not validate_email_exist(email):
        errors['email'] = 'email does not exist'
        input_error = 1
    else:
        sql = "select * from users where email=%s"
        args = (email,)
        db.request2(sql, args)
        if db.getRowCount():
            errors['email'] = 'This email is already in use'
            input_error = 1

    # validate username
    if not username:
        errors['username'] = 'username must be specified'
        input_error = 1   
    elif not validate_username(username):
        errors['username'] = 'username is not valid'
        input_error = 1
    else:
        sql = "select * from users_info where username=%s"
        args = (username,)
        db.request2(sql, args)
        if db.getRowCount():
            errors['username'] = 'This username is already in use'
            input_error = 1

    # validate fname
    if not fname:
        errors['fname'] = 'first name must be specified'
        input_error = 1   
    elif not validate_name(fname):
        errors['fname'] = 'first name is not valid'
        input_error = 1

    # validate sname
    if not sname:
        errors['sname'] = 'second name must be specified'
        input_error = 1   
    elif not validate_name(sname):
        errors['sname'] = 'second name is not valid'
        input_error = 1

    # validate password
    if not password:
        errors['password'] = 'password must be specified'
        input_error = 1
    elif not validate_password(password):
        errors['password'] = 'password is not secure enough'
        input_error = 1        

    if errors:
        return jsonify({'success': success, 'method': 'register', 'errors': errors})

    password = hasher.hash_string(password)

    sql = "insert into users (email, password, confirmed) values (%s, %s, 0) returning id"
    args = (email, password, )
    db.request2(sql, args)
    user_id = db.getLastRowId()

    sql = "insert into users_info (user_id, username, fname, sname) values (%s, %s, %s, %s) returning id"

    args = (user_id, username, fname, sname)
    db.request2(sql, args)

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

    sql = "select * from confirm where email_hash=%s and confirm_hash=%s;"
    args = (email_hash, confirm_hash,)
    db.request2(sql, args)

    if db.getRowCount():
        success = 1
        user_id = db.getResult()[0]['user_id']
        sql = "update users set confirmed={:d} where id={:d};".format(1, user_id)
        db.request(sql)        

    return jsonify({'success': success, 'method': 'confirm'})


@app.route("/forgot", methods=['POST'])
def forgot():

    success = 0
    email = request.json.get('email')
    input_error = 0
    errors = {}


    db = shared.database()

    # validate email
    if not email:
        errors['email'] = 'email must be specified'
        input_error = 1   
    else:
        sql = "select * from users where email=%s"
        args = (email,)
        db.request2(sql, args)
        if not db.getRowCount():
            errors['email'] = 'No user with such email'
            input_error = 1

    if errors:
        return jsonify({'success': success, 'method': 'forgot', 'errors': errors})


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

    sql = "select * from forgot where email_hash=%s and reset_hash=%s;"
    args = (email_hash, reset_hash,)
    db.request2(sql, args)

    if db.getRowCount():
        success = 1

    return jsonify({'success': success, 'method': 'check_reset'})

@app.route("/reset", methods=['POST'])
def reset():
    success = 0
    hasher = Hasher()
    input_error = 0
    errors = {}

    email = request.json.get('email')

    email_hash = request.json.get('email_hash')
    reset_hash = request.json.get('reset_hash')
    password = request.json.get('password')
    repeat_password = request.json.get('repeat_password')


    # validate email_hash
    if not email_hash:
        errors['email_hash'] = 'email_hash must be specified'
        input_error = 1  

    # validate reset_hash
    if not reset_hash:
        errors['reset_hash'] = 'reset_hash must be specified'
        input_error = 1  

    # check if hashes exist in db
    db = shared.database()
    sql = "select * from forgot where email_hash=%s and reset_hash= %s;"
    args = (email_hash, reset_hash,)
    db.request2(sql, args)
    if not db.getRowCount():
        errors['email_reset_hash'] = 'invalid email or/and reset hash'
        input_error = 1 


    # validate password
    if not password:
        errors['password'] = 'password must be specified'
        input_error = 1
    elif not validate_password(password):
        errors['password'] = 'password is not secure enough'
        input_error = 1 

    # validate repeat_password
    if not repeat_password:
        errors['repeat_password'] = 'repeat_password must be specified'
        input_error = 1

    if password and repeat_password and password != repeat_password:
        errors['repeat_password'] = 'repeat_password is not equal password'
        input_error = 1 

    if errors:
        return jsonify({'success': success, 'method': 'reset', 'errors': errors})


    password = hasher.hash_string(password)
    repeat_password = hasher.hash_string(repeat_password)

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
    input_error = 0
    errors = {}

    username = request.json.get('username')
    password = request.json.get('password', '').encode('utf8')


    # validate email
    if not username:
        errors['username'] = 'username must be specified'
        input_error = 1  

    # validate password
    if not password:
        errors['password'] = 'password must be specified'
        input_error = 1 

    # validate if email and password valid
    if password and username:
        password = hasher.hash_string(password)
        db = shared.database()
        sql = """
            select users.*, users_info.*
            from users
            inner join users_info on users.id=users_info.user_id
            where users_info.username=%s
            and users.password=%s
            and confirmed=1"""
        args = (username, password,)
        db.request2(sql, args)
        if not db.getRowCount():
            errors['username_password'] = 'username or password is wrong'
            input_error = 1 

    if errors:
        return jsonify({'success': success, 'method': 'login', 'errors': errors})


    user_id = db.getResult()[0]['user_id']
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
    sql = "select * from login where token=%s;"
    args = (token,)
    db.request2(sql, args)
    if db.getRowCount():
        success = 1 
        sql = "update login set last_seen=DEFAULT where token='{:s}';".format(token)
        db.request(sql)

    return jsonify({'success': success, 'method': 'auth'})

def auth_user(token):
    success = 0
    user_id = None

    db = shared.database()
    sql = "select * from login where token=%s;"
    args = (token,)
    db.request2(sql, args)
    if db.getRowCount():
        success = 1
        user_id = db.getResult()[0]['user_id']
        sql = "update login set last_seen=DEFAULT where token='{:s}';".format(token)
        db.request(sql)

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
        select users.*, users_info.*, avatar_count.avatar
        from users
        inner join users_info
        on users.id = users_info.user_id
        left join (select avatar, user_id from photos where user_id={:d} and avatar=1) as avatar_count on avatar_count.user_id = users.id
        where users.id='{:d}'
    """.format(user_id, user_id)

    db.request(sql)
    if db.getRowCount():
        result = db.getResult()[0]
        result['rating'] = str(result['rating'])
        result['geo_lat'] = str(result['geo_lat'])
        result['geo_lng'] = str(result['geo_lng'])
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    # get user interests
    sql = """
        select *
        from users_interests
        inner join interests
        on users_interests.interest_id = interests.id
        where users_interests.user_id='{:d}'
    """.format(user_id)

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

@app.route("/profile/update", methods=['POST'])
def profile_update():
    success = 0
    result = []
    input_error = 0
    errors = {}

    # authorize
    token = request.json.get('token')
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    username = request.json.get('username')
    fname = request.json.get('fname')
    sname = request.json.get('sname')
    gender = int(request.json.get('gender', 0))
    sex_preference = int(request.json.get('sex_preference', 0))
    birth = request.json.get('birth')
    phone = request.json.get('phone')
    bio = request.json.get('bio')
    interests = request.json.get('interests')


    # get db
    db = shared.database()

    # validate username
    if not username:
        errors['username'] = 'username must be specified'
        input_error = 1
    elif not validate_username(username):
        errors['username'] = 'username is not valid'
        input_error = 1
    else:
        sql = "select * from users_info where username=%s and not user_id=%s"
        args = (username, user_id,)
        db.request2(sql, args)
        if db.getRowCount():
            errors['username'] = 'This username is already in use'
            input_error = 1

    # validate fname
    if not fname:
        errors['fname'] = 'fname must be specified'
        input_error = 1 
    elif not validate_name(fname):
        errors['fname'] = 'fname is not valid'
        input_error = 1

    # validate sname
    if not sname:
        errors['sname'] = 'sname must be specified'
        input_error = 1
    elif not validate_name(sname):
        errors['sname'] = 'sname is not valid'
        input_error = 1

    # validate gender
    if not gender:
        errors['gender'] = 'gender must be specified'
        input_error = 1 
    elif not int(gender) in [1, 2]:
        errors['gender'] = 'gender is not valid'
        input_error = 1
    else:
        gender = int(gender)

    # validate sex_preference
    if not sex_preference:
        errors['sex_preference'] = 'sex_preference must be specified'
        input_error = 1
    elif not int(sex_preference) in [1, 2, 3]:
        errors['sex_preference'] = 'sex_preference is not valid'
        input_error = 1
    else:
        sex_preference = int(sex_preference)


    import datetime
    if birth:
        birth = datetime.datetime.strptime(birth, "%Y-%m-%d")

    # validate birth
    if not birth:
        errors['birth'] = 'birth must be specified'
        input_error = 1
    elif birth > datetime.datetime.strptime('2002-12-31', "%Y-%m-%d"):
        errors['birth'] = 'birth date is too big'
        input_error = 1 
    elif birth < datetime.datetime.strptime('1920-01-01', "%Y-%m-%d"):
        errors['birth'] = 'birth date is too low'
        input_error = 1 

    # validate phone
    if not phone:
        errors['phone'] = 'phone must be specified'
        input_error = 1
    elif len(phone) > 16:
        errors['phone'] = 'phone is too long'
        input_error = 1


    # validate bio
    if not bio:
        errors['bio'] = 'bio must be specified'
        input_error = 1
    elif len(bio) > 1000:
        bio = bio[:1000]


    # validate interests
    if not interests:
        pass
    elif len(interests) > 3000:
        interests = interests[:3000]

    if errors:
        return jsonify({'success': success, 'method': '/profile/update', 'errors': errors})

    # update user info
    sql = """
        update users_info
        set 
        username=%s, 
        fname=%s, 
        sname=%s, 
        gender=%s, 
        sex_preference=%s, 
        birth=%s, 
        phone=%s, 
        bio=%s 
        where user_id=%s
    """
    args = (username, fname, sname, gender, sex_preference, birth, phone, bio, user_id,)
    db.request2(sql, args)

    # interests per request
    split_interests = [x.strip('\'\" ') for x in interests.split(',')]
    split_interests = [x for x in split_interests if x]


    # update general interest table
    to_add_interests = []
    if split_interests:
        sql = "select * from interests where "
        add_or = ""
        for interest in split_interests:
            sql = sql + """
                {:s} interest=%s 
            """.format(add_or)
            if not add_or:
                add_or = "OR"
        db.request2(sql, tuple(split_interests))

        exist_interests = [x['interest'] for x in db.getResult()]
        to_add_interests = [item for item in split_interests if item not in exist_interests]

    # if some new interests detected - add to general table
    if to_add_interests:
        sql = """
            insert into interests (interest)
            values 
        """
        first = True
        for to_add in to_add_interests:
            if not first:
                sql = sql + ', '
            sql = sql + "(%s) "
            first = False
        db.request2(sql, tuple(to_add_interests), return_id_flag=False)

    # tricky approach - we will delete all interests and add new list :)
    
    # now deleting all interest of current user
    sql = """
        delete from users_interests where user_id={:d}
    """.format(user_id)
    db.request(sql)

    if split_interests:
        # getting all ids of new interests
        sql = "select * from interests where "
        add_or = ""
        for interest in split_interests:
            sql = sql + """
                {:s} interest=%s 
            """.format(add_or)
            if not add_or:
                add_or = "OR"        
        db.request2(sql, tuple(split_interests))
        exist_interests_ids = [x['id'] for x in db.getResult()]

        # insert all new interest ids fo current user
        sql = """
            insert into users_interests (interest_id, user_id) values 
        """
        first = True
        for interest_id in exist_interests_ids:
            if not first:
                sql = sql + ', '
            sql = sql + "({:d}, {:d})".format(interest_id, user_id)
            first = False
        db.request(sql, return_id_flag=False)

    # finally mark profile as 'filled'
    sql = "update users set filled=2 where id=%s"
    args = (user_id,)
    db.request2(sql, args,)


    if not db.getError():
        success = 1

    return jsonify({'success': success, 'method': 'profile/update'})


@app.route("/profile/update_password", methods=['POST'])
def profile_update_password():
    success = 0
    result = []
    input_error = 0
    errors = {}



    # get db and hasher
    db = shared.database()
    hasher = Hasher()

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    password = request.json.get('password', '').encode('utf8')
    new_password  = request.json.get('new_password')
    repeat_password  = request.json.get('repeat_password')


    if not password:
        errors['password'] = 'password must be specified'
        input_error = 1
    else:
        # validate current password
        sql = """
            select * from users
            where id={:d} and password='{:s}'
        """.format(user_id, hasher.hash_string(password))
        db.request(sql)

        if not db.getRowCount():
            errors['password'] = 'password is wrong'
            input_error = 1 


    if not new_password:
        errors['new_password'] = 'new_password must be specified'
        input_error = 1
    elif not validate_password(new_password):
        errors['new_password'] = 'new_password is not secure enough'
        input_error = 1 

    # validate repeat_password
    if not repeat_password:
        errors['repeat_password'] = 'repeat_password must be specified'
        input_error = 1

    if new_password and repeat_password and new_password != repeat_password:
        errors['repeat_password'] = 'repeat_password is not equal new_password'
        input_error = 1 

    if errors:
        return jsonify({'success': success, 'method': '/profile/update_password', 'errors': errors})

    # insert new password
    sql = """
        update users set password='{:s}' where id={:d}
    """.format(hasher.hash_string(new_password), user_id)
    db.request(sql)

    if not db.getError():
        success = 1

    return jsonify({'success': success, 'method': 'profile/update_password'})

@app.route("/profile/update_email", methods=['POST'])
def profile_update_email():
    success = 0
    result = []
    input_error = 0
    errors = {}

    # get db
    db = shared.database()
    hasher = Hasher()
    mailer = Mailer()

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    new_email = request.json.get('new_email')

    # validate new_email
    if not new_email:
        errors['new_email'] = 'new_email must be specified'
        input_error = 1   
    elif not validate_email_exist(new_email):
        errors['new_email'] = 'new_email does not exist'
        input_error = 1
    else:
        sql = "select * from users where email=%s and not id=%s"
        args = (new_email, user_id,)
        db.request2(sql, args)
        if db.getRowCount():
            errors['new_email'] = 'This email is already in use'
            input_error = 1

    if errors:
        return jsonify({'success': success, 'method': '/profile/update_email', 'errors': errors})

    # if hash for email update confirm for current user already exist - delete it
    sql = """delete from email_update where user_id={:d}""".format(user_id)
    db.request(sql)

    # continue if no email found
    email_hash = hasher.hash_string(new_email)
    confirm_hash = hasher.generate_hash(32)
    sql = """
        insert into email_update (user_id, new_email, email_hash, confirm_hash) values
        ({:d}, '{:s}', '{:s}', '{:s}') returning id
    """.format(user_id, new_email, email_hash, confirm_hash)
    db.request(sql)

    mailer.send_email_update_confirm(new_email, new_email, email_hash, confirm_hash)

    if not db.getError():
        success = 1

    return jsonify({'success': success, 'method': 'profile/update_email'})

@app.route("/confirm_update_email", methods=['POST'])
def confirm_update_email():

    email_hash = request.json['email_hash']
    confirm_hash = request.json['confirm_hash']

    db = shared.database()
    success = 0

    sql = "select * from email_update where email_hash=%s and confirm_hash=%s;"
    args = (email_hash, confirm_hash,)
    db.request2(sql, args)

    if db.getRowCount():
        user_id = db.getResult()[0]['user_id']
        new_email = db.getResult()[0]['new_email']
        sql = "update users set email='{:s}' where id={:d};".format(new_email, user_id)
        db.request(sql)        

        sql = "delete from email_update where user_id={:d}".format(user_id)
        db.request(sql)        

        if not db.getError():
            success = 1

    return jsonify({'success': success, 'method': 'confirm_update_email'})

@app.route("/profile/upload_photo", methods=['POST'])
def profile_upload_photo():
    success = 0
    result = []
    input_error = 0
    errors = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    # get db, hasher filesaver
    filesaver = FileSaver()
    hasher = Hasher()
    db = shared.database()

    # check how many photos already per current
    sql = 'select * from photos where user_id={:d}'.format(user_id)
    db.request(sql)
    if db.getRowCount() is 5: # TO TEST!!!!!!!!!!!!!!!!!!!!!!!
        return jsonify({'success': success})

    avatar = 0
    if not db.getRowCount():
        avatar = 1


    raw_photo = request.json.get('photoValue')
    if not raw_photo:
        return jsonify({'success': success})
    photo_value = base64.b64decode(request.json['photoValue'])
    photo_hash = hasher.generate_hash(32)
    photo_extention = 'jpeg'
    photo_path = '/vagrant/backend/data/photos'
    filesaver.save_file(value=photo_value, name=photo_hash, extention="jpeg", path=photo_path)

    # validate saved image by Pillow library
    from PIL import Image
    try:
        Image.open(photo_path + "/" + photo_hash + ".jpeg")
    except IOError:
        errors['photo'] = 'invalid photo format'
        input_error = 1
        os.remove(photo_path + "/" + photo_hash + ".jpeg")

    if errors:
        return jsonify({'success': success, 'method': '/profile/upload_photo', 'errors': errors})

    #insert new photo to db
    sql = """
        insert into photos (user_id, name, hash, avatar)
        values ({:d}, '{:s}', '{:s}', {:d}) returning id
    """.format(user_id, photo_hash + "." + photo_extention, photo_hash, avatar)
    db.request(sql)

    return jsonify({'success': 1, 'method': 'profile/upload_photo'})

@app.route("/profile/get_profile_photos", methods=['POST'])
def get_profile_photos():
    success = 0
    result = []
    filesaver = FileSaver()

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    # get db
    db = shared.database()

    # check how many photos already per current
    sql = 'select * from photos where user_id={:d}'.format(user_id)
    db.request(sql)
    if not db.getRowCount():
        return jsonify({'success': success})

    response_photos = []
    photos = db.getResult()
    for photo in photos:
        response_photo = {};
        response_photo['src'] = base64.b64encode(filesaver.read_file(photo['name'], '/vagrant/backend/data/photos'))
        response_photo['avatar'] = photo['avatar']
        response_photo['hash'] = photo['hash']
        response_photos.append(response_photo)

    success = 1
    return jsonify({'success': success, 'method': 'get_profile_photos', 'photos': response_photos})

@app.route("/profile/set_avatar", methods=['POST'])
def set_avatar():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    # get db
    db = shared.database()

    # first set all photos to avatar = 0 (just reset)
    sql = 'update photos set avatar=0 where user_id={:d}'.format(user_id)
    db.request(sql)

    # set new avatar
    photo_hash = request.json['photo_hash']
    sql = "update photos set avatar=1 where hash=%s"
    args = (photo_hash,)
    db.request2(sql, args)

    success = 1
    return jsonify({'success': success, 'method': 'set_avatar'})

@app.route("/profile/delete_photo", methods=['POST'])
def delete_photo():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']
    photo_hash = request.json.get('photo_hash')

    # get db
    db = shared.database()

    # delete the photo  if it is actually user`s photo
    sql = "select * from photos where user_id=%s and hash=%s"
    args = (user_id, photo_hash,)
    db.request2(sql, args)

    if db.getRowCount():
        sql = "delete from photos where user_id=%s and hash=%s"
        args = (user_id, photo_hash,)
        db.request2(sql, args)

        # actually delete photo
        os.remove("/vagrant/backend/data/photos/" + photo_hash + ".jpeg")


    success = 1
    return jsonify({'success': success, 'method': 'profile/delete_photo'})


@app.route("/profile/update_geotype", methods=['POST'])
def update_geotype():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    # get db
    db = shared.database()

    # get args
    geo_type = int(request.json['geo_type'])

    sql = "update users_info set geo_type=%s where user_id=%s"
    args = (geo_type, user_id,)
    db.request2(sql, args)

    success = 1
    return jsonify({'success': success, 'method': 'profile/update_geotype'})


@app.route("/profile/update_coords", methods=['POST'])
def update_coords():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    # get db
    db = shared.database()

    # get args
    lat = float(request.json['lat'])
    lng = float(request.json['lng'])

    sql = "update users_info set geo_lat=%s, geo_lng=%s where user_id=%s"
    args = (lat, lng, user_id,)
    db.request2(sql, args)

    success = 1
    return jsonify({'success': success, 'method': 'profile/update_coords'})

@app.route("/explore/search_mates", methods=['POST'])
def search_mates():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select users.*, users_info.*
        from users
        inner join users_info
        on users.id = users_info.user_id
        where users.id='{:d}'
    """.format(user_id)

    db.request(sql)
    if db.getRowCount():
        auth_user_info = db.getResult()[0]
        auth_user_info['rating'] = str(auth_user_info['rating'])
        auth_user_info['geo_lat'] = str(auth_user_info['geo_lat'])
        auth_user_info['geo_lng'] = str(auth_user_info['geo_lng'])
    else:    
        return jsonify({'success': success})

    # unpack request parameters
    interests = request.json.get('interests')

    if interests and len(interests) > 3000:
        interests = interests[:3000]

    sort = request.json['sort']
    sort = sort.split('_')
    bottomAge = int(request.json['bottomAge'])
    upperAge = int(request.json['upperAge'])
    bottomRating = float(request.json['bottomRating'])
    upperRating = float(request.json['upperRating'])
    online = request.json['online']
    radius = float(request.json['radius'])
    offset = (int(request.json['page']) - 1) * 10

    man = request.json.get('man')
    man_hetero = request.json.get('man_hetero')
    man_homo = request.json.get('man_homo')
    man_bi = request.json.get('man_bi')
    woman = request.json.get('woman')
    woman_hetero = request.json.get('woman_hetero')
    woman_lesbi = request.json.get('woman_lesbi')
    woman_bi = request.json.get('woman_bi')


    split_interests = [x.strip('\'\" ') for x in interests.split(',')]
    split_interests = [x for x in split_interests if x]
    split_interests = split_interests + ['some_mock_interest_to_prevent_error']

    inline_interests = "('some_blank_interest_to_avoid_error'"
    counter = 1
    for interest in split_interests:
        delimiter = ''
        if counter:
            delimiter = ', '
        inline_interests = inline_interests + delimiter + "'" + interest + "'"
        counter = counter + 1
    inline_interests = inline_interests + ')'

    # vdf(split_interests, 'split_interests')
    # vdf(inline_interests, 'inline_interests')
    # vdf(request.json, 'request')

    # get matched mates
    sql = """
        select users.*, users_info.*, user_match.matched_interests, distances.distance, date_part('year', AGE(users_info.birth)) as "age", avatars_table.avatar_name, online_table.last_seen,
         CASE WHEN online_table.last_seen > NOW() - INTERVAL '15 minutes' THEN 1
              ELSE 0
         END as online_status
        from users
        inner join users_info on users.id = users_info.user_id
        inner join
            (select user_id, name as "avatar_name" 
            from photos
            where photos.avatar = 1) as avatars_table
        on users.id=avatars_table.user_id
        left join
            (select user_id, last_seen from login
            ) as online_table
        on users.id=online_table.user_id
        left join
            (select user_id, count(interests.interest) as matched_interests 
            from users_interests
            inner join interests on users_interests.interest_id=interests.id
            where interests.interest in %s
            and not user_id={:d}
            group by user_id) as user_match
        on users.id=user_match.user_id
        inner join
            (select users_info.user_id, 2 * 3961 * asin(sqrt((sin(radians((users_info.geo_lat - {:s}) / 2))) ^ 2 + cos(radians({:s})) * cos(radians(users_info.geo_lat)) * (sin(radians((users_info.geo_lng - {:s}) / 2))) ^ 2)) as distance
            from users_info
            where not user_id={:d}
            and users_info.geo_lat is not null
            and users_info.geo_lng is not null
            ) as distances
        on users.id=distances.user_id
        where not users.id={:d}
        and not users.id in (select user_id_2 from likes where user_id_1={:d})
        and not users.id in (select user_id_1 from likes where user_id_2={:d} and (action=2 or action=3))
        and users_info.geo_lat is not null
        and users_info.geo_lng is not null
        and users.filled=2
        and distance < {:f}\n""".format(user_id, auth_user_info['geo_lat'], auth_user_info['geo_lat'], auth_user_info['geo_lng'], user_id, user_id, user_id, user_id, radius)



    man_sql = ''
    woman_sql = ''

    if man:
        if not man_hetero and not man_homo and not man_bi:
            man_sql = 'users_info.gender=1'
        else:
            pref_tuple = ()
            if man_hetero:
                pref_tuple += (2,)
            if man_homo:
                pref_tuple += (1,)
            if man_bi:
                pref_tuple += (3,)
            man_sql = 'users_info.gender=1 and users_info.sex_preference in %s' % (pref_tuple,)
            if len(pref_tuple) == 1:
                man_sql = man_sql.replace(",", "")
    if woman:
        if not woman_hetero and not woman_lesbi and not woman_bi:
            woman_sql = 'users_info.gender=2'
        else:
            pref_tuple = ()
            if woman_hetero:
                pref_tuple += (1,)
            if woman_lesbi:
                pref_tuple += (2,)
            if woman_bi:
                pref_tuple += (3,)
            woman_sql = 'users_info.gender=2 and users_info.sex_preference in %s' % (pref_tuple, )
            if len(pref_tuple) == 1:
                woman_sql = woman_sql.replace(",", "")

    if man_sql and woman_sql:
        sql = sql + '\t\tand ((%s) OR (%s))\n' % (man_sql, woman_sql,)
    elif man_sql:
        sql = sql + '\t\t and %s\n' % (man_sql,)        
    elif woman_sql:
        sql = sql + '\t\t and %s\n' % (woman_sql,)

    sql = sql + '\t\tand users_info.rating * 100 >= {:f}\n'.format(bottomRating)
    sql = sql + '\t\tand users_info.rating * 100 <= {:f}\n'.format(upperRating)

    sql = sql + '\t\tand EXTRACT(year from AGE(users_info.birth)) >= {:d}\n'.format(bottomAge)
    sql = sql + '\t\tand EXTRACT(year from AGE(users_info.birth)) <= {:d}\n'.format(upperAge)

    if online:
        sql = sql + """\t\tand online_table.last_seen > NOW() - INTERVAL '15 minutes'\n"""

    sort_mapping = {
        'match': 'user_match.matched_interests',
        'age': 'users_info.birth',
        'rating': 'users_info.rating',
        'dist': 'distances.distance'
    }

    sort_attribute = sort_mapping[sort[0]]
    sort_order = sort[1]
    if sort[0] == 'age':
        if sort_order =='asc':
            sort_order = 'desc'
        else:
            sort_order = 'asc'

    null_order = ''
    if sort[0] == 'match':
        null_order = ' NULLS LAST' if sort_order == 'desc' else ' NULLS FIRST'

    sql = sql + '\t\torder by ' + sort_attribute + ' ' + sort_order + null_order + ', distances.distance desc, users_info.rating desc, user_match.matched_interests desc NULLS LAST\n'

    sql = sql + '\t\tlimit 10 offset {:d}\n'.format(offset)

    # vdf(sql, 'sql')

    filesaver = FileSaver()
    args = (tuple(split_interests),)
    db.request2(sql, args)
    if db.getRowCount() and not db.getError():
        result_array = db.getResult()
        # vdf(result_array, 'result')
        for item in result_array:
            item['password'] = 'qwerty'
            item['rating'] = str(item['rating'])
            item['geo_lat'] = str(item['geo_lat'])
            item['geo_lng'] = str(item['geo_lng'])
            item['avatar_src'] = base64.b64encode(filesaver.read_file(item['avatar_name'], '/vagrant/backend/data/photos'))
    elif not db.getError():
        success = 1
        return jsonify({'success': success, 'result': None})
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    success = 1
    return jsonify({'success': success, 'method': 'explore/search_mates', 'result': result_array})

@app.route("/explore/search_connections", methods=['POST'])
def search_connections():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select users.*, users_info.*
        from users
        inner join users_info
        on users.id = users_info.user_id
        where users.id='{:d}'
    """.format(user_id)

    db.request(sql)
    if db.getRowCount():
        auth_user_info = db.getResult()[0]
        auth_user_info['rating'] = str(auth_user_info['rating'])
        auth_user_info['geo_lat'] = str(auth_user_info['geo_lat'])
        auth_user_info['geo_lng'] = str(auth_user_info['geo_lng'])
    else:    
        return jsonify({'success': success})

    # unpack request parameters
    interests = request.json.get('interests')

    if interests and len(interests) > 3000:
        interests = interests[:3000]

    sort = request.json['sort']
    sort = sort.split('_')
    bottomAge = int(request.json['bottomAge'])
    upperAge = int(request.json['upperAge'])
    bottomRating = float(request.json['bottomRating'])
    upperRating = float(request.json['upperRating'])
    online = request.json['online']
    radius = float(request.json['radius'])
    offset = (int(request.json['page']) - 1) * 10
    i_like_flag = request.json['i_like_flag']
    i_dislike_flag = request.json['i_dislike_flag']
    like_me_flag = request.json['like_me_flag']
    connections_flag = request.json['connections_flag']

    man = request.json.get('man')
    man_hetero = request.json.get('man_hetero')
    man_homo = request.json.get('man_homo')
    man_bi = request.json.get('man_bi')
    woman = request.json.get('woman')
    woman_hetero = request.json.get('woman_hetero')
    woman_lesbi = request.json.get('woman_lesbi')
    woman_bi = request.json.get('woman_bi')

    split_interests = [x.strip('\'\" ') for x in interests.split(',')]
    split_interests = [x for x in split_interests if x]
    split_interests = split_interests + ['some_mock_interest_to_prevent_error']

    inline_interests = "('some_blank_interest_to_avoid_error'"
    counter = 1
    for interest in split_interests:
        delimiter = ''
        if counter:
            delimiter = ', '
        inline_interests = inline_interests + delimiter + "'" + interest + "'"
        counter = counter + 1
    inline_interests = inline_interests + ')'

    # vdf(split_interests, 'split_interests')
    # vdf(inline_interests, 'inline_interests')

    # vdf(request.json, 'request')


    # get matched mates
    sql = """
        select users.*, users_info.*, user_match.matched_interests, distances.distance, date_part('year', AGE(users_info.birth)) as "age", avatars_table.avatar_name, online_table.last_seen, actions_table.action_of_user,
         CASE WHEN online_table.last_seen > NOW() - INTERVAL '15 minutes' THEN 1
              ELSE 0
         END as online_status
        from users
        inner join users_info on users.id = users_info.user_id
        left join
            (select user_id, name as "avatar_name" 
            from photos
            where photos.avatar = 1) as avatars_table
        on users.id=avatars_table.user_id
        left join
            (select user_id, last_seen from login
            ) as online_table
        on users.id=online_table.user_id
        left join
            (select user_id_2, action as action_of_user from likes where user_id_1={:d}
            ) as actions_table
        on users.id=actions_table.user_id_2
        left join
            (select user_id, count(interests.interest) as matched_interests 
            from users_interests
            inner join interests on users_interests.interest_id=interests.id
            where interests.interest in %s
            and not user_id={:d}
            group by user_id) as user_match
        on users.id=user_match.user_id
        inner join
            (select users_info.user_id, 2 * 3961 * asin(sqrt((sin(radians((users_info.geo_lat - {:s}) / 2))) ^ 2 + cos(radians({:s})) * cos(radians(users_info.geo_lat)) * (sin(radians((users_info.geo_lng - {:s}) / 2))) ^ 2)) as distance
            from users_info
            where not user_id={:d}
            and users_info.geo_lat is not null
            and users_info.geo_lng is not null
            ) as distances
        on users.id=distances.user_id
        where not users.id={:d}
        and not users.id in (select user_id_1 from likes where user_id_2={:d} and (action = 2 or action = 3))
        and users_info.geo_lat is not null
        and users_info.geo_lng is not null
        and distance < {:f}\n""".format(user_id, user_id, auth_user_info['geo_lat'], auth_user_info['geo_lat'], auth_user_info['geo_lng'], user_id, user_id, user_id, radius)

    if (i_like_flag):
        sql = sql + '\t\tand users.id in (select user_id_2 from likes where user_id_1={:d} and action=1 and not user_id_2 in (select user_id_1 from likes where user_id_2={:d}))\n'.format(user_id, user_id)

    if (i_dislike_flag):
        sql = sql + '\t\tand users.id in (select user_id_2 from likes where user_id_1={:d} and action=2)\n'.format(user_id)

    if (like_me_flag):
        sql = sql + """\t\tand users.id in (select user_id_1 from likes where user_id_2={:d} and action=1 and user_id_1 not in (select user_id_2 from likes where user_id_1={:d} and (action=2 or action=3 or action=1)))\n""".format(user_id, user_id)

    if (connections_flag):
        sql = sql + """\t\tand users.id in (select user_id_2 from likes where user_id_1={:d} and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2={:d} and action=1))\n""".format(user_id, user_id)

    man_sql = ''
    woman_sql = ''

    if man:
        if not man_hetero and not man_homo and not man_bi:
            man_sql = 'users_info.gender=1'
        else:
            pref_tuple = ()
            if man_hetero:
                pref_tuple += (2,)
            if man_homo:
                pref_tuple += (1,)
            if man_bi:
                pref_tuple += (3,)
            man_sql = 'users_info.gender=1 and users_info.sex_preference in %s' % (pref_tuple,)
            if len(pref_tuple) == 1:
                man_sql = man_sql.replace(",", "")
    if woman:
        if not woman_hetero and not woman_lesbi and not woman_bi:
            woman_sql = 'users_info.gender=2'
        else:
            pref_tuple = ()
            if woman_hetero:
                pref_tuple += (1,)
            if woman_lesbi:
                pref_tuple += (2,)
            if woman_bi:
                pref_tuple += (3,)
            woman_sql = 'users_info.gender=2 and users_info.sex_preference in %s' % (pref_tuple, )
            if len(pref_tuple) == 1:
                woman_sql = woman_sql.replace(",", "")

    if man_sql and woman_sql:
        sql = sql + '\t\tand ((%s) OR (%s))\n' % (man_sql, woman_sql,)
    elif man_sql:
        sql = sql + '\t\t and %s\n' % (man_sql,)        
    elif woman_sql:
        sql = sql + '\t\t and %s\n' % (woman_sql,)

    sql = sql + '\t\tand users_info.rating * 100 >= {:f}\n'.format(bottomRating)
    sql = sql + '\t\tand users_info.rating * 100 <= {:f}\n'.format(upperRating)

    sql = sql + '\t\tand EXTRACT(year from AGE(users_info.birth)) >= {:d}\n'.format(bottomAge)
    sql = sql + '\t\tand EXTRACT(year from AGE(users_info.birth)) <= {:d}\n'.format(upperAge)

    if online:
        sql = sql + """\t\tand online_table.last_seen > NOW() - INTERVAL '15 minutes'\n"""

    sort_mapping = {
        'match': 'user_match.matched_interests',
        'age': 'users_info.birth',
        'rating': 'users_info.rating',
        'dist': 'distances.distance'
    }

    sort_attribute = sort_mapping[sort[0]]
    sort_order = sort[1]
    if sort[0] == 'age':
        if sort_order =='asc':
            sort_order = 'desc'
        else:
            sort_order = 'asc'

    null_order = ''
    if sort[0] == 'match':
        null_order = ' NULLS LAST' if sort_order == 'desc' else ' NULLS FIRST'

    sql = sql + '\t\torder by ' + sort_attribute + ' ' + sort_order + null_order + ', distances.distance desc, users_info.rating desc, user_match.matched_interests desc NULLS LAST\n'

    sql = sql + '\t\tlimit 10 offset {:d}\n'.format(offset)

    # vdf(sql, 'sql')

    filesaver = FileSaver()
    args = (tuple(split_interests),)
    db.request2(sql, args)
    if db.getRowCount() and not db.getError():
        result_array = db.getResult()
        # vdf(result_array, 'result')
        for item in result_array:
            item['password'] = 'qwerty'
            item['rating'] = str(item['rating'])
            item['geo_lat'] = str(item['geo_lat'])
            item['geo_lng'] = str(item['geo_lng'])
            if item['avatar_name']:
                item['avatar_src'] = base64.b64encode(filesaver.read_file(item['avatar_name'], '/vagrant/backend/data/photos'))
            else :
                item['avatar_src'] = base64.b64encode(filesaver.read_file('blank-avatar.jpg', '/vagrant/backend/data'))
    elif not db.getError():
        success = 1
        return jsonify({'success': success, 'result': None})
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    success = 1
    return jsonify({'success': success, 'method': 'explore/search_mates', 'result': result_array})



@app.route("/explore/get_mate", methods=['POST'])
def get_mate():
    success = 0
    result = []

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    to_log = int(request.json.get('to_log', 0))

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select users.*, users_info.*
        from users
        inner join users_info
        on users.id = users_info.user_id
        where users.id='{:d}'
    """.format(user_id)

    db.request(sql)
    if db.getRowCount():
        auth_user_info = db.getResult()[0]
        auth_user_info['rating'] = float(auth_user_info['rating'])
        auth_user_info['geo_lat'] = float(auth_user_info['geo_lat'])
        auth_user_info['geo_lng'] = float(auth_user_info['geo_lng'])
    else:    
        return jsonify({'success': success})

    # unpack request parameters
    mate_id = int(request.json['mate_id'])


    # get info of mate
    sql = """
        select users.*, users_info.*, date_part('year', AGE(users_info.birth)) as "age", login.last_seen,
            CASE WHEN login.last_seen > NOW() - INTERVAL '15 minutes' THEN 1
                 ELSE 0
            END as online_status
        from users
        left join login on users.id = login.user_id
        inner join users_info on users.id = users_info.user_id
        where users.id=%s
    """
    args = (mate_id,)

    db.request2(sql, args)
    if db.getRowCount():
        result = db.getResult()[0]
        result['rating'] = float(result['rating'])
        result['geo_lat'] = float(result['geo_lat'])
        result['geo_lng'] = float(result['geo_lng'])
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    # get user interests
    sql = """
        select *
        from users_interests
        inner join interests
        on users_interests.interest_id = interests.id
        where users_interests.user_id=%s
    """
    args = (mate_id,)
    db.request2(sql, args)
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

    # get mates photos and avatar
    filesaver = FileSaver()
    sql = "select * from photos where user_id = %s"
    args = (mate_id,)
    db.request2(sql, args)
    photos = []
    avatar = ''
    if db.getRowCount():
        result_photos = db.getResult()
        for result_photo in result_photos:
            photos.append({'src': base64.b64encode(filesaver.read_file(result_photo['name'], '/vagrant/backend/data/photos'))})
            if result_photo['avatar'] == 1:
                avatar = {'src': base64.b64encode(filesaver.read_file(result_photo['name'], '/vagrant/backend/data/photos'))}
    elif not db.getRowCount() and not db.getError():
        photos.append({'src': base64.b64encode(filesaver.read_file('blank-avatar.jpg', '/vagrant/backend/data'))})
        avatar = {'src': base64.b64encode(filesaver.read_file('blank-avatar.jpg', '/vagrant/backend/data'))}
    elif db.getError():
        success = 0
        return jsonify({'success': success, 'result': None})

    result['photos'] = photos
    result['avatar'] = avatar
    import math
    result['distance'] = 2 * 3961 * math.asin(math.sqrt((math.sin(math.radians((result['geo_lat'] - auth_user_info['geo_lat']) / 2))) ** 2 + math.cos(math.radians(auth_user_info['geo_lat'])) * math.cos(math.radians(result['geo_lat'])) * (math.sin(math.radians((result['geo_lng'] - auth_user_info['geo_lng']) / 2))) ** 2))

    #get actions (like, disllike) of user
    sql = 'select * from likes where user_id_1={:d} and user_id_2={:d}'.format(user_id, mate_id)
    db.request(sql)
    if db.getRowCount():
        actions_result = db.getResult()[0]
        result['action_of_user'] = actions_result['action']
    else:
        result['action_of_user'] = None

    #get actions (like, disllike) to user
    sql = 'select * from likes where user_id_1={:d} and user_id_2={:d}'.format(mate_id, user_id)
    db.request(sql)
    if db.getRowCount():
        actions_result = db.getResult()[0]
        result['action_to_user'] = actions_result['action']
    else:
        result['action_to_user'] = None

    # finally log this action in notification table (action visit)

    if (to_log and result['action_of_user'] != 2 and result['action_to_user'] != 2):
        sql = "insert into notifications (user_id_1, user_id_2, action) values ({:d}, {:d}, {:d});".format(user_id, mate_id, 40)
        db.request(sql, False)

    success = 1
    return jsonify({'success': success, 'method': 'explore/search_mates', 'result': result})

def calulate_raiting(user_id):
    db = shared.database()
    sql = "select * from likes where user_id_2={:d} and action=1;".format(user_id)
    db.request(sql)
    likes = len(db.getResult())

    sql = "select * from likes where user_id_2={:d} and action=2;".format(user_id)
    db.request(sql)
    dislikes = len(db.getResult())

    base_rating = 0.5
    if not likes and not dislikes:
        additive_rating = 0
    elif not likes and dislikes > 0:
        additive_rating = 0
    else:
        additive_rating = 0.5 * likes / (likes + dislikes)

    rating = round(base_rating + additive_rating, 4)
    return rating

def update_rating(user_id):
    db = shared.database()
    new_rating = calulate_raiting(user_id)
    sql = "update users_info set rating={:f} where user_id={:d}".format(new_rating, user_id)
    db.request(sql)

@app.route("/explore/like", methods=['POST'])
def like():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (user_id, mate_id,)

    # actions: 1 - like, 2 - dislike
    db.request2(sql, args)
    if db.getRowCount():
        # just update action
        sql = 'update likes set action=1 where user_id_1=%s and user_id_2=%s'
        args = (user_id, mate_id,)
        db.request2(sql, args)
        success = 1
    else:
        sql = 'insert into likes (user_id_1, user_id_2, action) values (%s, %s, 1)'
        args = (user_id, mate_id,)
        db.request2(sql, args, False)
        success = 1

    # update action of mate (if he perofrmed action during profile view)    
    sql = """
        select action
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (mate_id, user_id,)
    db.request2(sql, args)
    if db.getRowCount():
        result['action_to_user'] = db.getResult()[0]['action']
    else: 
        result['action_to_user'] = None

    #update rating
    update_rating(mate_id)

    # finally log this action in notification table (10  - like, 11 - like back)
    like_type = 11 if result['action_to_user'] == 1 else 10
    sql = "insert into notifications (user_id_1, user_id_2, action) values (%s, %s, %s);"
    args = (user_id, mate_id, like_type,)
    db.request2(sql, args, False)

    return jsonify({'success': success, 'method': 'explore/like', 'result': result})


@app.route("/explore/dislike", methods=['POST'])
def dislike():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (user_id, mate_id,)

    # actions: 1 - like, 2 - dislike,  3 - report
    db.request2(sql, args)
    if db.getRowCount():
        # just update action
        sql = 'update likes set action=2 where user_id_1=%s and user_id_2=%s'
        args = (user_id, mate_id,)
        db.request2(sql, args)
        success = 1
    else:
        sql = 'insert into likes (user_id_1, user_id_2, action) values (%s, %s, 2)'
        agrs = (user_id, mate_id,)
        db.request2(sql, args, False)
        success = 1

    # update action of mate (if he perofrmed action during profile view)    
    sql = """
        select action
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (mate_id, user_id,)
    db.request2(sql, args)
    if db.getRowCount():
        result['action_to_user'] = db.getResult()[0]['action']
    else: 
        result['action_to_user'] = None

    #update rating
    update_rating(mate_id)

    return jsonify({'success': success, 'method': 'explore/dislike', 'result': result})


@app.route("/explore/unlike", methods=['POST'])
def unlike():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1=%s
        and user_id_2=%s
        and action=1
    """
    args = (user_id, mate_id,)

    # actions: 1 - like, 2 - dislike
    db.request2(sql, args)
    if db.getRowCount():
        # just update action
        sql = 'delete from likes where user_id_1=%s and user_id_2=%s and action=1'
        agrs = (user_id, mate_id,)
        db.request2(sql, args)
        success = 1
    else:
        # nothing to unlike
        success = 1

    # update action of mate (if he perofrmed action during profile view)    
    sql = """
        select action
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (mate_id, user_id,)
    db.request2(sql, args)
    if db.getRowCount():
        result['action_to_user'] = db.getResult()[0]['action']
    else: 
        result['action_to_user'] = None

    #update rating
    update_rating(mate_id)

    # finally log this action in notification table
    unlike_type = 51 if result['action_to_user'] == 1 else 50 
    sql = "insert into notifications (user_id_1, user_id_2, action) values (%s, %s, %s);"
    args = (user_id, mate_id, unlike_type,)
    db.request2(sql, args, False)

    return jsonify({'success': success, 'method': 'explore/unlike', 'result': result})


@app.route("/explore/undislike", methods=['POST'])
def undislike():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info action
    sql = """
        select *
        from likes
        where user_id_1=%s
        and user_id_2=%s
        and action=2
    """
    args = (user_id, mate_id,)

    # actions: 1 - like, 2 - dislike
    db.request2(sql, args)
    if db.getRowCount():
        # just update action
        sql = 'delete from likes where user_id_1=%s and user_id_2=%s and action=2'
        args = (user_id, mate_id,)
        db.request2(sql, args)
        success = 1
    else:
        # nothing to undislike
        success = 1

    # update action of mate (if he perofrmed action during profile view)    
    sql = """
        select action
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (mate_id, user_id,)
    db.request2(sql, args)
    if db.getRowCount():
        result['action_to_user'] = db.getResult()[0]['action']
    else: 
        result['action_to_user'] = None

    #update rating
    update_rating(mate_id)


    return jsonify({'success': success, 'method': 'explore/unlike', 'result': result})



@app.route("/explore/report", methods=['POST'])
def report():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (user_id, mate_id,)

    # actions: 1 - like, 2 - dislike,  3 - report
    db.request2(sql, args)
    if db.getRowCount():
        # just update action
        sql = 'update likes set action=3 where user_id_1=%s and user_id_2=%s'
        args =(user_id, mate_id,)
        db.request2(sql, args)
        success = 1
    else:
        sql = 'insert into likes (user_id_1, user_id_2, action) values (%s, %s, 3)'
        args = (user_id, mate_id,)
        db.request2(sql, args, False)
        success = 1

    # update action of mate (if he perofrmed action during profile view)    
    sql = """
        select action
        from likes
        where user_id_1=%s
        and user_id_2=%s
    """
    args = (mate_id, user_id)
    db.request2(sql, args)
    if db.getRowCount():
        result['action_to_user'] = db.getResult()[0]['action']
    else: 
        result['action_to_user'] = None

    return jsonify({'success': success, 'method': 'explore/report', 'result': result})



@app.route("/notifications/get_list", methods=['POST'])
def get_list():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    page = request.json['page']
    offset = (int(request.json['page']) - 1) * 15

    # get db
    db = shared.database()
    sql = """
        select notifications.*, users_info.username
        from notifications
        inner join users_info on notifications.user_id_1 = users_info.user_id
        where notifications.user_id_2=%s
        and not notifications.user_id_1 in (select user_id_2 from likes where user_id_1=%s and (action=2 or action=3))
        and not notifications.user_id_1 in (select user_id_1 from likes where user_id_2=%s and (action=2 or action=3))
        order by notifications.action_time desc
        limit 15
        offset %s
    """
    args = (user_id, user_id, user_id, offset,)
    db.request2(sql, args)

    if db.getRowCount():
        result['notifications'] = db.getResult()
    else: 
        result['notifications'] = None

    # mark last get notifs as read
    if result['notifications']:
        last_notifs_ids = "( -999"
        for item in result['notifications']:
            last_notifs_ids = last_notifs_ids + ", " + str(item['id'])
        last_notifs_ids = last_notifs_ids + ")"
        sql = "update notifications set seen=2 where id in {:s}".format(last_notifs_ids)
        db.request(sql)

    success = 1
    return jsonify({'success': success, 'method': 'notifications/get_list', 'result': result})




@app.route("/messages/get_current_mate_chat", methods=['POST'])
def get_current_mate_chat():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = int(request.json['mate_id'])

    db = shared.database()

    # check if you are connected
    sql = """
        select * from likes where user_id_1=%s and user_id_2=%s and action = 1 and user_id_1 in (select user_id_2 from likes where user_id_1=%s)
    """
    args = (user_id, mate_id, mate_id,)
    db.request2(sql, args)

    if not db.getRowCount():
        return jsonify({'method': '/messages/get_current_mate_chat', 'success': success})

    # actually get last 20 messages/ direction: 1 outcome, 2 income
    sql = """
        select * from (
            select *, 
                CASE WHEN messages.user_id_1 = %s THEN 1
                ELSE 2
                END as direction
            from messages
            where ((user_id_1=%s and user_id_2=%s) or (user_id_1=%s and user_id_2=%s))
            order by id desc
            limit 20
        ) as message_table
        order by message_table.id asc
    """
    args = (user_id, user_id, mate_id, mate_id, user_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['messages'] = db.getResult()
    else: 
        result['messages'] = None


    # mark last 20 messages as read
    if result['messages']:
        last_20_massages_ids = "( -999"
        for item in result['messages']:
            if item['direction'] == 2: # set seen only income messages
                last_20_massages_ids = last_20_massages_ids + ", " + str(item['id'])
        last_20_massages_ids = last_20_massages_ids + ")"
        sql = "update messages set seen=2 where id in {:s}".format(last_20_massages_ids)
        db.request(sql)

    success = 1
    return jsonify({'success': success, 'method': '/messages/get_current_mate_chat', 'result': result})


@app.route("/messages/send_msg", methods=['POST'])
def send_msg():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']


    mate_id = int(request.json['mate_id'])
    message = request.json['message'].encode('utf8')
    message = message[:100] if len(message) > 100 else message
    first_msg_id = int(request.json['first_msg_id'])

    db = shared.database()

    # check if you are connected
    sql = """
        select * from likes where user_id_1=%s and user_id_2=%s and action = 1 and user_id_1 in (select user_id_2 from likes where user_id_1=%s)
    """
    args = (user_id, mate_id, mate_id,)
    db.request2(sql, args)

    # if not connected - message is not permitted
    if not db.getRowCount():
        return jsonify({'method': '/messages/send_msg', 'success': success})

    # actually insert message
    sql = """
        insert into messages (user_id_1, user_id_2, message) values (%s, %s, %s) returning id
    """
    args = (user_id, mate_id, message,)
    db.request2(sql, args)

    # get id of last message
    last_message_id = db.getLastRowId()


    # get all messages that are before current messages and unread
    sql = """
        select * from (
            select *, 
                CASE WHEN messages.user_id_1 = %s THEN 1
                ELSE 2
                END as direction
            from messages
            where (user_id_1=%s and user_id_2=%s and id > %s and seen=1) or (id=%s)
            order by id desc
            limit 20
        ) as message_table
        order by message_table.id asc
    """
    args = (user_id, mate_id, user_id, first_msg_id, last_message_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['new_messages'] = db.getResult()
    else: 
        result['new_messages'] = None

    # mark as read nearly got messages
    if result['new_messages']:
        last_massages_ids = "( -999"
        for item in result['new_messages']:
            if item['direction'] == 2: # set seen only income messages
                last_massages_ids = last_massages_ids + ", " + str(item['id'])
        last_massages_ids = last_massages_ids + ")"
        sql = "update messages set seen=2 where id in {:s}".format(last_massages_ids)
        db.request(sql)


    success = 1
    return jsonify({'success': success, 'method': '/messages/send_msg', 'result': result})



@app.route("/messages/get_mate_list", methods=['POST'])
def get_mate_list():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    db = shared.database()
    sql = """
        select count(CASE WHEN seen=1 and user_id_2=%s THEN 1 END), max(action_time) as last_message_time, users_info.username, users_info.fname, users_info.sname,
            CASE WHEN messages_table.user_id_1 = %s THEN messages_table.user_id_2
            ELSE messages_table.user_id_1
            END as user_id_mate
        from (
            select * from messages where (
                (user_id_1=%s and user_id_2 in (select user_id_2 from likes where user_id_1=%s and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2=%s and action=1)))
                or (user_id_2=%s and user_id_1 in (select user_id_2 from likes where user_id_1=%s and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2=%s and action=1)))
            ) 
        ) as messages_table
        inner join users_info on
            CASE WHEN messages_table.user_id_1 = %s THEN messages_table.user_id_2 = users_info.user_id
            ELSE messages_table.user_id_1 = users_info.user_id
            END
        group by user_id_mate, users_info.username, users_info.fname, users_info.sname
        order by max(action_time)
    """
    args = (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['mate_list'] = db.getResult()
    else: 
        result['mate_list'] = None

    success = 1
    return jsonify({'success': success, 'method': '/messages/get_mate_list', 'result': result})


@app.route("/messages/load_prev_messages", methods=['POST'])
def load_prev_messages():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']
    mate_id = int(request.json['mate_id'])
    first_msg_id = int(request.json['first_msg_id'])

    db = shared.database()

    # get 20 messages that are before first_message_id
    sql = """
        select * from (
            select *, 
                CASE WHEN messages.user_id_1 = %s THEN 1
                ELSE 2
                END as direction
            from messages
            where ((user_id_1=%s and user_id_2=%s) or (user_id_1=%s and user_id_2=%s))
            and id < %s
            order by id desc
            limit 20
        ) as message_table
        order by message_table.id asc
    """
    args = (user_id, user_id, mate_id, mate_id, user_id, first_msg_id,)
    db.request2(sql, args)


    if db.getRowCount():
        result['prev_messages'] = db.getResult()
    else: 
        result['prev_messages'] = []


    # mark as read nearly got messages
    if result['prev_messages']:
        prev_massages_ids = "( -999"
        for item in result['prev_messages']:
            if item['direction'] == 2: # set seen only outcome messages
                prev_massages_ids = prev_massages_ids + ", " + str(item['id'])
        prev_massages_ids = prev_massages_ids + ")"
        sql = "update messages set seen=2 where id in {:s}".format(prev_massages_ids)
        db.request(sql)


    success = 1
    return jsonify({'success': success, 'method': '/messages/load_prev_messages', 'result': result})



@app.route("/messages/update_chat", methods=['POST'])
def update_chat():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']
    mate_id = int(request.json['mate_id'])
    first_msg_id = int(request.json['first_msg_id'])

    db = shared.database()

    # first get updated mate list
    sql = """
        select count(CASE WHEN seen=1 and user_id_2=%s and not user_id_1=%s THEN 1 END), max(action_time) as last_message_time, users_info.username, users_info.fname, users_info.sname,
            CASE WHEN messages_table.user_id_1 = %s THEN messages_table.user_id_2
            ELSE messages_table.user_id_1
            END as user_id_mate
        from (
            select * from messages where (
                (user_id_1=%s and user_id_2 in (select user_id_2 from likes where user_id_1=%s and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2=%s and action=1)))
                or (user_id_2=%s and user_id_1 in (select user_id_2 from likes where user_id_1=%s and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2=%s and action=1)))
            ) 
        ) as messages_table
        inner join users_info on
            CASE WHEN messages_table.user_id_1 = %s THEN messages_table.user_id_2 = users_info.user_id
            ELSE messages_table.user_id_1 = users_info.user_id
            END
        group by user_id_mate, users_info.username, users_info.fname, users_info.sname
        order by max(action_time)
    """
    args = (user_id, mate_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['mate_list'] = db.getResult()
    else: 
        result['mate_list'] = None

    # if chat with some mate is opened - we get new income messages for received mate id
    result['new_messages'] = []

    if mate_id > 0:
        sql = """
            select * from (
                select *, 
                    CASE WHEN messages.user_id_1 = %s THEN 1
                    ELSE 2
                    END as direction
                from messages
                where (user_id_1=%s and user_id_2=%s)
                and id > %s
                and seen=1
            ) as message_table
            order by message_table.id asc
        """
        args = (user_id, mate_id, user_id, first_msg_id,)
        db.request2(sql, args)


        if db.getRowCount():
            result['new_messages'] = db.getResult()
        else: 
            result['new_messages'] = []


        # mark as read nearly got messages
        if result['new_messages']:
            new_massages_ids = "( -999"
            for item in result['new_messages']:
                if item['direction'] == 2: # set seen only income messages
                    new_massages_ids = new_massages_ids + ", " + str(item['id'])
            new_massages_ids = new_massages_ids + ")"
            sql = "update messages set seen=2 where id in {:s}".format(new_massages_ids)
            db.request(sql)


    success = 1
    return jsonify({'success': success, 'method': '/messages/update_chat', 'result': result})


@app.route("/notifications/get_notif_count", methods=['POST'])
def get_notif_count():
    success = 0
    result = {}

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    db = shared.database()

    # get all income messages that unread ( but only from connected users)
    sql = """
        select count(*) from messages where user_id_2=%s and seen=1
        and user_id_1 in (select user_id_2 from likes where user_id_1=%s and action=1 and user_id_2 in (select user_id_1 from likes where user_id_2=%s and action=1))
    """
    args = (user_id, user_id, user_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['new_msg'] = db.getResult()[0]['count']
    else: 
        result['new_msg'] = 0



    # get all income notifs that unread ( but exclude from who dislike or report me and from whom i dislike or report)
    sql = """
        select count(*) from notifications where user_id_2=%s and seen=1
        and not user_id_1 in (select user_id_2 from likes where user_id_1=%s and (action=2 or action=3))
        and not user_id_1 in (select user_id_1 from likes where user_id_2=%s and (action=2 or action=3))
    """
    args = (user_id, user_id, user_id,)
    db.request2(sql, args)

    if db.getRowCount():
        result['new_notif'] = db.getResult()[0]['count']
    else: 
        result['new_notif'] = 0

    success = 1
    return jsonify({'success': success, 'method': '/messages/get_notif_count', 'result': result})
