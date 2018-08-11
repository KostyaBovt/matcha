import psycopg2
import psycopg2.extras
import psycopg2.extensions

from debug import vdf

class database(object):
	_result = None
	_error = False
	_rowCount = 0
	_command = None
	_lastRowId = None

	def __init__(self):
		pass

	def request(self, request, return_id_flag=True):
		self._result = None
		self._error = False
		self._rowCount = 0
		self._lastRowId = None
		self._command = request.split()[0].lower()

		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

		conn = psycopg2.connect("dbname=matcha user=vagrant");
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		cur.execute(request)
		conn.commit()

		forLastRowId = ['insert']
		forRowCount = ['select', 'update', 'insert']
		forFetch = ['select']

		if (self._command in forFetch):
			self._result = cur.fetchall()

		if (self._command in forRowCount):
			self._rowCount = cur.rowcount

		if (self._command in forLastRowId and return_id_flag):
			self._lastRowId = cur.fetchone()['id']

		cur.close()
		conn.close()

	def request2(self, request, args, return_id_flag=True):
		self._result = None
		self._error = False
		self._rowCount = 0
		self._lastRowId = None
		self._command = request.split()[0].lower()

		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

		conn = psycopg2.connect("dbname=matcha user=vagrant");
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		cur.execute(request, args)
		conn.commit()

		forLastRowId = ['insert']
		forRowCount = ['select', 'update', 'insert']
		forFetch = ['select']

		if (self._command in forFetch):
			self._result = cur.fetchall()

		if (self._command in forRowCount):
			self._rowCount = cur.rowcount

		if (self._command in forLastRowId and return_id_flag):
			self._lastRowId = cur.fetchone()['id']

		cur.close()
		conn.close()

	def getResult(self):
		return self._result

	def getError(self):
		return self._error

	def getRowCount(self):
		return self._rowCount

	def getLastRowId(self):
		return self._lastRowId

