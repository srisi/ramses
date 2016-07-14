# -*- coding: utf-8 -*-

import re
import sqlite3
import codecs
import os

import time

from configuration import TXT_PATH, DB_PATH


EXCLUDED = {'le_qzxb0089.txt',
               'le_lylk0191.txt',   # incorrect spaces
               'le_jtnl0001.txt',   # bad OCR
               'le_shlj0015.txt',   # bad OCR
        }

WORKING = {
    'le_ejs07a00.txt',
    'le_fmlk0191.txt',
    'le_fpkl0190.txt',
    'le_frxd0001.txt',
    'le_gllk0191.txt',
    'le_gmlk0191.txt',
    'le_grxd0001.txt',
    'le_hgdy0019.txt',
    'le_hhlk0191.txt',
    'le_hknc0093.txt',
    'le_hllk0191.txt',
    'le_hmlk0191.txt',
    'le_hplj0015.txt',
    'le_hsvj0223.txt',
    'le_hylk0191.txt',
    'le_hzfj0223.txt',
    'le_jhtl0001.txt',
    'le_jllk0191.txt',
    'le_jmgf0028.txt',
    'le_jqlc0093.txt',
    'le_kfll0190.txt',
    'le_kllk0191.txt',
    'le_kqkl0190.txt',
    'le_kqlc0093.txt',
    'le_kylk0191.txt',
    'le_ljml0190.txt',
    'le_lkml0191.txt',
    'le_lkml0190.txt',
    'le_lpkl0190.txt',
    'le_lqlc0093.txt',
    'le_mhlk0191.txt',
    'le_mllk0191.txt',
    'le_mmlk0191.txt',
    'le_mqlc0093.txt',
    'le_mtvj0223.txt',
    'le_mykk0191.txt',
    'le_nflk0191.txt',
    'le_npvj0223.txt',
    'le_nylk0191.txt',
    'le_pflk0191.txt',
    'le_phlk0191.txt',
    'le_pllk0191.txt',
    'le_pmlk0191.txt',
    'le_pzxb0089.txt',
    'le_pylk0191.txt',
    'le_qflw0221.txt',
    'le_qllk0191.txt',
    'le_qtkk0191.txt',
    'le_rhlj0015.txt',
    'le_rlkp0018.txt',
    'le_rpfd0086.txt',
    'le_smlk0191.txt',
    'le_sznl0083.txt',
    'le_tllk0191.txt',
    'le_tndy0019.txt',
    'le_xllk0191.txt',
    'le_xmlk0191.txt',
    'le_xplw0221.txt',
    'le_xqgf0028.txt',
    'le_xxhl0190.txt',
    'le_yflk0191.txt',
    'le_ykml0190.txt',
    'le_zfxd0001.txt',
    'le_zllk0191.txt',
    'le_zmlk0191.txt',
    'le_zndy0019.txt',

    'wl_1371239.txt',
    'wl_3000717.txt',
    'wl_3450318.txt',
    'wl_4062242.txt',
    'wl_4062274.txt',
    'wl_5061522.txt',
    'wl_5133569.txt',
    'wl_5438004.txt',
    'wl_5487028.txt',
    'wl_5580439.txt',
    'wl_5882553.txt',
    'wl_6320166.txt',
    'wl_6511228.txt',
    'wl_6512412.txt',
    'wl_6537151.txt',
    'wl_6537162.txt',
    'wl_6666232.txt',
    'wl_6768206.txt',
    'wl_7237080.txt',
    'wl_7757499.txt',
    'wl_8042643.txt',
    'wl_11685904.txt',
    'wl_11685905.txt',
    'wl_25967718.txt',
    'wl_34425546.txt',
    'wl_34428170.txt',
    'wl_34428171.txt',
    'wl_34667222.txt',
    'wl_34662921.txt',
    'wl_34663497.txt',
    'wl_34665268.txt',
    'wl_34672161.txt',
    'wl_34673167.txt',
    'wl_34872139.txt',
    'wl_34935827.txt',
    'wl_35271772.txt',
    'wl_35271782.txt',
    'wl_35273084.txt',
    'wl_35642155.txt',
    'wl_35639702.txt',
    'wl_35639703.txt',
    'wl_35717504.txt',

    'sp_01092010.txt',
    'sp_02102008.txt',
    'sp_02062010.txt',
    'sp_02082011.txt',
    'sp_06102010.txt',
    'sp_18122012.txt',
    'sp_19082009.txt',
    'sp_27022013.txt',


            }

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

    if file.startswith('le') or file.startswith('sp'):
        text = text

        # remove page breaks
        text = re.sub('\x0c', '', text, flags=re.MULTILINE)
        # remove leading numbers
        text = re.sub('^\x0c?[0-9]+[\t ]+[0-9]?', '', text, flags=re.MULTILINE)

        # change false Q. and A.
        text = re.sub('Q\*( |\t)', 'Q. ', text, flags=re.MULTILINE)
        text = re.sub('Q,( |\t)', 'Q. ', text, flags=re.MULTILINE)
        text = re.sub('q(\.|,)( |\t)', 'Q. ', text, flags=re.MULTILINE)

        text = re.sub('A\*( |\t)', 'A. ', text, flags=re.MULTILINE)
        text = re.sub('A,( |\t)', 'A. ', text, flags=re.MULTILINE)
        text = re.sub('a(\.,)( |\t)', 'A. ', text, flags=re.MULTILINE)

        # 8 misinterpreted as B, 0 as Q
        text = re.sub('B\t0\. ', 'Q. ', text, flags=re.MULTILINE)

        # Eliminate everything after witness is excused
        text = re.sub('(\(Witness excused.\)|REPORTER\'S CERTI FI CATE|\(The deposition concluded|Deposition adjourned|the videographer: we\'re now going off|\(Whereupon, the deposition continued in Volume|Deposition concluded|Signature of the Witness|THE VIDEOGRAPHER: There being no further questions, we\'re concluded,|I, JULIE I\. UPTON, a Certified Shorthand Reporter|\(Proceedings continued in Volume 24.\)).*', '', text, flags=re.MULTILINE|re.DOTALL)

        # Delete text at the end of every page
        # leZzfxd0001.txt
        text = re.sub('Brinkman Court Reporting, Inc\.\nDogwood Drive, Bozeman, MT 59718 \(406\) 585-0078\nDr\. Joan Hoff \-', '', text, flags=re.MULTILINE)

        if file.startswith('sp'):

            # remove lines that consist only of numbers
            text = re.sub('^[0-9]+\n', '', text, flags=re.MULTILINE)

            text = re.sub('^A\.?\n', 'A. ', text, flags=re.MULTILINE)
            text = re.sub('^Q\.?\n', 'Q. ', text, flags=re.MULTILINE)

            # remove tags by reporting companies
            text = re.sub('^www.phippsreporting.com\n11-34083533\n', '', text, flags=re.MULTILINE)
            text = re.sub('^\(212\) 279-9424\nVERITEXT REPORTING COMPANY\nwww.veritext.com\n\(212\) 490-34301', '', text, flags=re.MULTILINE)
            text = re.sub('^Veritext Florida Reporting Co\.\n800-726-7007\n305-376-8800Page [0-9]+\n', '', text, flags=re.MULTILINE)
            text = re.sub('^www.phippsreporting.com\n11-340863\n', '', text, flags=re.MULTILINE)
            text = re.sub('^United Reporting, Inc\n954-525-2221Page [0-9]+\n', '', text, flags=re.MULTILINE)



        # ocr was, in the end, too bad to use this document
        if file.startswith('le_jtnl0001.txt'):
            text = text[text.find('I STEPHEN E. AMBROSE. Ph.D. - EX. BY MR. MIKHAIL !	STIPULATION ,	- .. :'):]

        if file.startswith('le_hhlk0191.txt'):
            text = re.sub('^(\.|!|L) ?[0-9]+( |\t)', '', text, flags=re.MULTILINE)

            text = re.sub('O\.( |\t)', 'Q. ', text, flags=re.MULTILINE)

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

   # print repr(merged_qas[longest_qa_i]['text'])


    return merged_qas

def create_db_table():

    con = sqlite3.connect(DB_PATH)
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



def add_to_database(file, qas):

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

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

def add_all_documents_to_db():


    create_db_table()

    path = TXT_PATH

    for file in os.listdir(path):

        if file in EXCLUDED: continue
        #if file in WORKING: continue
        if not file.endswith('.txt'): continue

        if file.startswith('sp'): continue

        print file
        text = preprocess(path, file)

        qas = extract_questions_answers(text)
       # add_to_database(file, qas)




if __name__ == "__main__":

    # path = '/home/stephan/Dropbox/Risi/txt/'
    # file = 'wl_5061522.txt'
    #
    # text = preprocess(path, file)
    # qas = extract_questions_answers(text)
    #
    # add_to_database(file, qas)

    add_all_documents_to_db()
