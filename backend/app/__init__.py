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

    sql = "insert into users_info (user_id) values ({:d}) returning id".format(user_id)
    db.request(sql)

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

    sql = "update login set last_seen=DEFAULT where token='{:s}';".format(token)
    db.request(sql)

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
        sql = "update login set last_seen=DEFAULT where token='{:s}';".format(token)
        db.request(sql)

    return {'success': success, 'user_id': user_id}

def calulate_raiting(user_id):
    db = shared.database()
    sql = "select * likes where user_id_2='{:d} and action=1';".format(user_id)
    db.request(sql)
    likes = len(db.getResult())

    sql = "select * likes where user_id_2='{:d} and action=2';".format(user_id)
    db.request(sql)
    dislikes = len(db.getResult())

    base_rating = 0.5
    if not likes and not dislikes:
        additive_rating = 0
    elif not likes and dislikes > 0:
        additive_ratnig = 0
    else:
        additive_ratnig = 0.5 * likes / (likes + dislikes)

    rating = round(base_rating + additive_ratnig, 4)
    return rating


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

    # authorize
    token = request.json['token']
    auth_result = auth_user(token)

    # if not authorized - return immediately
    if not auth_result['success']:
        return jsonify({'success': success})

    # authorized user id
    user_id = auth_result['user_id']

    username = request.json['username']
    fname = request.json['fname']
    sname = request.json['sname']
    gender = 0 if not request.json['gender'] else int(request.json['gender'])
    sex_preference = 0 if not request.json['sex_preference'] else int(request.json['sex_preference'])
    birth = request.json['birth']
    phone = request.json['phone']
    bio = request.json['bio']

    # get db
    db = shared.database()

    # update user info
    sql = """
        update users_info
        set 
        username='{:s}', 
        fname='{:s}', 
        sname='{:s}', 
        gender='{:d}', 
        sex_preference='{:d}', 
        birth='{:s}', 
        phone='{:s}', 
        bio='{:s}' 
        where user_id={:d}
    """.format(username, fname, sname, gender, sex_preference, birth, phone, bio, user_id)
    db.request(sql)

    # interests per request
    interests = request.json['interests']
    split_interests = [x.strip('\'\" ') for x in interests.split(',')]
    split_interests = [x for x in split_interests if x]


    # update general interest table
    to_add_interests = []
    if split_interests:
        sql = "select * from interests where "
        add_or = ""
        for interest in split_interests:
            sql = sql + """
                {:s} interest='{:s}'
            """.format(add_or, interest)
            if not add_or:
                add_or = "OR"
        db.request(sql)

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
            sql = sql + "('" + to_add + "') "
            first = False
        db.request(sql, return_id_flag=False)

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
                {:s} interest='{:s}'
            """.format(add_or, interest)
            if not add_or:
                add_or = "OR"        
        db.request(sql)
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

    if not db.getError():
        success = 1

    return jsonify({'success': success, 'method': 'profile/update'})


@app.route("/profile/update_password", methods=['POST'])
def profile_update_password():
    success = 0
    result = []

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

    password = request.json['password']
    new_password  = request.json['new_password']
    repeate_password  = request.json['repeate_password']

    # if repeate password != new password - return immediately
    if new_password is not repeate_password:
        return jsonify({'success': success})

    # validate current password
    sql = """
        select * from users
        where id={:d} and password='{:s}'
    """.format(user_id, hasher.hash_string(password))
    db.request(sql)

    # return immediately if not validated
    if not db.getRowCount():
        return jsonify({'success': success})

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

    new_email = request.json['new_email']
    
    #check if email already exist
    sql = """
        select * from users where email='{:s}'
    """.format(new_email)
    db.request(sql)

    if db.getRowCount():
        # if email already exist - return immediately
        return jsonify({'success': success})

    # if hash for email update confirm fro current user already exist - delete it
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

    sql = "select * from email_update where email_hash='{:s}' and confirm_hash='{:s}';".format(email_hash, confirm_hash)
    db.request(sql)

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

    photo_value = base64.b64decode(request.json['photoValue'])
    photo_hash = hasher.generate_hash(32)
    photo_extention = 'jpeg'
    photo_path = '/vagrant/backend/data/photos'
    filesaver.save_file(value=photo_value, name=photo_hash, extention="jpeg", path=photo_path)


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
    sql = "update photos set avatar=1 where hash='{:s}'".format(photo_hash)
    db.request(sql)

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


    # get db
    db = shared.database()

    # actually delete photo
    photo_hash = request.json['photo_hash']
    sql = "delete from photos where user_id={:d} and hash='{:s}'".format(user_id, photo_hash)
    db.request(sql)

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

    # actually delete photo
    geo_type = int(request.json['geo_type'])

    sql = "update users_info set geo_type={:d} where user_id={:d}".format(geo_type, user_id)
    db.request(sql)

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

    # actually delete photo
    lat = float(request.json['lat'])
    lng = float(request.json['lng'])

    sql = "update users_info set geo_lat={:5.15f}, geo_lng={:5.15f} where user_id={:d}".format(lat, lng, user_id)
    db.request(sql)

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
    interests = request.json['interests']
    sort = request.json['sort']
    sort = sort.split('_')
    bottomAge = int(request.json['bottomAge'])
    upperAge = int(request.json['upperAge'])
    bottomRating = float(request.json['bottomRating'])
    upperRating = float(request.json['upperRating'])
    woman = request.json['woman']
    man = request.json['man']
    online = request.json['online']
    radius = float(request.json['radius'])
    offset = (int(request.json['page']) - 1) * 10

    split_interests = [x.strip('\'\" ') for x in interests.split(',')]
    split_interests = [x for x in split_interests if x]

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


    for_online_filter = """
        left join
        (select user_id, now()::timestamp - login.last_seen as seen_ago from login
        ) as online
        on users.id = online.user_id
    """



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
            where interests.interest in {:s}
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
        and users_info.geo_lat is not null
        and users_info.geo_lng is not null
        and distance < {:f}\n""".format(inline_interests, user_id, auth_user_info['geo_lat'], auth_user_info['geo_lat'], auth_user_info['geo_lng'], user_id, user_id, user_id, radius)

    if (man and not woman):
        sql = sql + '\t\tand users_info.gender=1\n'
    if (woman and not man):
        sql = sql + '\t\tand users_info.gender=2\n'

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

    vdf(sql, 'sql')

    filesaver = FileSaver()
    db.request(sql)
    if db.getRowCount() and not db.getError():
        result_array = db.getResult()
        vdf(result_array, 'result')
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
    mate_id = int(request.json['mate_id'])


    # get matched mates
    sql = """
        select users.*, users_info.*
        from users
        inner join users_info
        on users.id = users_info.user_id
        where users.id='{:d}'
    """.format(mate_id)

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
    """.format(mate_id)

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

    filesaver = FileSaver()
    sql = "select * from photos where user_id = {:d}".format(mate_id)
    db.request(sql)
    photos = []
    if db.getRowCount() and not db.getError():
        result_photos = db.getResult()
        for result_photo in result_photos:
            photos.append({'src': base64.b64encode(filesaver.read_file(result_photo['name'], '/vagrant/backend/data/photos')), 'avatar': result_photo['avatar']})
    elif not db.getError():
        success = 1
        return jsonify({'success': success, 'result': None})
    else:
        success = 0
        return jsonify({'success': success, 'result': None})

    result['photos'] = photos

    success = 1
    return jsonify({'success': success, 'method': 'explore/search_mates', 'result': result})


@app.route("/explore/like", methods=['POST'])
def like():
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


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1={:d}
        and user_id_2={:d}
    """.format(user_id, mate_id)

    # actions: 1 - like, 2 - dislike
    db.request(sql)
    if db.getRowCount():
        # just update action
        sql = 'update likes set action=1 where user_id_1={:d} and user_id_2={:d}'.format(user_id, mate_id)
        db.request(sql)
        success = 1
    else:
        sql = 'insert into likes (user_id_1, user_id_2, action) values ({:d}, {:d}, 1)'.format(user_id, mate_id)
        db.request(sql, False)
        success = 1

    return jsonify({'success': success, 'method': 'explore/like'})


@app.route("/explore/dislike", methods=['POST'])
def dislike():
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


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1={:d}
        and user_id_2={:d}
    """.format(user_id, mate_id)

    # actions: 1 - like, 2 - dislike
    db.request(sql)
    if db.getRowCount():
        # just update action
        sql = 'update likes set action=2 where user_id_1={:d} and user_id_2={:d}'.format(user_id, mate_id)
        db.request(sql)
        success = 1
    else:
        sql = 'insert into likes (user_id_1, user_id_2, action) values ({:d}, {:d}, 2)'.format(user_id, mate_id)
        db.request(sql, False)
        success = 1

    return jsonify({'success': success, 'method': 'explore/dislike'})


@app.route("/explore/unlike", methods=['POST'])
def unlike():
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


    mate_id = request.json['mate_id']

    # get db
    db = shared.database()

    # get authorized user_info
    sql = """
        select *
        from likes
        where user_id_1={:d}
        and user_id_2={:d}
    """.format(user_id, mate_id)

    # actions: 1 - like, 2 - dislike
    db.request(sql)
    if db.getRowCount():
        # just update action
        sql = 'delete from likes where user_id_1={:d} and user_id_2={:d}'.format(user_id, mate_id)
        db.request(sql)
        success = 1
    else:
        # nothing to unlike
        success = 1

    return jsonify({'success': success, 'method': 'explore/unlike'})



