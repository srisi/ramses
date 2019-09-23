from utilities import document_iterator, get_sides, print_highlight
from configuration import DB_PATH

from collections import Counter, OrderedDict

import csv
import codecs
import cStringIO

import sqlite3
import re

RED = '\033[91m'

def get_text_passages(search_term, historian_name_last=None, scope=1, side_question=None, side_answer=None, type=None,
                      year_start=1990, year_end=2017, document_type=None):

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    side_question, side_answer = get_sides(side_question, side_answer)

    docs = document_iterator(year_start=year_start, year_end=year_end, side_question=side_question, type=type,
                             search_term=search_term, format='text_passages', historian_name_last=historian_name_last,
                             document_type=document_type)

    doc_list = []
    years = {i:0 for i in range(year_start,year_end+1)}
    witnesses = Counter()
    count = 0
    for doc in docs:
        count += 1
        date, text, doc_id, qas_id, last_name, first_name, historian_side = doc

        witnesses[u'{},{}'.format(last_name, first_name)] += 1
        years[int(date[:4])] += 1

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

            doc_list.append({
                'witness': u'{}, {}'.format(last_name, first_name),
                'doc_id': doc_id,
                'date': date,
                'year': int(date[:4]),
                'type': row[1],
                'text': row[0]
            })


        print_highlight(qas, search_term)




    print "{} Documents".format(count)

    return doc_list, years, witnesses

def store_as_csv(doc_list, years, witnesses, search_term, type, side_answer):

    if not type:
        type = "None"

    if not side_answer:
        side_answer = 'None'

    year_dates =  [i[0] for i in sorted(years.items())]
    year_values = [i[1] for i in sorted(years.items())]

    witness_names = [i[0] for i in sorted(witnesses.items())]
    witness_values = [i[1] for i in sorted(witnesses.items())]

    csvfile = open('../csv/{}_{}.csv'.format(search_term, type), 'w')

    csv_writer = UnicodeWriter(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

    csv_writer.writerow(["Term", "Q or A", "Side Witness"])
    print [search_term, type, side_answer]
    csv_writer.writerow([search_term, type, side_answer])

    csv_writer.writerow([''])
    csv_writer.writerow(['Years'])

    for i in range(len(year_dates)):
        csv_writer.writerow([str(year_dates[i]), str(year_values[i])])

    csv_writer.writerow([''])

    csv_writer.writerow(["Witnesses"])
    for i in range(len(witness_names)):
        csv_writer.writerow([witness_names[i], str(witness_values[i])])

    csv_writer.writerow([''])

    csv_writer.writerow(["Documents"])
    csv_writer.writerow(['Year', 'Date', 'Witness', 'Doc ID', 'Type', 'Text'])

    print doc_list
    for i in doc_list:
        csv_writer.writerow([str(i['year']), i['date'], i['witness'], i['doc_id'], i['type'], i['text']])

    csvfile.close()


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)









#Predictors for Defendants:
#[(u'various types', -105.8601311706164), (u'engaged', -102.03621957206748), (u'say cigarette', -80.960436279485137), (u'didn think', -72.090462869000959), (u'know don', -69.188901028380286), (u'smoke cigarettes', -65.538780551048575), (u'brought forth', -62.409800103414938), (u'diseases lung', -61.293895739940588), (u'building', -61.169605725794327), (u'bear', -60.569944871095551)]

#Predictors for Plaintiffs:
#[(u'cancer causes', 87.569150368627845), (u'accusation', 63.604816718896608), (u'smoking causes lung', 63.002003749780755), (u'highly', 62.090345449241447), (u'add', 61.8085092352716), (u'epidemiological study', 61.417806385265251), (u'hold', 60.99331488543902), (u'count', 59.624903729424553), (u'general population', 57.735014532335477), (u'15', 57.415970953575481)]



if __name__ == "__main__":
#    get_text_passages(search_term='various', scope=0, side_answer='Plaintiff', type='A')

    search_term = 'selikoff'
    type='A'

    doc_list, years, witnesses = get_text_passages(search_term=search_term, scope=0, side_question='Defendant', type=type,
                      year_start=1987, year_end=2017, historian_name_last='Cobbs-Hoffman', document_type='TEC')

    store_as_csv(doc_list, years, witnesses, search_term, type, side_answer='Plaintiff')
