# -*- coding: utf-8 -*-

import re
import sqlite3
import codecs
import os


EXCLUDED = set('le_qzxb0089.txt')

#qzxb0089 ends with the line (Deposition concluded.)

def preprocess(path, file):

    with codecs.open(path + file,'r',encoding='utf8') as f:
        text = f.read()

    text = text.replace(u"THE WITNESS", u"A. ")


    if file.startswith('wl'):
        # as long as there are still copyright marks, eliminate them.
        while text.find(u'©') > -1:
            copyright_pos = text.find(u'©')
            first_line_pos = text.find(u'\n', copyright_pos)
            second_line_pos = text.find(u'\n', first_line_pos+1)

            text = text[:copyright_pos - 1] + text[second_line_pos:]

        # not sure anymore what this was about...
        text = text.replace(u"ject to form. ", u"ject to form.\n")

    if file.startswith('le'):
        text = text
        text = re.sub('\x0c', '', text, flags=re.MULTILINE)
        text = re.sub('^\x0c?[0-9]+[\t ]+[0-9]?', '', text, flags=re.MULTILINE)

        text = re.sub('Q*( |\t)', '', text, flags=re.MULTILINE)
        text = re.sub('q.( |\t)', '', text, flags=re.MULTILINE)
        text = re.sub('Q,( |\t)', '', text, flags=re.MULTILINE)
        text = re.sub('A*( |\t)', '', text, flags=re.MULTILINE)
        text = re.sub('A,( |\t)', '', text, flags=re.MULTILINE)

        #print text
#    if file.startswith('le'):



    return text


def extract_questions_answers(text):


    # Split up questions and answers
    qas_raw = [m for m in re.finditer(r'^ ?(Q|A)(\.|:)? (.+?)(?=^Q|^A|^MS.|^MR.|^BY )',
                         text, re.MULTILINE | re.DOTALL)]
    qas_raw = [m for m in re.finditer(r'^ ?(Q|A)(\.|:)?( |\t)(.+?)(?=^Q|^A|^MS.|^MR.|^BY )',
                         text, re.MULTILINE | re.DOTALL)]

    # add all to a list with start and end position
    qas = []
    for qa in qas_raw:
        qas.append({
            'type': text[qa.start(1): qa.end(1)],
            'text': text[qa.start(0): qa.end(0)],
            'position': qa.span(0)
        })

    # If 2 questions or 2 answers follow one another, merge the text in-between
    merged_qas = []
    i = 0
    while i < len(qas) - 2:
        # if answer follows question or vice versa (normal case)
        if qas[i]['type'] != qas[i+1]['type']:
            merged_qas.append(qas[i])
            i += 1

        # if 2 answers or questions follow one another
        if qas[i]['type'] == qas[i+1]['type']:

            qa_text_start = qas[i]['position'][0]
            qa_text_end = qas[i]['position'][1]
            skipped = 1
            while True:
                try:
                    if qas[i]['type'] == qas[i+skipped]['type']:
                        qa_text_end = qas[i+skipped]['position'][1]
                        skipped += 1
                    else:
                        break
                except IndexError:
                    break

            skipped -= 1

            merged_qas.append({
                'type': qas[i]['type'],
                'text': text[qa_text_start:qa_text_end],
                'position': (qa_text_start, qa_text_end)
            })


            i += skipped + 1

    # counts for number of questions and answers as well as longest qa.
    qu = 0
    an = 0
    longest_qa = 0
    longest_qa_i = 0
    for i in range(len(merged_qas)):
        if merged_qas[i]['type'] == 'Q': qu +=1
        if merged_qas[i]['type'] == 'A': an += 1

        if len(merged_qas[i]['text']) > longest_qa:
            longest_qa = len(merged_qas[i]['text'])
            longest_qa_i = i

    print qu, an
    print merged_qas[longest_qa_i]['text']

    print repr(merged_qas[longest_qa_i]['text'])


    return merged_qas


def add_to_database(file, qas):

    db_path = '../database/depo.db'
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS qas(

                    document    text NOT NULL,
                    id          integer NOT NULL,

                    type        text NOT NULL,
                    text        text NOT NULL,
                    pos_start   integer NOT NULL,
                    pos_end     integer NOT NULL,

                    UNIQUE(document, id) ON CONFLICT REPLACE);
    ''')

    insert_list = []
    for id, qa in enumerate(qas):
        insert_list.append((
            file[:-4]+'.pdf', id,
            qa['type'], qa['text'], qa['position'][0], qa['position'][1]
        ))

    cur.executemany('''INSERT OR IGNORE INTO qas(
                        document, id,
                        type, text, pos_start, pos_end)
                        VALUES(?, ?, ?, ?, ?, ?);''',
                    insert_list)

    con.commit()

def add_all_westlaw():

    path = '/home/stephan/Dropbox/Risi/txt/'
    path = '/Users/stephan/Dropbox/Risi/txt/'

    for file in os.listdir(path):

        if file in EXCLUDED: continue

        if file.startswith("wl_") and file.endswith(".txt"):
            continue
            print file
            text = preprocess(path, file)
            qas = extract_questions_answers(text)

            add_to_database(file, qas)

        if file.startswith("le_") and file.endswith(".txt"):
            print file
            text = preprocess(path, file)
            qas = extract_questions_answers(text)


if __name__ == "__main__":

    # path = '/home/stephan/Dropbox/Risi/txt/'
    # file = 'wl_5061522.txt'
    #
    # text = preprocess(path, file)
    # qas = extract_questions_answers(text)
    #
    # add_to_database(file, qas)

    add_all_westlaw()
