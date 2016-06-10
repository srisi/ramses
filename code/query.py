

import sqlite3



def query(keyword = 'addic', side='Plaintiff', type='A',
          year_start=1950, year_end=2016, historian="Proctor"):



    db_path = '/home/stephan/tobacco/code/ramses/database/depo.db'
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = '''SELECT * FROM qas
                      JOIN legal_document on legal_document.file_name = qas.document
                      JOIN historian on legal_document.id_historian = historian.id_historian
                      WHERE legal_document. >= Datetime('2009-11-13 00:00:00')
  and mydate <= Datetime('2009-11-15 00:00:00')'''

    if keyword:
        query += ' qas.text LIKE "%{}%" AND'.format(keyword)

    if type:
        query += ' qas.type = "{}" AND'.format(type)

    if side:
        if type:
            query += ' legal_document.side_question = "{}" AND'.format(type)
        else:
            if side == 'Plaintiff':
                query += ''' (legal_document.side_question = "Plaintiff" AND qas.type = "Q") OR
                             (legal_document.side_answer = "Defendant" AND qas.type = "A") AND'''
            if side == 'Defendant':
                query += ''' (legal_document.side_question = "Defendant" AND qas.type = "Q") OR
                             (legal_document.side_answer = "Plaintiff" AND qas.type = "A") AND'''



    cur.execute('''SELECT * FROM qas
                      JOIN legal_document on legal_document.file_name = qas.document
                      JOIN historian on legal_document.id_historian = historian.id_historian
                      WHERE key)