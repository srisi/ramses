from sklearn.feature_extraction.text import CountVectorizer

import numpy as np

import urllib2
import csv
import matplotlib.pyplot as plt

import sqlite3

from utilities import flexible_htm, mth, get_sides, document_iterator



def ngrams(year_start=1990, year_end=2016, type = 'Q', side_question=None, side_answer=None, term=None):


    side_question, side_answer = get_sides(side_question, side_answer)

    vectorizer = CountVectorizer(max_features= 100000)

    docs = document_iterator(type=type, side_question=side_question, format='docs_only')
    vectorizer.fit(docs)

    features =  vectorizer.get_feature_names()
    vocabulary = {features[i]:i for i in range(len(features))}

    word_counts = np.zeros(shape= (year_end - year_start + 1, len(vocabulary)), dtype=np.int)

    docs = document_iterator(type=type, side_question=side_question)
    tokenizer = vectorizer.build_tokenizer()
    for doc in docs:
        year = int(doc[0][:4])
        document = doc[1].lower()
        for token in tokenizer(document):
            word_counts[year-year_start, vocabulary[token]] += 1



    totals = np.sum(word_counts, axis=1)

    word_counts =  word_counts[:,vocabulary[term]]
    word_frequencies = 1.0 * word_counts / totals

    viz_formatting = {'Plaintiff': 's',
                      'Defendant': '^'}

    if type == 'A':
        label = '{} in Answers by {} Witnesses.'.format( term, side_answer)
        viz_format = 'b{}'.format(viz_formatting[side_answer])
    if type == 'Q':
        label = '{} in Questions by {} Lawyers.'.format(term, side_question)
        viz_format = 'r{}'.format(viz_formatting[side_question])

    return {
        'year_start': year_start,
        'year_end': year_end,
        'term': term,
        'word_counts': word_counts,
        'word_frequencies': word_frequencies,
        'label': label,
        'viz_format': viz_format,
        'side_question': side_question,
        'side_answer': side_answer,
        'type': type
    }

def visualize_ngrams(ngram_results, year_start, year_end, term, viz_type='relative'):



    label_dict = {'relative': 'Relative Frequencies',
                  'absolute': 'Absolute Counts'}

    if viz_type =='relative':
        data = 'word_frequencies'
    elif viz_type == 'absolute':
        data = 'word_counts'
    else:
        raise "Invalid visualization type"

    # if type == 'A':
    #     label = '{} for {} in Answers Given by {} Witnesses.'.format(label_dict[viz_type], term, side_answer)
    # if type == 'Q':
    #     label = '{} for {} in Questions Posed by {} Lawyers.'.format(label_dict[viz_type], term, side_question)

    label = "Ngrams for {}".format(term)

    years = range(year_start, year_end +1)

    plt.rcParams['figure.figsize'] = (15,8)
    plt.rcParams['font.size'] = 10
    ax= plt.axes()
    for result in ngram_results:
        plt.plot(years, result['word_frequencies'], label=result['label'])
#        plt.plot(years, result['word_frequencies'],  't')
#    plt.plot(years, data, '1', years, word_counts, label='{}'.format(term))
    plt.title(label)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    legend_title = ax.get_legend().get_title()
    legend_title.set_fontsize(15)

    plt.show()



if __name__ == "__main__":


    year_start = 1990
    year_end = 2016
    term = 'cancer'

    ad = ngrams(side_answer='Defendant', type = 'A', term=term, year_start = year_start, year_end=year_end)
    ap = ngrams(side_answer='Plaintiff', type = 'A', term=term, year_start = year_start, year_end=year_end)
    qd = ngrams(side_question='Defendant', type = 'Q', term=term, year_start = year_start, year_end=year_end)
    qp = ngrams(side_question='Plaintiff', type = 'Q', term=term, year_start = year_start, year_end=year_end)

    visualize_ngrams([ad, ap, qd, qp], year_start, year_end, term, viz_type='relative')

    # visualize_ngrams(res1, 'relative')
    #
    # res2 = ngrams(side_answer='Plaintiff', type = 'A', term='addictive')
    # visualize_ngrams(res2, 'relative')