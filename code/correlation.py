
from utilities import document_iterator, get_sides
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from tobacco.stats.correlation import correlation_matrix_cython
from tobacco.stats.cooccurrence import cooccurrence_matrix

from scipy.sparse import csr_matrix

import time

import numpy as np

def load_cor_matrix(qa='A', side_question=None, side_answer=None, year_start=1990, year_end=2016, ngram_range=(1,1)):

    side_question, side_answer = get_sides(side_question, side_answer)

    try:
        m = np.load('cor_{}_{}_{}_{}.npz'.format(qa, side_answer, ngram_range[0], ngram_range[1]))
        cor_mat = m['cor_mat']
        features = m['features']
        cooc_mat = m['cooc_mat']

    except IOError:
        cor_mat, cooc_mat, features = calculate_and_store_cor_matrix(qa, side_question, side_answer, year_start,
                                                           year_end, ngram_range)

    features_lookup = {features[i]:i for i in range(len(features))}

    return cor_mat, cooc_mat, features, features_lookup

def calculate_and_store_cor_matrix(qa, side_question, side_answer, year_start, year_end, ngram_range):

    stop_words=None
    if ngram_range== (1,1):
        stop_words = 'english'

    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=ngram_range, stop_words=stop_words, min_df=5,
                                 use_idf=False)
    docs = document_iterator(year_start=year_start, year_end=year_end, type=qa, side_question=side_question,
                             format='docs_only')

    X = vectorizer.fit_transform(docs)
    features = vectorizer.get_feature_names()

    cor_mat = correlation_matrix_cython(X, axis=1)

    cooc_mat = cooccurrence_matrix(X, axis=1)


    np.savez('cor_{}_{}_{}_{}.npz'.format(qa, side_answer, ngram_range[0], ngram_range[1]), cor_mat=cor_mat,
             cooc_mat = cooc_mat.todense(), features=features)

    return cor_mat, cooc_mat, features




def find_most_correlated(term, qa, side_question=None, side_answer=None, year_start=1990, year_end=2017,
                         ngram_range=(1,1)):

    cor_mat, cooc_mat, features, features_lookup = load_cor_matrix(qa, side_question=side_question, side_answer=side_answer,
                                                         year_start=year_start, year_end=year_end,
                                                         ngram_range=ngram_range)

    i = features_lookup[term]

    print "\nType: {}. Side Witness: {}. Term: {}. Occurrences: {}. Features: {}".format(qa, side_answer, term,
                                                               cooc_mat[i,i],  len(features))

    correlations_most = sorted(zip(features, cor_mat[i,:], cooc_mat[i,:]), key=lambda x: x[1], reverse=True)[0:20]
    print [j for j in correlations_most if j[2]>2 ]

    correlations_least = sorted(zip(features, cor_mat[i,:], cooc_mat[i,:]), key=lambda x: x[1], reverse=False)[0:20]
    print [j for j in correlations_least if j[2]>2 ]


    pass

if __name__=="__main__":

    term = 'various'

    find_most_correlated(term, qa='A', side_answer='Defendant', ngram_range= (1,2))
    find_most_correlated(term, qa='A', side_answer='Plaintiff', ngram_range=(1,2))




