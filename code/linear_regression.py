

from utilities import document_iterator
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import Lasso, Ridge, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

from scipy.sparse import vstack

import numpy as np


def lasso(term, year_start=1990, year_end=2016, qa='A', reg_type='lasso'):

    ngram_range=(2, 5)


    vectorizer = CountVectorizer(max_features= 50000, ngram_range=ngram_range, stop_words='english', min_df=5)

    docs_all = document_iterator(type=qa, year_start=year_start, year_end=year_end, format='docs_only',
                                 search_term=term)
    vectorizer.fit(docs_all)

    vocabulary =  vectorizer.get_feature_names()

    vectorizer_plaintiff = TfidfVectorizer(vocabulary=vocabulary, ngram_range=ngram_range, use_idf=True)
    docs_plaintiff = document_iterator(type=qa, year_start=year_start, side_answer='Plaintiff', format='docs_only', search_term=term)
    dtm_plaintiff = vectorizer_plaintiff.fit_transform(docs_plaintiff)

    vectorizer_defendant = TfidfVectorizer(vocabulary=vocabulary, ngram_range=ngram_range, use_idf=True)
    docs_defendant = document_iterator(type=qa, year_start=year_start, side_answer='Defendant', format='docs_only', search_term=term)
    dtm_defendant = vectorizer_defendant.fit_transform(docs_defendant)

    X = vstack([dtm_plaintiff, dtm_defendant])

    y = np.ndarray(shape=(X.shape[0]))

    # Plaintiff docs = 1, defendant docs = 0
    y[:dtm_plaintiff.shape[0]] = 1
    y[dtm_plaintiff.shape[0]:] = 0

    if reg_type == 'ridge':
        alpha = 0.00001
        clf = Ridge(alpha=alpha)
        clf.fit(X, y)
        coeff = clf.coef_

    elif reg_type == 'lasso':
        alpha = 0.0001
        clf = Lasso(alpha=alpha, max_iter=1000)
        clf.fit(X, y)
        coeff = clf.coef_


    elif reg_type == 'logistic':
        alpha=None
        clf = LogisticRegression()
        clf.fit(X, y)
        coeff = clf.coef_[0]

    mse = mean_squared_error(y, clf.predict(X))
    mae = mean_absolute_error(y, clf.predict(X))



    argsorted = np.argsort(coeff)
    min_coef = argsorted[:10]
    max_coef = argsorted[-10:][::-1]



    min_coefs = [(vocabulary[i], coeff[i]) for i in min_coef]
    max_coefs = [(vocabulary[i], coeff[i]) for i in max_coef]

    print "Using {} regression. Mean Squared Error: {}. Mean Absolute Error: {}".format(reg_type, mse, mae)
    print "Samples. Plaintiff: {}. Defendant: {}. Total: {}. Number of tokens: {}".format(dtm_plaintiff.shape[0],
                                                  dtm_defendant.shape[0], X.shape[0], X.shape[1])
    print "Predictors for Defendants:\n{}".format(min_coefs)
    print "\nPredictors for Plaintiffs:\n{}\n\n".format(max_coefs)


if __name__ == "__main__":
#    lasso(None, reg_type='logistic')
#    lasso(None, reg_type='ridge')
    lasso(term=None, reg_type='ridge')