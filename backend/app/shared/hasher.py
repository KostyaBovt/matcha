import random
import string
import hashlib

class Hasher(object):

	def __init__(self):
		pass

	def generate_hash(self, len):
		return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(len)])

	def hash_string(self, str):
		return hashlib.md5(str).hexdigest()
