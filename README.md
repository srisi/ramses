# The Judge and The Historian Quantified

## Pre-processing steps

1. Convert the database
    1. Export all 3 tables in Acces DB to CSV
    2. Import CSV into `database/depo.db` using http://sqlitebrowser.org/ or https://sqlitestudio.pl/index.rvt
2. Move / copy the txt files in the `docs/txt` directory
3. Execute the `code/extract_qa.py` script

## Processing steps

### Find passages
1. Modify the query at the bottom of `code/text_passages.py`
2. Execute the `code/text_passages.py` script
### Visualize a query
1. Modify the queries at the bottom of `code/ngrams.py`
2. Execute the `code/ngrams.py` script
