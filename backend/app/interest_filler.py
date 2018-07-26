import shared
import random

db = shared.database()
sql = 'select * from users;'
db.request(sql)
result = db.getResult()

for item in result:
	user_id = item['id']

	sample_interests = random.sample(range(3015, 3115), 15)
	for sample_interest in sample_interests:
		sql = "insert into users_interests (user_id, interest_id) values ({:d}, {:d})".format(user_id, sample_interest)
		db.request(sql, False)