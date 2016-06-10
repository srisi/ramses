# -*- coding: utf-8 -*-


'''
Tool to scrape questions

'''

import re


test = '''
    1 things in the report that are different that don't 4

    2 relate specifically to the period 2002 to 2010.
    3 O. Okay. Let me try to now move to a question
    4 to asking you about how you, as a medical historian,

    5 go about practicing your expertise. And I'll tell

    6 you —— have you read Professor Greenwood's report in

    7 this case?

    8 A. No.

    9 O. She is also a historian. The scope of her
    10 report is more aimed at information that was addressed

    11 to the public as opposed to the public health
    12 community, but she had a section which I noticed yours

    13 didn't that talks about what the historical method is.

    14 And 1 was going to ask you if you proceed as does

    15 Professor Greenwood.
        '''


def scrape_questions_and_answers(filepath, start_page, end_page):

    file = open(filepath)

    raw_text = ''
    for line in file.readlines():
        raw_text += line




    # extract relevant pages from the document
    extract = raw_text[
        raw_text.find("Page {} \n".format(start_page)) :
        raw_text.find("Page {} \n".format(end_page+1))
    ]

    extract = clean_raw_text(extract, 'le')

    print extract

    extract = test

    questions = re.findall(r'A. (.*?)Q.', extract, re.MULTILINE)
    answers = re.findall(r'^A[^Q]*', extract, re.MULTILINE)

    print len(questions), len(answers)

    for i in range(len(answers)):
        print questions[i].strip()
        print answers[i].strip()
        print "\n"

    print re.findall(r'.+?(?=O.)', extract, re.MULTILINE)

#    for question in re.search('^A[^Q]*', extract):
 #       r

def clean_raw_text(text, doc_source):
    '''

    :param doc_source:
    :return:
    '''

    # print re.findall(r'^[0-9]+\s', text, re.MULTILINE)
    #
    # print re.sub(r'^[0-9]+\s', '', text, count=1000, flags=re.MULTILINE)
    #
    # clean = text
    #
    # for i in range(100):
    #     print clean, re.findall(r'^[0-9]+\s', clean, re.MULTILINE)
    #     clean = re.sub(r'^[0-9]+\s', '', clean, re.MULTILINE)

    # remove numbers at the beginning of the line
    clean = re.sub(r'^[0-9]+\s', '', text, count=10000, flags=re.MULTILINE)
    return clean



if __name__ == "__main__":

    filepath = '/home/stephan/tobacco/code/ramses/code/test/le_fpkl0190.txt'

    scrape_questions_and_answers(filepath, 7, 7)

