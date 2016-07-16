from text_passages import get_text_passages, store_as_csv

from utilities import get_sides

from ngrams import ngrams, visualize_ngrams
from linear_regression import lasso


def passages(search_term, historian_last_name=None, side_question=None, side_answer=None, year_start=1987,
             year_end=2017, scope=0, type=None):
    '''
    Passages lets you find text passages with a lot of different configuration options.
    All passages get stored as csv files, found in the csv folder

    The parameters you can pass are:

    search_term             (required) search term or expression to look for
    historian_name_last     last name of the historian to look for
    side_question           side that poses the question ("Plaintiff" or "Defendant")
    side_answer             side of the witness the question ("Plaintiff" or "Defendant")
    type                    questions or answers ("Q" or "A")
    year_start              earliest year to use (default: 1990)
    year_end                final year to use (default: 2017)
    scope                       0: only return passage that includes the search term. (default)
                                1: return the passage that includes the search term as well as the preceeding
                                    and succeeding question/answer
                                2: and so forth


    Examples

    # Find all passages mentioning various between 1990 and 2017
    passages('various')

    # Find all passages by Kyriakoudes that mention addiction
    passages('addiction', historian_last_name="Kyriakoudes")

    # Find all passages by Kyriakoudes that mention addiction, include the surrounding questions
    passages('addiction', historian_last_name="Kyriakoudes", scope=1, type='A')

    # Find all questions that mention addiction between 2000 and 2015
    passages('addiction, type='Q', year_start=2000, year_end=2015)

    # Find all questions by defendant lawyers that mention addiction
    passages('addiction', side_question='Defendant', type='Q')


    :return:
    '''

    if side_question or side_answer:
        side_question, side_answer = get_sides(side_question, side_answer)

    doc_list, years, witnesses = get_text_passages(search_term, historian_name_last=historian_last_name,
                                                    side_question=side_question, side_answer=side_answer,
                                                    year_start=year_start, year_end=year_end, scope=scope)

    store_as_csv(doc_list, years, witnesses, search_term, type, side_answer)


# modify: export as csv

# count by Witness

# totals by year



if __name__ == "__main__":
    passages('cancer', side_question='Defendant')