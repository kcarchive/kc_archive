from flask import Flask, render_template, request, send_from_directory
from archive_helpers import connectMysql, renderError, assembleSql, collectData

app = Flask(__name__)

#only flask functions here
@app.route('/robots.txt')
def serve_robot_overlords():
	return send_from_directory(app.static_folder, 'robots.txt')

@app.errorhandler(500)
def internal_server_error(e):
	return renderError('Error 500: Whoopsie. I screwed something up.'), 500

@app.errorhandler(404)
def page_not_found(e):
	return renderError('Error 404: Page doesn\'t exist.'), 404

@app.route('/')
def kcsearch():
	return render_template('search.html')
		
@app.route('/result')
def result():
	result = collectData()  # on success of collectData(), result is dict
							# containing all search data provided

	if type(result) == str: # on failure of collectData(), result is str
		return renderError(result)

	if len(result) < 2:
		return renderError('No search criteria provided.')

	sqlReady = assembleSql(result) # sql query at [0] and variables at [1]
	mysqlObj = connectMysql()
	try:
	    mysqlObj.connect()
	except:
		return renderError('Error connecting to the database.')
	mysqlObj.execute(sqlReady[0], sqlReady[1])
	rows = mysqlObj.fetch()
	mysqlObj.disconnect()

	# this is some serious scotch tape fix; needs rewrite soon
	pageData = request.url.split('page=')
	if len(pageData) != 2:
		pageData = [request.url + '&', '0']

	return render_template('search_result.html', data=rows, currentUrl=pageData[0], pageNumber=pageData[1])
	


@app.route('/int/res/<THREAD_ID>.html')
def show_post(THREAD_ID):
	if THREAD_ID.isdecimal() is False:
		return renderError('Bad link. Protip: use it like so /int/res/[thread id].html')

	mysqlObj = connectMysql()
	try:
		mysqlObj.connect()
	except:
		return renderError('Error connecting to the database.')

	# op
	sql = 'SELECT * FROM posts WHERE THREAD_ID = %s AND THREAD_ID = POST_ID'
	mysqlObj.execute(sql, (THREAD_ID,))
	opRow = mysqlObj.fetch()

	# posts
	sql = 'SELECT * FROM posts WHERE THREAD_ID = %s AND THREAD_ID <> POST_ID ORDER BY DATE_CREATED ASC'
	mysqlObj.execute(sql, (THREAD_ID,))
	postRows = mysqlObj.fetch()
	mysqlObj.disconnect()

	if len(opRow) == 0:	
		return renderError('No such thread was found.')

	return render_template('thread.html', op=opRow, posts=postRows)


@app.route('/whatthefuck')
def about():
	return render_template('whatthefuck.html')


if __name__=='__main__':
	app.run(host="0.0.0.0", port=int("80"), debug=True)