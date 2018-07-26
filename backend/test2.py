from random import randint

for k in range(1, 30):
	geo_lat = float(randint(50315498066384631,50521129770500394)) / float(1000000000000000)
	geo_lng = float(randint(30257072037908188,30676172560903183)) / float(1000000000000000)

	print geo_lat
	print geo_lng
	print