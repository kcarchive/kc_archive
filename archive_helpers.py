from flask import Flask, render_template, request
import mysql.connector
import html

class connectMysql:
	mydb = None
	mycursor = None

	def disconnect(self):
		self.mycursor.close()
		self.mydb.close()
		self.mycursor = None
		self.mydb = None

	def connect(self):
		self.mydb = mysql.connector.connect(
			host='[HOST]',
			user='[USER]',
			passwd='[PASSWORD]',
			database='[DATABASE]',
			charset='utf8mb4'
			#auth_plugin='mysql_native_password'
		)
		self.mycursor = self.mydb.cursor()


	def execute(self, SQLstring, SQLtuple):
		try:
			self.mycursor.execute(SQLstring, SQLtuple)
		except:
			self.disconnect()
			return

	def fetch(self):
		try:
			return self.mycursor.fetchall()
		except:
			self.disconnect()
			return

def renderError(error_message):
	return render_template('error.html', error=error_message)

def assembleSql(myDict):
	sql = 'SELECT * FROM posts WHERE 1' # string of the main SQL query
	sqlVarsList = [] # these will replace %s's in the query

	for k,v in myDict.items():
		if k == 'string':
			sql += ' AND MESSAGE LIKE %s'
			sqlVarsList.append('%' + v + '%')
		if k == 'country':
			sql += ' AND COUNTRY = %s'
			sqlVarsList.append(v)
		if k == 'subject':
			sql += ' AND SUBJECT LIKE %s'
			sqlVarsList.append('%' + v + '%')
		if k == 'name':
			sql += ' AND NAME LIKE %s'
			sqlVarsList.append('%' + v + '%')
		if k == 'postID':
			sql += ' AND POST_ID = %s'
			sqlVarsList.append(v)
		if k == 'threadID':
			sql += ' AND THREAD_ID = %s'
			sqlVarsList.append(v)
		if k == 'filename':
			sql += ' AND (FILE1 LIKE %s OR FILE2 LIKE %s OR FILE3 LIKE %s OR FILE4 LIKE %s)'
			sqlVarsList.append('%' + v + '%')
			sqlVarsList.append('%' + v + '%')
			sqlVarsList.append('%' + v + '%')
			sqlVarsList.append('%' + v + '%')
		if k == 'day':
			sql += ' AND DAYOFMONTH(DATE_CREATED) = %s'
			sqlVarsList.append(v)
		if k == 'month':
			sql += ' AND MONTH(DATE_CREATED) = %s'
			sqlVarsList.append(v)
		if k == 'year':
			sql += ' AND YEAR(DATE_CREATED) = %s'
			sqlVarsList.append(v)
		if k == 'page':
			sql += ' ORDER BY DATE_CREATED DESC LIMIT 150 OFFSET %s'
			sqlVarsList.append(v * 150)

	sqlVars = tuple(sqlVarsList)
	return (sql, sqlVars)

def collectData():
	dataDict = {
		'string': '',
		'day': 0,
		'month': 0,
		'year': 0,
		'country': '',
		'subject': '',
		'name': '',
		'postID': 0,
		'threadID': 0,
		'filename': '',
		'page': 0
	}

	# get data from the forms; pls dont bully for searchString
	searchString = request.args.get('string')
	if searchString:
		searchString = searchString.replace('&', '&amp;').replace('\'', '&apos;').replace('>', '&gt;').replace('<', '&lt;').replace('"', '&quot;')
	dateDay = request.args.get('day') #int
	dateMonth = request.args.get('month') #int
	dateYear =  request.args.get('year') #int
	countryball = request.args.get('country') #string
	subject = request.args.get('subject') #string
	name = request.args.get('postName') #string
	postID = request.args.get('postID') #int
	threadID = request.args.get('threadID') #int
	filename = request.args.get('filename') #string
	page = request.args.get('page')


	# MESSAGE
	if searchString:
		dataDict['string'] = searchString
	else:
		dataDict.pop('string')

	# DAY
	if dateDay:
		if dateDay.isdecimal() and int(dateDay) <= 31 and int(dateDay) >= 1:
			dataDict['day'] = int(dateDay)
		else:
			return '[Day] field should only contain numerals 1-31, or nothing at all.'
	else:
		dataDict.pop('day')

	# MONTH
	if dateMonth:
		if dateMonth.isdecimal() and int(dateMonth) <= 12 and int(dateMonth) >= 1:
			dataDict['month'] = int(dateMonth)
		else:
			return '[Month] field should only contain numerals 1-12, or nothing at all.'
	else:
		dataDict.pop('month')

	# YEAR
	if dateYear:
		if dateYear.isdecimal():
			dataDict['year'] = int(dateYear)
		else:
			return '[Year] field should only contain numerals, or nothing at all.'
	else:
		dataDict.pop('year')

	# COUNTRY
	if countryball:
		dataDict['country'] = countryball
	else:
		dataDict.pop('country')

	# SUBJECT
	if subject:
		dataDict['subject'] = subject
	else:
		dataDict.pop('subject')

	# NAME
	if name:
		dataDict['name'] = name
	else:
		dataDict.pop('name')

	# POST_ID
	if postID:
		if postID.isdecimal():
			dataDict['postID'] = int(postID)
		else:
			return '[postID] field should only contain numerals, or nothing at all.'
	else:
		dataDict.pop('postID')

	# THREAD_ID
	if threadID:
		if threadID.isdecimal():
			dataDict['threadID'] = int(threadID)
		else:
			return '[threadID] field should only contain numerals, or nothing at all.'
	else:
		dataDict.pop('threadID')

	if filename:
		dataDict['filename'] = filename
	else:
		dataDict.pop('filename')

	if page and page.isdecimal():
		dataDict['page'] = int(page)

	return dataDict
