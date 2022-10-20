# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['regex', 'reg_email', 'db_name', 'searchpb', 'fetch_details', 'getParsedArticles', 'getParsedArticlesPeriod',
           'fetchPubmedArticles', 'retrieveArticles']

# %% ../nbs/00_core.ipynb 3
from Bio import Entrez
import sys
# from tinydb import TinyDB, Query, where
import pandas as pd
import xlsxwriter
from datetime import datetime, timedelta, date
from collections import defaultdict, Counter
import  pickle
from fastcore.all import *
from dotenv import load_dotenv


# %% ../nbs/00_core.ipynb 6
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
db_name = ''

# %% ../nbs/00_core.ipynb 7
def searchpb(
    search_term:str, #Query to be search in pubmed
    retmax:int = 5000, #Maximum number of results to be retrieved
    retmode:str ='xml', #Format of the returned data, options are xml, 
    sort:str='relevance', #Way to sort the results
    mindate:int = None, #Initial data to be search from, year
    maxdate:int = None #Final data to be search from, year
    ):
    """
    It receive a query to be searched in pubmed and return the handler of the search
    """
    Entrez.email = email
    Entrez.api_key = api_key
    handle = Entrez.esearch(db='pubmed',
                            sort=sort,
                            retmax=retmax,
                            retmode=retmode,
                            term=search_term,
                            mindate = mindate,
                            maxdate = maxdate)
    return Entrez.read(handle)

# %% ../nbs/00_core.ipynb 8
def fetch_details(
    IdList:list #List of pubmedIDs to fetch the details
    ):
    """
    It receive a list of pubmedIds from a search, and retrieve all the details of those publications
    """
    ids = ','.join(IdList)
    Entrez.email = email
    Entrez.api_key = api_key
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

# %% ../nbs/00_core.ipynb 9
def getParsedArticles(name, years = 3):
    query = name + '[Author]'
    results = searchpb(query, 100, maxdate = 2021, mindate = 2021 - years)
    id_list = results['IdList']
    if len(id_list) == 0:
        return 0
    papers = fetch_details(id_list)
    n_papers = len(id_list)
    print('checking in {} Articles'.format(n_papers))
    articles=[]
    for i, paperinfo in enumerate(papers['PubmedArticle']):
        article = parse_paperinfo(paperinfo)
        if int(article['published']) < 2020 - years:
            # print('to old, article published on {}'.format(article['published']))
            continue
        articles.append(article)
    print('Keeping with {} from last {} years'.format(len(articles), years))
    return articles

# %% ../nbs/00_core.ipynb 10
def getParsedArticlesPeriod(name, maxdate=2020, years = 3, top_n=None, verbose=False):
    query = name + '[Author]'
    results = searchpb(query, 1000, maxdate = maxdate, mindate = maxdate - years)
    id_list = results['IdList']
    if len(id_list) == 0:
        return ([],0)
    papers = fetch_details(id_list)
    n_papers = len(id_list)
    if verbose:
        print('checking in {} Articles'.format(n_papers))
    articles=[]
    for i, paperinfo in enumerate(papers['PubmedArticle']):
        article = parse_paperinfo(paperinfo)
        if maxdate < int(article['published'])  or int(article['published']) < maxdate -years :
            # print('to old, article published on {}'.format(article['published']))
            continue
        articles.append(article)
    if len(articles) == 0:
        if verbose:
            print('No articles in the time period')
        return ([],n_papers)
    elif top_n:
        df = pd.DataFrame(articles).sort_values('published', ascending=False)
        df = df.iloc[:top_n]
        articles = df.to_dict('records')
    if verbose:
        print('Keeping with {} from last {} years'.format(len(articles), years))
    return (articles, n_papers)

# %% ../nbs/00_core.ipynb 11
def fetchPubmedArticles(name, start, end, path, db_path = '/Volumes/Users/matu/Documents/Xcode/SFDC/db.pckl'):
    """Function to search in pubmed by name, start and end year.
    It checks first in the database of abstracts downloaded before.
    Create a csv file with the parsed pubmed results including abstract, authors, etc. (look at pubmed_utils)

    return (pd.Dataframe) -> the DataFrame with all the information retrieved"""
    db = loadDB(db_path)
    if name not in db:
        print('adding new year {} for {}'.format(start, name))
        (pubmedData, total) = getParsedArticlesPeriod(name, start, end)
        if pubmedData == 0:
            db.update({name: {str(start):[total, 0]}})
            return 
        else:
            db.update({name: {str(start):[total, len(pubmedData)]}})
    else:
        if (str(start) in db[name]) and (str(end) in db[name]):
            print(f"{name} already in DB with year {start} - {end}, passing")
            df = pd.read_csv('{}/{}_{}_{}.csv'.format(path, name, start, start - end))
            return df
        else:
            (pubmedData, total) = getParsedArticlesPeriod(name, start, end)
            if pubmedData == 0:
                db[name].update({str(start):[total, 0]})
                return 
            else:
                db[name].update({str(start):[total, len(pubmedData)]})
    df = pd.DataFrame(pubmedData)
    file_output = '{}/{}_{}_{}.csv'.format(path, name, start, start - end)
    df.to_csv(file_output)
    saveDB(db, db_path)
    if df.shape[0] >= 10:
        df = df.sort_values('published', ascending=False)
        print('Using the 10 newer papers')
        return df.iloc[:10]
    return df

# %% ../nbs/00_core.ipynb 12
def retrieveArticles():
    results = searchpb('Peter Ihnat[Author]')
    papers = fetch_details(results['IdList'])
    articles=[]
    for i, paperinfo in enumerate(papers['PubmedArticle']):
        article = parse_paperinfo(paperinfo)
        articles.append(article)
    return articles
