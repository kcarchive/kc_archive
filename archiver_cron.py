#!/usr/bin/python3.7

# this is basically a one big hack that barely works, but somehow does
# with barely any exception handling

import mysql.connector
import json
from urllib.request import urlopen
from dateutil.parser import parse
import sys

mydb = mysql.connector.connect(
    host='[HOST]',
    user='[USERNAME]',
    passwd='[PASSWORD]',
    database='[DATABASE',
    charset='utf8mb4',
    connection_timeout=250
)
mycursor = mydb.cursor()

def catalog():
	try:
		with urlopen('https://kohlchan.net/int/catalog.json') as res:
			source = res.read()
	except:
		mycursor.close()
		mydb.close()
		print('ERROR FETCHING CATALOG')
		sys.exit(3)

	data = json.loads(source)
	a = list()
	for dat in data:
		a.append(dat['threadId'])
	return a



threads = catalog()


for thread in threads[:30]:
    try:
        with urlopen('https://kohlchan.net/int/res/' + str(thread) + '.json') as res:
            source = res.read()
    except:
        try:
            with urlopen('https://kohlchan.net/int/res/' + str(thread) + '.json') as res:
                source = res.read()
        except:
    	    print('thread ' + str(thread) + ' probably diedededed')
    	    continue

    data = json.loads(source)

    filezp = [''] * 4

    iterator = 0
    for file in data['files']:
        filezp[iterator] = file['originalName']
        iterator += 1

    threadIds = str(data['threadId'])

    #OP ==========================================================================================================

    datep = parse(data['creation']).strftime("%Y-%m-%d %H:%M:%S")

    sql = 'INSERT IGNORE INTO posts (THREAD_ID, POST_ID, COUNTRYBALL, MESSAGE, NAME, DATE_CREATED, SUBJECT, FILE1, FILE2, FILE3, FILE4, COUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (
            str(data['threadId']),
            str(data['threadId']),
            str(data['flag']),
            str(data['markdown']),
            str(data['name']),
            datep,
            str(data['subject']),
            filezp[0],
            filezp[1],
            filezp[2],
            filezp[3],
            str(data['flagName'])
    )
    try:
        mycursor.execute(sql, val)
    except:
        mycursor.close()
        mydb.close()
        print('ERROR EXECUTING. SHUTTING IT DOWN')
        sys.exit(1)

	# POSTS ================================================================================================
    for post in data['posts']:
        date = parse(post['creation']).strftime("%Y-%m-%d %H:%M:%S")

        filez = [''] * 4
        if post['message'][-8:] == '[b]\n[/b]':
            post['markdown'] = '<p style="color: grey">[message not archived as per request of the poster]</p>'
            print('opt-out detected in thread ' + str(data['threadID']))

        iterator = 0
        for file in post['files']:
            filez[iterator] = file['originalName']
            iterator += 1

        sql = 'INSERT IGNORE INTO posts (THREAD_ID, POST_ID, COUNTRYBALL, MESSAGE, NAME, DATE_CREATED, SUBJECT, FILE1, FILE2, FILE3, FILE4, COUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (
                threadIds,
                str(post['postId']),
                str(post['flag']),
                str(post['markdown']),
                str(post['name']),
                date,
                str(post['subject']),
                filez[0],
                filez[1],
                filez[2],
                filez[3],
                str(post['flagName'])
        )
        try:
            mycursor.execute(sql, val)
        except:
            mycursor.close()
            mydb.close()
            print('ERROR EXECUTING. SHUTTING IT DOWN')
            sys.exit(2)



try:
    mydb.commit()
except:
    mycursor.close()
    mydb.close()
    print('ERROR COMMITTING. SHUTTING IT DOWN')
    sys.exit(3)

mycursor.close()
mydb.close()
mycursor = None
mydb = None
