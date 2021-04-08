from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import time


def generate_article_and_tags(soup):
    """
    Generates an article dictionary and keywords gained from that article
    
    This method is broken into two sections: Retrieving article information and tag information.
    It is highly reccommended to include a field for the DOI name and/or the PMID
    as it would make future queries much easier.
    
    Keyword arguments:
    soup -- the BeautifulSoup object containing an article
    """
    ###################
    # Article Section #
    ###################
    
    article = {'title': 'None', 'publication date': 'None', 'pdf link': 'None', 'description': 'None'}
    
    # Article Title
    title = soup.find('articletitle')
    if title:
        article['title'] = title.text
    
    # Publication Date
    # Sometimes only part of the date has been provided
    pubdate = soup.find('pubdate')
    date = 'None'
    if pubdate:
        date = pubdate.year.text
        if pubdate.month:
            month = monthToNum(pubdate.month.text)       
            date += '/' + pubdate.month.text
            if pubdate.day:
                date += '/' + pubdate.day.text
    article['publication date'] = date
    
    # Pdf Link
    # All published articles should have a DOI name
    doi = soup.find('articleid', idtype = "doi")
    if doi:
        # The pdf link should be the final redirect of accessing DOI name
        pdflink = urllib.request.urlopen('https://doi.org/' + doi.text)
        article['pdf link'] = pdflink.geturl()
    
    # Abstract
    abst = soup.find('abstracttext')
    if abst:
        article['description'] = abst.text
    
    ################
    # Tags Section #
    ################
    
    # Temporary implementation of tag collection
    tags = []
    keywords = soup.find_all('keyword')
    for keyword in keywords:
        tags.append(keyword.text)
    # Could add MeSH tags if exist, would probably be better than these
    
    return article, tags

def generate_researcher(name, email=None, org=None, studyNum=5, doi=None, pmid=None):
    """
    Generates a researcher dictionary given a name and other identifying information
    
    This method is broken into two sections: Link generation and researcher generation.
    
    Keyword arguments:
    name -- the name of the researcher
    email -- the email of the researcher (default 'None')
    org -- the organization of the researcher (default 'None')
    studyNum -- the requested number of studies returned (default 5)
    doi -- the DOI name of an existing publication by this researcher (default None)
    pmid -- the PubMed ID of an existing article by this researcher (default None)
    """
    ###################
    # Link Generation #
    ###################
    
    # Search Link Creation
    if doi and not pmid:
        pmid = doi_to_pmid(doi)
    elif not pmid:
        pmid = ft_query(name, email, org)
        time.sleep(0.1) # UrlLib requires sleep time between queries, which occurs in ft_query and below
    
    query = name.split()[1] + "+" + name.split()[0]
    
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json"
    url = base + "&retmax=" + str(studyNum) + "&term=" + query + "&cauthor_id=" + pmid
    
    # Create List of Articles
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    #########################
    # Researcher Generation #
    #########################
    
    researcher = {'name': name, 'email': 'None', 'organization': 'None', 'topics': 'None', 'studies': 'None'}
    articles = []
    topics = []
    apiRequestCounter = 0
    
    for PubMedID in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
        url = url.replace('idlist', PubMedID)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        article, tags = generate_article_and_tags(soup)
        
        # Occationally I ran into blank studies, this will temporarily remove them
        # until I can find out what is causing this
        ADD = False
        for entries in article.values():
            if entries != 'None':
                ADD = True
        if ADD:
            articles.append(article)
            topics = topics + tags
        else:
            print('Blank study encountered. Please save query information for further replication.')
        
        apiRequestCounter += 1
        if apiRequestCounter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep in between.
            apiRequestCounter = 0
    
    if email:
        researcher['email'] = email
    if org:
        researcher['organization'] = org
    if articles:
        articles = sorted(articles, key = lambda i: i['publication date'], reverse=True)
        researcher['studies'] = articles
    if topics:
        researcher['topics'] = topics
    if pmid:
        researcher['pmid'] = pmid # There should ALWAYS be a pmid returned.
    else:
        raise Exception("No PMID returned, something has gone horribly wrong")
    return researcher


def doi_to_pmid(doi):
    """
    Returns a valid PubMedID if it exists.
    
    Given a valid DOI name or the None object, use the NCBI id converter API to potentially produce a PubMed ID.
    If no results are obtained, the None object should be returned.
    
    Keyword arguments:
    doi -- the DOI name of the publication to be searched
    """
    if not doi:
        return None
    
    url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi + "&format=json"
    
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    pmid = dict_page["records"][0]["pmid"]
    
    return pmid

def ft_query(name, email=None, org=None):
    """
    Searches for verifiable articles for a particular researcher, with the prior information
    that this is the first-time query being performed.
    
    If we have not previously searched for this researcher, this method should run a search of the first
    10 articles and pick the one with the most verifiable information.
    
    Keyword arguments:
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    """
    query = name.split()[1] + "+" + name.split()[0]
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json"
    url = base + "&retmax=10&term=" + query
    
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    apiRequestCounter = 0
    PubMedIDList = []
    pmid = None
    for PubMedID in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
        url = url.replace('idlist', PubMedID)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        vtable = ft_verify(soup, name, email, org)
        if vtable[0]:
            PubMedIDList.insert(0, PubMedID)
        elif vtable[1]:
            PubMedIDList.append(PubMedID)
        elif not pmid:
            pmid = PubMedID
        
        apiRequestCounter += 1
        if apiRequestCounter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep in between.
            apiRequestCounter = 0
    
    if len(PubMedIDList) > 0:
        pmid = PubMedIDList[0]
    return pmid

def ft_verify(soup, name, email=None, org=None):
    """
    Verifies information in a given PubMed article, with the prior information
    that this is within the first-time query being performed.
    
    Understanding this verification is being called within a first-time query, we are guarenteed
    to be searching by the name, so we just need to return a table with the other information
    asked to verify.
    
    Keyword arguments:
    pmid -- the PubMed ID of the article we are verifying
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    """
    firstname = name.split()[0]
    lastname = name.split()[1]
    vtable = [False] * 2
    
    authors = soup.find_all('author')
    for author in authors:
        fname = author.find('forename')
        lname = author.find('lastname')
        
        # We initially found this article with the name, so the author should always come up
        if(fname and fname.text == firstname and lname and lname.text == lastname):
            affils = author.find_all('affiliation')
            for affil in affils:
                if email and email in affil.text:
                    vtable[0] = True
                if org and org in affil.text:
                    vtable[1] = True
    return vtable
    
def monthToNum(month):
    """
    Converts PubMed's month names and abbreviations to a numerical format
    
    This method should leave months alone if they are already a number.
    If a new spelling is found, please add it to the hardcoded list.
    
    Keyword arguments:
    month -- the month name or number
    """
    if month == 'Jan' or month == 'January':
        month = '01'
    elif month == 'Feb' or month == 'February':
        month = '02'
    elif month == 'Mar' or month == 'March':
        month = '03'
    elif month == 'Apr' or month == 'April':
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun' or month == 'June':
        month = '06'
    elif month == 'Jul' or month == 'July':
        month = '07'
    elif month == 'Aug' or month == 'August':
        month = '08'
    elif month == 'Sep' or month == 'Sept' or month == 'September':
        month = '09'
    elif month == 'Oct' or month == 'October':
        month = '10'
    elif month == 'Nov' or month == 'November':
        month = '11'
    elif month == 'Dec' or month == 'December':
        month = '12'
    return month
