

import sqlite3

from utilities import flexible_htm, mth, to_unicode

DB_PATH = '/home/stephan/tobacco/code/ramses/database/depo.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query(keyword = 'addic', side='Plaintiff', type='A',
          year_start=1987, year_end=2017, historian="Proctor"):



    con = sqlite3.connect(DB_PATH)
    con.row_factory = dict_factory
    cur = con.cursor()

    # access stores Datetime such that the last 3 digits are hour and minute -> multiply by 1000
    start_timestamp = flexible_htm('1/1/{}'.format(year_start)) * 1000
    end_timestamp = flexible_htm('1/1/{}'.format(year_end)) * 1000


    query = ['''SELECT  qas.id, qas.type, qas.text,
                        legal_document.id_doc, legal_document.date_doc, legal_document.type,
                        legal_document.side_question, legal_document.side_answer, legal_document.file_name,
                        historian.name_last, historian.name_first
                      FROM qas
                        JOIN legal_document on legal_document.file_name = qas.document
                        JOIN historian on legal_document.id_historian = historian.id_historian
                      WHERE legal_document.date_doc >= {}
                        and legal_document.date_doc <= {}'''.format(start_timestamp, end_timestamp)]

    if keyword:
        query += ['qas.text LIKE "%{}%"'.format(keyword)]

    if type:
        query += ['qas.type = "{}"'.format(type)]

    if side:
        if type:
            query += ['legal_document.side_question = "{}" '.format(side)]
        else:
            if side == 'Plaintiff':
                query += ['''(legal_document.side_question = "Plaintiff" AND qas.type = "Q") OR
                             (legal_document.side_answer = "Defendant" AND qas.type = "A")''']
            if side == 'Defendant':
                query += ['''(legal_document.side_question = "Defendant" AND qas.type = "Q") OR
                             (legal_document.side_answer = "Plaintiff" AND qas.type = "A")''']

    query = "\nAND ".join(query)


    print query 

    cur.execute(query)

    for row in cur.fetchall():
        print u"{}, {} ({}). {}. {}. \n{}".format(row['name_last'], row['name_first'], row['side_answer'],
                                          mth(row['date_doc'] /1000), row['type'], row['text'])

    # cur.execute('''SELECT * FROM qas
    #                   JOIN legal_document on legal_document.file_name = qas.document
    #                   JOIN historian on legal_document.id_historian = historian.id_historian
    #                   WHERE key)


def document_iterator(year_start=1940, year_end=2020, type = 'Q', side_question=None, side_answer=None):
    '''

    :param year_start:
    :param year_end:
    :param type: Q or A
    :param side_question: Defendant or Plaintiff
    :param side_answer: Defendant or Plaintiff
    :return:
    '''

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # access stores Datetime such that the last 3 digits are hour and minute -> multiply by 1000
    start_timestamp = flexible_htm('1/1/{}'.format(year_start)) * 1000
    end_timestamp = flexible_htm('1/1/{}'.format(year_end)) * 1000

    query = '''SELECT qas.text, legal_document.date_doc
                    FROM qas
                      JOIN legal_document on legal_document.file_name = qas.document'''

    if side_question:
        query += ''' WHERE legal_document.side_question = "{}" AND qas.type= "{}"'''.format(side_question, type)
    if side_answer:
        query += ''' WHERE legal_document.side_answer = "{}" AND qas.type= "{}"'''.format(side_answer, type)
    query += ''' AND legal_document.date_doc >= {} AND legal_document.date_doc <= {}
                 ORDER BY legal_document.date_doc ASC;'''.format(start_timestamp, end_timestamp)

    print query
    cur.execute(query)

    for document in cur.fetchall():

        date = mth(document[1]/1000)
        yield (date, document[0])


if __name__ == "__main__":
#    query()

    for i in document_iterator(type='Q', side_question='Defendant'):
        print i