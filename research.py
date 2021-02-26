from bs4 import BeautifulSoup
import requests
import urllib.request
import json
import time


def generate_study_and_tags(soup):
    
    ### Study Section ###
    study = {'title': 'None', 'publication date': 'None', 'pdf link': 'None', 'description': 'None'}
    
    # Article Name #
    name = soup.find('articletitle')
    if name:
        study['title'] = name.text
    
    # Publication Date #
    pubdate = soup.find('pubdate')
    date = 'None'
    if pubdate:
        date = pubdate.year.text
        if pubdate.month:
            month = pubdate.month.text
            if month == 'Jan':
                month = '1'
            elif month == 'Feb':
                month = '2'
            elif month == 'Mar':
                month = '3'
            elif month == 'Apr':
                month = '4'
            elif month == 'May':
                month = '5'
            elif month == 'Jun':
                month = '6'
            elif month == 'Jul':
                month = '7'
            elif month == 'Aug':
                month = '8'
            elif month == 'Sept':
                month = '9'
            elif month == 'Oct':
                month = '10'
            elif month == 'Nov':
                month = '11'
            elif month == 'Dec':
                month = '12'
            date += '/' + pubdate.month.text
            if pubdate.day:
                date += '/' + pubdate.day.text
    study['publication date'] = date
    
    # Pdf Link #
    doi = soup.find('articleid', idtype = "doi")
    if doi:
        study['pdf link'] = 'https://doi.org/' + doi.text
    
    # Abstract #
    desc = soup.find('abstracttext')
    if desc:
        study['description'] = desc.text
    
    ### Tags Section ###
    tags = []
    keywords = soup.find_all('keyword')
    for keyword in keywords:
        tags.append(keyword.text) 
    #Could add MeSH tags if exist, would probably be better than these
    
    return study, tags

def generate_researcher(InputName):
    
    ### Prior information ###
    #Name needs to be in the format "First Last"
    name = InputName
    org = 'Organization'
    email = 'Email'
    
    ### Search Link Creation ###
    #Fill in prior information
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    #Database searching
    db = "pubmed"
    #Output format
    ret = "json"
    #Max number of results
    retnum = '5'
    #Search Query - reorganize name into the format 'Last+F', though I think including the entire first name also works
    query = InputName.split()[1] + "+" + InputName.split()[0]
    #Computed author id
    #cauthor = '32489811'
    #Assemble elink
    url = base + "esearch.fcgi?db=" + db + "&retmode=" + ret + "&retmax=" + retnum + "&term=" + query# + "&cauthor_id=" + cauthor
    #Test esearch URL
    #print(url)
    
    ### Create List of Studies ###
    #Add search results to a list
    webpage = urllib.request.urlopen(url).read()
    dict_page =json.loads(webpage)
    idlist = dict_page["esearchresult"]["idlist"]
    #Test for search results
    #print(idlist)
    
    ### Create Researcher Dictionary ###
    #Setup dictionary
    researcher = {'name': name, 'organization': org, 'topics': 'None', 'studies': 'None'}
    studies = []
    topics = []
    
    for link in idlist:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
        url = url.replace('idlist', link)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        study, tags = generate_study_and_tags(soup)
        
        #Occationally I ran into blank studies? I think this was a result of other issues with my code
        ADD = False
        for entries in study.values():
            if entries != 'None':
                ADD = True
        if ADD:
            studies.append(study)
            topics = topics + tags
        
        #Need to sleep otherwise we get request error
        time.sleep(0.1)
    
    if studies:
        #Sort the studies by date
        studies = sorted(studies, key = lambda i: i['publication date'], reverse=True)
        researcher['studies'] = studies
    if topics:
        researcher['topics'] = topics
    #Test scraping results
    #print(researcher)
    
    return researcher