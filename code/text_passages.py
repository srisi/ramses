from utilities import document_iterator, get_sides, print_highlight
from configuration import DB_PATH

import sqlite3
import re

RED = '\033[91m'

def get_text_passages(search_term, witness=None, scope=1, side_question=None, side_answer=None, type=None):

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    side_question, side_answer = get_sides(side_question, side_answer)

    docs = document_iterator(year_start=1990, year_end=2017, side_question=side_question, type=type,
                             search_term=search_term, format='text_passages')


    count = 0
    for doc in docs:
        count += 1
        date, text, doc_id, qas_id, last_name, first_name, historian_side = doc


        heading = u"Witness: {}, {} ({}). Date: {}. Document ID: {}".format(last_name, first_name, historian_side,
                                                                            date, doc_id)
        print_highlight(heading, heading, 'bold')

        cur.execute('''SELECT qas.text, qas.type FROM qas
                       WHERE qas.document = "{}" AND qas.id >= {} AND qas.id <= {};'''.format(doc_id, qas_id-scope,
                                                                                              qas_id+scope))
        rows = cur.fetchall()
        qas = u''
        for row in rows:
             qas += u"Type: {}.\t{}".format(row[1], row[0])

        print_highlight(qas, search_term)

    print "{} Documents".format(count)














if __name__ == "__main__":
    get_text_passages(search_term='quit ', scope=0, side_answer='Defendant', type='A')