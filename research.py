from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import time
import nltk
import re
import heapq



def generate_article_and_tags(soup):
    """
    Generates an article dictionary and keywords gained from that article
    
    This method is broken into two sections: Retrieving article information and tag information.
    It is highly reccommended to include a field for the DOI name and/or the PMID
    as it would make future queries much easier.
    
    Keyword arguments:
    soup -- the BeautifulSoup object containing the article
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
    date = 'None'
    pubdate = soup.find('pubdate')
    if pubdate:
        date = pubdate.year.text
        if pubdate.month:
            month = monthToNum(pubdate.month.text)       
            date += '/' + pubdate.month.text # change to num
            if pubdate.day:
                date += '/' + pubdate.day.text
    article['publication date'] = date
    
    # Pdf Link
    # All published articles should have a DOI name
    doi = soup.find('articleid', idtype = "doi")
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    if doi:
        # The pdf link should be the final redirect of accessing DOI name
        req = urllib.request.Request('https://doi.org/' + doi.text, headers=hdr)
        # pdflink = urllib.request.urlopen('https://doi.org/' + doi.text)
        pdflink = urllib.request.urlopen(req)
        article['pdf link'] = pdflink.geturl()
    
    # Abstract
    abst = soup.find('abstracttext')
    if abst:
        summary = NLP(abst.text)
        article['description'] = summary
    
    ################
    # Tags Section #
    ################
    
    # Temporarily add all of the tags found to a list. Manipulation of the list comes after
    # all tags we are taking have been collected (in generate_researcher).
    
    tags = []
    
    keywords = soup.find_all('keyword')
    for keyword in keywords:
        tags.append(keyword.text)
    
    meshheadings = soup.find_all('meshheading')
    for meshheading in meshheadings:
        tags.append(meshheading.find('descriptorname').text)
    
    return article, tags

def generate_researcher(name, email=None, org=None, studyNum=5, searchFactor=1.0, doi=None, pmid=None):
    """
    Generates a researcher dictionary given a name and other identifying information
    
    This method is broken into two sections: Link generation and researcher generation.
    
    Keyword arguments:
    name -- the name of the researcher in the form "First Last"
    email -- the email of the researcher (default 'None')
    org -- the organization of the researcher (default 'None')
    studyNum -- the requested number of studies returned (default 5)
    searchFactor -- the search range for the studies pulled (default 1.0)
    doi -- the DOI name of an existing publication by this researcher (default None)
    pmid -- the PubMed ID of an existing article by this researcher (default None)
    """
    ###################
    # Link Generation #
    ###################
    
    # Search Link Creation
    if doi and not pmid:
        pmid = doi_to_pmid(doi)
        time.sleep(0.1) # UrlLib requires sleep time between queries, which occurs here and below
    elif not pmid:
        pmid = ft_query(name, email, org)
        time.sleep(0.1)
    
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json"
    
    query = name.split()[1] + "+" + name.split()[0]
    queryNum = int(studyNum * searchFactor)
    
    url = base + "&retmax=" + str(queryNum) + "&term=" + query + "&cauthor_id=" + pmid
    
    # Create List of Articles
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    #########################
    # Researcher Generation #
    #########################
    
    researcher = {'name': name, 'email': 'None', 'organization': 'None', 'topics': 'None', 'pmid': "None",'studies': 'None'}
    articles = []
    topics = []
    apiRequestCounter = 0
    
    for PubMedID in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=PubMedID"
        url = url.replace('PubMedID', PubMedID)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        article, tags = generate_article_and_tags(soup)
        articles.append(article)
        topics = topics + tags
        
        # The following code removed articles that had no information in
        # its entries. The problem was due to an api request error as we
        # were not giving it enough time between queries.
        
        #ADD = False
        #for entries in article.values():
        #    if entries != 'None':
        #        ADD = True
        #if ADD:
        #    articles.append(article)
        #    topics = topics + tags
        #else:
        #    raise Exception("Blank study encountered. Please save query information for further replication.")
        
        apiRequestCounter += 1
        if apiRequestCounter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep inbetween.
            apiRequestCounter = 0
    
    if email:
        researcher['email'] = email
    if org:
        researcher['organization'] = org
    if pmid:
        researcher['pmid'] = pmid # There should always be a pmid returned.
    if articles:
        articles = sorted(articles, key = lambda i: i['publication date'], reverse=True)
        researcher['studies'] = articles[:studyNum]
    if topics:
        #researcher['topics'] = reduce_tags(topics)
        researcher['topics'] = topics[:10]
    if pmid:
        researcher['pmid'] = pmid # There should always be a pmid returned.
    return researcher


def doi_to_pmid(doi):
    """
    Returns a valid PubMedID if it exists.
    
    Given a valid DOI name or the None object, use the NCBI id converter API to potentially produce a PubMed ID.
    If no results are obtained, the None object should be returned.
    
    Keyword arguments:
    doi -- the DOI name of the publication to be searched
    """
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
    X articles and pick the one with the most verifiable information. The name of this function
    is shorthand for "first-time query".
    
    Keyword arguments:
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    """
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json"
    
    query = name.split()[1] + "+" + name.split()[0]
    
    # Arbitrarily searching the first X = 10 results. This can be increased.
    url = base + "&retmax=10&term=" + query
    
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    PubMedIDList = []
    emailcounter = 0
    orgcounter = 0
    apiRequestCounter = 0
    
    for PubMedID in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=PubMedID"
        url = url.replace('PubMedID', PubMedID)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        vtable = ft_verify(soup, name, email, org)
        if vtable[0]: #
            PubMedIDList.insert(emailcounter, PubMedID)
            emailcounter += 1
        elif vtable[1]:
            PubMedIDList.insert(emailcounter + orgcounter, PubMedID)
            orgcounter += 1
        else:
            PubMedIDList.append(PubMedID)
        
        apiRequestCounter += 1
        if apiRequestCounter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep in between.
            apiRequestCounter = 0
    
    return PubMedIDList[0]

def ft_verify(soup, name, email=None, org=None):
    """
    Verifies information in a given PubMed article, with the prior information
    that this is within the first-time query being performed.
    
    Understanding this verification is being called within a first-time query, we are guarenteed
    to be searching by the name, so we just need to return a table with the other information
    asked to verify. The name of this function is shorthand for "first-time verify".
    
    Keyword arguments:
    soup -- the BeautifulSoup object containing the article we are verifying
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    """
    firstname, lastname = name.split()
    vtable = [False] * 2 # One table entry for every artifact we are trying to verify (name already verified)
    
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

def NLP(description):
    stopwords = nltk.corpus.stopwords.words('english')
    
    formatted_desc = re.sub('[^a-zA-z]', ' ', description)
    formatted_desc = re.sub(r'\s+', ' ', formatted_desc)
    formatted_desc = formatted_desc.lower()
    sentence_list = nltk.sent_tokenize(description)
    
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_desc):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return summary

print(generate_researcher("Kamini Singh"))
