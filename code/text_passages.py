from utilities import document_iterator, get_sides, print_highlight
from configuration import DB_PATH

import sqlite3
import re

RED = '\033[91m'

def get_text_passages(search_term, historian_name_last=None, scope=1, side_question=None, side_answer=None, type=None,
                      year_start=1990, year_end=2017):

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    side_question, side_answer = get_sides(side_question, side_answer)

    docs = document_iterator(year_start=year_start, year_end=year_end, side_question=side_question, type=type,
                             search_term=search_term, format='text_passages', historian_name_last=historian_name_last)

#    dates={year:0 for }
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



#Predictors for Defendants:
#[(u'various types', -105.8601311706164), (u'engaged', -102.03621957206748), (u'say cigarette', -80.960436279485137), (u'didn think', -72.090462869000959), (u'know don', -69.188901028380286), (u'smoke cigarettes', -65.538780551048575), (u'brought forth', -62.409800103414938), (u'diseases lung', -61.293895739940588), (u'building', -61.169605725794327), (u'bear', -60.569944871095551)]

#Predictors for Plaintiffs:
#[(u'cancer causes', 87.569150368627845), (u'accusation', 63.604816718896608), (u'smoking causes lung', 63.002003749780755), (u'highly', 62.090345449241447), (u'add', 61.8085092352716), (u'epidemiological study', 61.417806385265251), (u'hold', 60.99331488543902), (u'count', 59.624903729424553), (u'general population', 57.735014532335477), (u'15', 57.415970953575481)]



if __name__ == "__main__":
#    get_text_passages(search_term='various', scope=0, side_answer='Plaintiff', type='A')
    get_text_passages(search_term='Proctor', scope=0, side_answer='Defendant',
                      year_start=2000, year_end=2017)