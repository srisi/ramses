import sqlite3

from datetime import datetime

from configuration import DB_PATH


con = sqlite3.connect(DB_PATH)
cur = con.cursor()

query = '''SELECT legal_document.id_doc, legal_document.date_doc
                FROM legal_document WHERE legal_document.date_doc LIKE "%/%"'''

cur.execute(query)

update_list = []

for doc in cur.fetchall():
    # calculate epoch time from string with %d/%m/%Y %H:%M:%S format
    timestamp = int((datetime.strptime(doc[1], '%d/%m/%Y %H:%M:%S') - datetime.utcfromtimestamp(0)).total_seconds() * 1000)

    update_list.append((timestamp, doc[0]))

cur.executemany('''UPDATE legal_document
                   SET date_doc = ?
                   WHERE id_doc = ?;''',
                update_list
)
con.commit()

print 'updated %s dates' % len(update_list)
