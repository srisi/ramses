
import sqlite3

from calendar import timegm
from dateutil import parser
from datetime import datetime

from configuration import DB_PATH

def flexible_htm(datestring,dayfirst=False,yearfirst=False):
    """
    Copied from anser_indicus

    Given a variety of human-readable date input strings, return a machine-friendly Unix timestamp

    Utilize dateutil's parser to extract unix timecodes from pretty much any time representation

    :param str datestring: string representing a date and time
    :keyword bool dayfirst: If the input string represents a date with the day number first, set this to True
    :keyword bool yearfirst: If the input string represents a date with the year number first, set this to True
    :return: Unix timestamp
    :rtype: int
    """
    return int(timegm(parser.parse(datestring,dayfirst=dayfirst,yearfirst=yearfirst).timetuple()))

def mth(timestamp, format='%Y-%m-%d'):

    return datetime.fromtimestamp( timestamp).strftime(format)

def print_highlight(text, highlight, color = 'red'):
    '''
    Prints a string and highlights the highlight passage

    :param text: e.g. 'This is a test string'
    :param highlight: e.g. 'test'
    :param color:
    :return:
    '''

    colors = {
        'red': '\033[91m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    }


    start = text.find(highlight)
    print text[:start] + colors[color] + highlight + colors['end'] + text[start+len(highlight):]



def get_sides(side_question, side_answer):

    if not side_question:
        if side_answer == 'Defendant':
            side_question = 'Plaintiff'
        else:
            side_question = 'Defendant'

    if not side_answer:
        if side_question == 'Defendant':
            side_answer = 'Plaintiff'
        else:
            side_answer = 'Defendant'

    return side_question, side_answer


def document_iterator(year_start=1940, year_end=2020,
                      side_question=None, side_answer=None, type=None,
                      search_term=None, historian_name_last=None, historian_name_first=None,
                      format=None):
    '''

    :param year_start:
    :param year_end:
    :param type: Q or A
    :param side_question: Defendant or Plaintiff
    :param side_answer: Defendant or Plaintiff
    :return:
    '''

    if side_question or side_answer:
        side_question, _ = get_sides(side_question, side_answer)


    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # access stores Datetime such that the last 3 digits are hour and minute -> multiply by 1000
    start_timestamp = flexible_htm('1/1/{}'.format(year_start)) * 1000
    end_timestamp = flexible_htm('1/1/{}'.format(year_end+1)) * 1000

    query = '''SELECT qas.text, legal_document.date_doc,
                      qas.document, qas.id, historian.name_last, historian.name_first, historian.Side
                    FROM qas
                      JOIN legal_document on legal_document.file_name = qas.document
                      JOIN historian on legal_document.id_historian = historian.id_historian'''

    if type:
        if side_question:
            query += ' WHERE legal_document.side_question = "{}" AND qas.type= "{}"'.format(side_question, type)
        else:
            query += ' WHERE qas.type= "{}"'.format(type)

    query += ' AND legal_document.date_doc >= {} AND legal_document.date_doc <= {} '.format(start_timestamp, end_timestamp)

    if search_term:
        query += ' AND UPPER(qas.text) LIKE "%{}%" '.format(search_term.upper())

    if historian_name_last:
        query += ' AND historian.name_last = "{}" '.format(historian_name_last)
    if historian_name_first:
        query += ' AND historian.name_first = "{}"'.format(historian_name_first)

    query += ' ORDER BY legal_document.date_doc ASC;'

    cur.execute(query)


    for document in cur.fetchall():

        date = mth(document[1]/1000)
        if format == 'docs_only':
            yield document[0]
        elif format == 'text_passages':
            yield (date, document[0], document[2], document[3], document[4], document[5], document[6])
        else:
            yield (date, document[0])


if __name__ == "__main__":
    print_highlight('this is a test string', 'test')