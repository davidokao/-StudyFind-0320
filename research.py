from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import time
import nltk
import re
import heapq

def generate_researcher(name, email=None, org=None, study_num=5, search_factor=1.0, doi=None, pmid=None):
    """
    Generates a researcher dictionary given a name and other identifying information.
    
    This method is broken into two sections: Link generation and researcher generation. The link
    created contains results for the first study_num * search_factor results based off of a pmid
    that is either generated or given that should contain the researcher searched.
    
    Keyword arguments:
    name -- the name of the researcher in the form "First Last"
    email -- the email of the researcher (default 'None')
    org -- the organization of the researcher (default 'None')
    study_num -- the requested number of studies returned (default 5)
    search_factor -- the search range for the studies pulled (default 1.0)
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
    query_num = int(study_num * search_factor)
    
    url = base + "&retmax=" + str(query_num) + "&term=" + query + "&cauthor_id=" + pmid
    
    # Create List of Articles
    webpage = urllib.request.urlopen(url).read()
    dict_page = json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    #########################
    # Researcher Generation #
    #########################
    
    # Standardized output with Google Scholar scraper, aside from 'pmid' field
    researcher = {'name': name, 'email': 'None', 'organization': 'None', 'pmid': "None", 'topics': 'None','studies': 'None'}
    articles = []
    topics = []
    api_request_counter = 0
    
    for pubmed_id in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=pubmed_id"
        url = url.replace('pubmed_id', pubmed_id)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        article, tags = generate_article_and_tags(soup)
        articles.append(article)
        topics = topics + tags
        
        # The following code removed articles that had no information in
        # its entries. We believe the problem was due to an api request error
        # as we were not giving it enough time between queries.
        
        #add = False
        #for entries in article.values():
        #    if entries != 'None':
        #        add = True
        #if add:
        #    articles.append(article)
        #    topics = topics + tags
        #else:
        #    raise Exception("Blank study encountered. Please save query information for further replication.")
        
        api_request_counter += 1
        if api_request_counter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep inbetween.
            api_request_counter = 0
    
    if email:
        researcher['email'] = email
    if org:
        researcher['organization'] = org
    if pmid:
        researcher['pmid'] = pmid # There should always be a pmid returned.
    if topics:
        researcher['topics'] = reduce_tags(topics)
    if articles:
        articles = sorted(articles, key = lambda i: i['publication date'], reverse=True)
        researcher['studies'] = articles[:study_num]
    
    return researcher

def doi_to_pmid(doi):
    """
    Returns a valid PubMed ID if it exists.
    
    Given a valid DOI name or the None object, use the NCBI id converter API to potentially produce a PubMed ID.
    If no results are obtained, the None object should be returned.
    
    Keyword arguments:
    doi -- the DOI name of the publication to be searched
    """
    url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi + "&format=json"
    
    webpage = urllib.request.urlopen(url).read()
    dict_page = json.loads(webpage)
    pmid = dict_page["records"][0]["pmid"]
    
    return pmid

def ft_query(name, email=None, org=None, query_num=10):
    """
    Searches for verifiable articles for a particular researcher, with the prior information
    that this is the first-time query being performed.
    
    If we have not previously searched for this researcher, this method should run a search of the first
    query_num articles and pick the one with the most verifiable information. The name of this function
    is shorthand for "first-time query".
    
    The logic can be changed to determine which intermediate pmid is selected,
    but keep in mind only one should be selected.
    
    Keyword arguments:
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    query_num -- the number of articles to search through (default 10)
    """
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json"
    
    query = name.split()[1] + "+" + name.split()[0]
    
    url = base + "&retmax=" + str(query_num) + "&term=" + query
    
    webpage = urllib.request.urlopen(url).read()
    dict_page = json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    
    pubmed_id_list = []
    email_counter = 0
    org_counter = 0
    api_request_counter = 0
    
    for pubmed_id in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=pubmed_id"
        url = url.replace('pubmed_id', pubmed_id)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        vtable = ft_verify(soup, name, email, org)
        if vtable[0]: # If the email was verified
            pubmed_id_list.insert(email_counter, pubmed_id)
            email_counter += 1
        elif vtable[1]: # If the organization was verified
            pubmed_id_list.insert(email_counter + org_counter, pubmed_id)
            org_counter += 1
        else:
            pubmed_id_list.append(pubmed_id)
        
        api_request_counter += 1
        if api_request_counter == 3:
            time.sleep(0.2) # API allows for 3 queries at a time. Need to sleep in between.
            api_request_counter = 0
    
    return pubmed_id_list[0]

def ft_verify(soup, name, email=None, org=None):
    """
    Verifies information in a given PubMed article, with the prior information
    that this is within the first-time query being performed.
    
    Understanding that this verification is being called within a first-time query, we are guarenteed
    to be searching by the name, so we just need to return a table with the other information
    asked to verify. The name of this function is shorthand for "first-time verify".
    
    The logic can be changed to determine which information is being verified.
    
    Keyword arguments:
    soup -- the BeautifulSoup object containing the article we are verifying
    name -- the name of the researcher
    email -- the email of the researcher (default None)
    org -- the organization of the researcher (default None)
    """
    firstname = name.split()[0]
    lastname = name.split()[1]
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

def reduce_tags(tags, reduce_num=10):
    """
    Reduces a list of tags to a specified number based on some criteria.
    
    We want tags to "look nice" when presented to the user, so we can attempt to filter out
    tags based off of three criteria. In order, we filter out numbers, dashes, spaces, and what
    should be left is a single word without numbers. Future work would include a more robust
    tag selection process. I am envisioning something similar to the NLP process where you
    assign weights to each tag when they are initially added, scoring higher the closer
    they are to 'ideal', with duplicates having a multiplicative modifier.
    
    The logic can be changed to determine which criteria is checked for and how the tags are
    manipulated.
    
    Keyword arguments:
    tags -- the list of tags to be sorted through
    """
    ideal_tags = []
    mword_tags = []
    dash_tags = []
    num_tags = []
    
    for tag in tags:
        captag = tag.capitalize()
        
        if bool(re.search(r'\d', tag)):
            num_tags.append(tag)
        elif bool(re.search(r'-', tag)):
            dash_tags.append(tag)
        elif bool(re.search(r"\s", tag)):
            mword_tags.append(captag)
        else:
            ideal_tags.append(captag)
    
    topics = sort_list(ideal_tags) + sort_list(mword_tags) + sort_list(dash_tags) + sort_list(num_tags)
    
    return topics[:reduce_num]

def sort_list(unsorted_list):
    """
    Quick method to perform some list manipulation.
    
    We want to sort the given list by entry length, as well as remove duplicates. This could
    be done without using a method, but I personally believe it looks cleaner this way. Feel
    free to change.

    Keyword arguments:
    unsorted_list -- the list to be manipulated
    """
    unique = list(set(unsorted_list))
    slist = sorted(unique, key=len)
    return slist

def generate_article_and_tags(soup):
    """
    Generates an article dictionary and keywords gained from that article
    
    This method is broken into two sections: Retrieving article information and tag information.
    For future work, is highly reccommended to include a field for the DOI name and/or the PMID
    as it would make future PubMed queries much easier.
    
    Keyword arguments:
    soup -- the BeautifulSoup object containing the article
    """
    ###################
    # Article Section #
    ###################
    
    # Standardized output with Google Scholar scraper
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
            month = month_to_num(pubdate.month.text)       
            date += '/' + month
            if pubdate.day:
                date += '/' + pubdate.day.text
    article['publication date'] = date
    
    # Pdf Link
    # All published articles should have a DOI name
    doi = soup.find('articleid', idtype = "doi")
    if doi:
        hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib.request.Request('https://doi.org/' + doi.text, headers=hdrs)
        
        # The pdf link should be the final redirect of accessing DOI name
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

def month_to_num(month):
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
    """
    Applies NLP on a description to produce a summmary.
    
    Specifically breaks a description down into sentences, then words. It counts each
    word and assigns a value to each word based on its relative frequency within the passage.
    Then it assigns each sentence a score based on its word values, finally taking
    the best few sentences in the order of their scores.
    
    Keyword arguments:
    description -- the description to reduce
    """
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

# Uncomment and run for testing purposes
print(generate_researcher("Kamini Singh"))