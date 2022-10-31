# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_parser.ipynb.

# %% auto 0
__all__ = ['affparser', 'regex', 'reg_email', 'db_name', 'parsePubmedData', 'parseArticle', 'parse_email', 'parseMayorKeys',
           'parseMeshKeys', 'parseKeys', 'parse_paperinfo', 'parse_author_xml', 'find_country', 'find_state',
           'affilparser']

# %% ../nbs/01_parser.ipynb 4
import pandas as pd
import xlsxwriter
from datetime import datetime, timedelta, date
from collections import defaultdict, Counter
from affilparser import AffiliationParser

# %% ../nbs/01_parser.ipynb 5
from .core import *
from .data import *
# from pubmed_lib.retriever import *
from fastcore.all import *



# %% ../nbs/01_parser.ipynb 6
affparser = AffiliationParser()
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
db_name = ''

# %% ../nbs/01_parser.ipynb 7
def parsePubmedData(
                        pubmeddata:dict #Data retrieve from pubmedData
                   ) ->list :
    """
    Receive the xml section of PubmedData and return list of ids
    """
    ids = {x.attributes['IdType']: str(x) for x in pubmeddata['ArticleIdList']}
    return ids

# %% ../nbs/01_parser.ipynb 8
def parseArticle(article_info:dict #Dictionary containing information of the article ('Article' Key)
                )->dict: #Somethign
    """
    Function to extract information from an Article, including Title, Abstract, AutorList, journal and published Date
    :param article_info: dictionary from key Article of an Medline citation
    :return (dict): tuple of dictionary with information from paper and autors
    """
    # Extract information about paper content
    title = article_info['ArticleTitle']
    journal = article_info['Journal']['Title']
    published_date = article_info['Journal']['JournalIssue']['PubDate']
    if 'Year' in published_date:
        published = published_date['Year']
    elif 'MedlineDate' in published_date:
        try:
            published = re.findall(r'\d\d\d\d',published_date['MedlineDate'])[0]
        except:
            published = published_date['MedlineDate'][:4]
    try:
#         print(article_info)
        abstract = '. '.join(article_info['Abstract']['AbstractText'])
    except:
        abstract = ''
    try:
        autorlist = article_info['AuthorList']
    except:
        print('no autors found, jumping next')
        autorlist = []
    return {'abstract': abstract, 'autorlist': autorlist, 'title': title, 'journal': journal,
            'published':published}

# %% ../nbs/01_parser.ipynb 9
def parse_email(affil_text:str #Affiliations information for each autor in the Article
               )->str:

    """
    Find email from the Affiliation text (Maybe use the reg_email regex and not the one in the function, TEST)
    """
    match = re.search(reg_email , affil_text) #r'[\w.-]+@[\w.-]+', affil_text)
    if match is not None:
        email = match.group()
        email = email.strip('.;,')
    else:
        email = ''
    return email

# %% ../nbs/01_parser.ipynb 12
def parseMayorKeys(citationInfo:dict #Dictionary from 'MedlineCitation' key containing keywords information
                  )->list:
    """
    Function to Parse the Mayor Keys from the Article.
    """
    keywordList = citationInfo['KeywordList']
    if len(keywordList) == 0:
        return []
    else:
        return [str(x) for x in keywordList[0] if x.attributes['MajorTopicYN'] == 'Y']

# %% ../nbs/01_parser.ipynb 13
def parseMeshKeys(citationInfo:dict #Dictionary from 'MedlineCitation' key containing keywords information
                 )->(list,list):
    """
    Function to Parse the Mayor and Minor MeSH Keys from the Article.
    """
    meshKeys = citationInfo['MeshHeadingList'] if 'MeshHeadingList' in citationInfo.keys() else []
    mayorkeys = [str(x['DescriptorName']) for x in meshKeys if x['DescriptorName'].attributes['MajorTopicYN']=='Y']
    minorKeys = [str(x['DescriptorName']) for x in meshKeys if x['DescriptorName'].attributes['MajorTopicYN']=='N']
    return mayorkeys, minorKeys

# %% ../nbs/01_parser.ipynb 14
def parseKeys(citationInfo):
    return parseMayorKeys(citationInfo), parseMeshKeys(citationInfo)

# %% ../nbs/01_parser.ipynb 15
def parse_paperinfo(
    paperinfo_xml:str #Information 
    ):
    """
    :param paperinfo_xml:
    :return:
    """
    PubmedData = parsePubmedData(paperinfo_xml['PubmedData'])
    article_xml = parseArticle(paperinfo_xml['MedlineCitation']['Article'])
    mayorKeys, (mayorMeshKeys, minorMeshKeys) = parseKeys(paperinfo_xml['MedlineCitation'])
    article_xml['mayorKeys'] = mayorKeys
    article_xml['mayorMesh'] = mayorMeshKeys
    article_xml['minorMesh'] = minorMeshKeys
    autorlist = []
    try:
        for author_xml in article_xml['autorlist']:
            if author_xml.attributes['ValidYN'] == 'N':
                continue
            autor_dict = parse_author_xml(author_xml)
            if autor_dict is None:
                continue
            autorlist.append(autor_dict)
    except:
        print('ERROR: parsing author {}'.format(author_xml))
    finally:
        article_xml['autorlist'] = autorlist
        PubmedData.update(article_xml)
    return PubmedData
    

# %% ../nbs/01_parser.ipynb 16
def parse_author_xml(autor_xml):
    """
    (dict)->dict
    Receive un diccionario con las informaciones de autor proveniente de pubmed xml article

    :param autor_xml:
    :return:
    """
    # Return false if no author information found
    if 'CollectiveName' in autor_xml:
        return
    # try to parse information from XML
    try:
        #get Identifier (only orcid is used now so if they have identifier it should be the first value
        if len(autor_xml['Identifier']) > 0:
            autorID = autor_xml['Identifier'][0]
        else:
            autorID = ''
        #Get the affilaition details from that author, if he had
        if len(autor_xml['AffiliationInfo']) > 0:
            AFFs = ';'.join([affiliationinfo['Affiliation'] for affiliationinfo in autor_xml['AffiliationInfo']])
        else:
            AFFs = ''
        #Retrieving the name information, it is a must and should exist
        autorFN = autor_xml['ForeName']
        autorLN = autor_xml['LastName']
        autorIN = autor_xml['Initials']
        name = autorFN + ' ' + autorLN
        #Start parsing or retrieving information for country, email, company, institute from affiliation
        affilparsed = affilparser(AFFs.split(';')[0])
        country_name, state = find_country(affilparsed['addr-line'],affilparsed['country'])
        emails = parse_email(AFFs)
        data = {'Fname': autorFN, 'Lname': autorLN, 'emails': emails,'countries': country_name,'state': state, 'affiliations': AFFs, 
                'identifier': autorID, 'name': name, 'n_papers': 0, 'updated': date.today().strftime('%d-%m-%Y'),
                 'initials': autorIN}  #
        data.update(affilparsed)
        
        return data

    except ValueError:
        print('not possible to get info value error')
        return
    except OSError as err:
        print("OS Error: {0}".format(err))
        return
    except:
        print('error en parsing')
        return

# %% ../nbs/01_parser.ipynb 17
def find_country(address, country):
    """
    Find country from string
    """
    country = country.lower()
    state = ''
    for countries in COUNTRY:
        for c in countries:
            if c == country:
                country = countries[0]
                # print(country)
                state = find_state(address, country) if country in COUNTRIES_L.keys() else ''
    return country.title(), state

# %% ../nbs/01_parser.ipynb 18
def find_state(address, country):
    """
    (str)->str
    Find state of Brazl from the affiliation details
    :param location:
    :return:
    """
    state_set = set(COUNTRIES_L[country])
    for state in state_set:
        if state in address.replace(',','').split(' '):
             return state.lstrip(' ')
    
    return ''

# %% ../nbs/01_parser.ipynb 19
def affilparser(text):
    parsed_affil = affparser.parse(text)
    return affparser.tuple2dict( parsed_affil)
