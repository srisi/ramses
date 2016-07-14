

from utilities import document_iterator
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import Lasso, Ridge

from scipy.sparse import vstack

import numpy as np


def lasso(term, year_start=1990, year_end=2016, qa='A'):

    ngram_range=(2, 2)


    vectorizer = CountVectorizer(max_features= 50000, ngram_range=ngram_range)

    docs_all = document_iterator(type=qa, year_start=year_start, year_end=year_end, format='docs_only',
                                 search_term=term, )
    vectorizer.fit(docs_all)

    vocabulary =  vectorizer.get_feature_names()

    vectorizer_plaintiff = TfidfVectorizer(vocabulary=vocabulary, ngram_range=ngram_range, use_idf=True)
    docs_plaintiff = document_iterator(type=qa, year_start=year_start, side_answer='Plaintiff', format='docs_only', search_term=term)
    dtm_plaintiff = vectorizer_plaintiff.fit_transform(docs_plaintiff)

    vectorizer_defendant = TfidfVectorizer(vocabulary=vocabulary, ngram_range=ngram_range, use_idf=True)
    docs_defendant = document_iterator(type=qa, year_start=year_start, side_answer='Defendant', format='docs_only', search_term=term)
    dtm_defendant = vectorizer_defendant.fit_transform(docs_defendant)

    print dtm_plaintiff.shape, dtm_defendant.shape

    X = vstack([dtm_plaintiff, dtm_defendant])

    print X.shape
    y = np.ndarray(shape=(X.shape[0], 1))

    # Plaintiff docs = 1, defendant docs = -1
    y[:dtm_plaintiff.shape[0], 0] = 1
    y[dtm_plaintiff.shape[0]:, 0] = -1


    clf = Ridge(alpha=0.1)
    clf.fit(X, y)

    print clf.intercept_
    print clf.coef_
    print len(clf.coef_[0])

    coeff = clf.coef_[0]

    argsorted = np.argsort(coeff)
    min_coef = argsorted[:10]
    max_coef = argsorted[-10:][::-1]



    min_coefs = [(vocabulary[i], coeff[i]) for i in min_coef]
    max_coefs = [(vocabulary[i], coeff[i]) for i in max_coef]

    print "\nPredictors for Defendants:\n{}".format(min_coefs)
    print "\nPredictors for Plaintiffs:\n{}".format(max_coefs)


if __name__ == "__main__":
    lasso('proctor')