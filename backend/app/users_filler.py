from shared import Mailer
from shared import Hasher
from shared import FileSaver
from shared import vdf
import base64
import os
import json
import shared
import urllib
from random import randint
import random

hasher = Hasher()


db = shared.database()
sql = 'select * from xlogins'
db.request(sql)
result = db.getResult()

for item in result:
	photo_hash = hasher.generate_hash(32)
	photo_name = photo_hash + '.jpeg'
	avatar = 1

	email = item['email']
	password = hasher.hash_string('1')
	confirmed = 1
	username = item['login']
	fname = item['first_name']
	sname = item['last_name']
	birth = "{:d}-{:02d}-{:02d}".format(randint(1920, 1999), randint(1, 12), randint(1, 28))
	gender = randint(1, 2)
	sex_preference = 2 if gender == 1 else 1
	phone = item['phone']
	bio = 'Here must be some text about me'
	geo_type = 2
	geo_lat = float(randint(50315498066384631,50521129770500394)) / float(1000000000000000)
	geo_lng = float(randint(30257072037908188,30676172560903183)) / float(1000000000000000)
	rating = float(randint(50,100)) / float(100)

	urllib.urlretrieve(item['image_url'], "/vagrant/backend/data/photos/" + photo_name)

	sql = "insert into users (email, password, confirmed) values ('{:s}', '{:s}', {:d}) returning id".format(email, password, confirmed)
	db.request(sql)
	user_id = db.getLastRowId()

	sql = """
		insert into users_info (user_id, username, fname, sname, birth, gender, sex_preference, phone, bio, geo_type, geo_lat, geo_lng, rating)
		values ({:d}, '{:s}', '{:s}', '{:s}', '{:s}', {:d}, {:d}, '{:s}', '{:s}', {:d}, {:5.15f}, {:5.15f}, {:1.15f}) returning id
		""".format(user_id, username, fname, sname, birth, gender, sex_preference, phone, bio, geo_type, geo_lat, geo_lng, rating)
	db.request(sql)

	sql = "insert into photos (user_id, name, hash, avatar) values ({:d}, '{:s}', '{:s}', {:d}) returning id".format(user_id, photo_name, photo_hash, avatar)
	db.request(sql)

	sample_interests = random.sample(range(1, 3014), 15)
	for sample_interest in sample_interests:
		sql = "insert into users_interests (user_id, interest_id) values ({:d}, {:d})".format(user_id, sample_interest)
		db.request(sql, False)

