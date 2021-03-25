from googlesearch import search 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 

def getResearcherURL(name, university=''):
    if name == '':
        return 'input name'
    if university != '':
        t_name = name + ' ' + university
        
    search_url = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors='
    t_name = name.split(' ')
    
    for i in t_name:
        search_url += i + '+'
        
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text,'html')
    summ = soup.findAll("div", {"class": "gsc_1usr"})
    
    for i in summ:
        if university in i.text and name in i.text:
            href = i.find_all('a', href=True)[0]['href']
            return ("https://scholar.google.com"+href)
    return 'no valid researcher found'

def getResearcherProfile(url):
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver = webdriver.Chrome('./chromedriver')
    url += '&view_op=list_works&sortby=pubdate'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html')


    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html')


    prof = soup.findAll("div", {"id": "gsc_prf_i"})
    tags = soup.findAll("a", {"class": "gsc_prf_inta gs_ibl"})
    prof_info = []

    for row in prof[0].find_all("div")[:2]:
        prof_info.append(row.text)
    temp_tags = []
    for tag in tags:
        temp_tags.append(tag.text)
    prof_info.append(temp_tags)
    prof_pic = driver.find_element_by_xpath('//*[@id="gsc_prf_pup-img"]')
    prof_pic = prof_pic.get_attribute('src')

    studies = soup.findAll("tbody", {"id": "gsc_a_b"})
    count = 1

    stoodies = []
    for row in studies[0].find_all("tr", {'class': 'gsc_a_tr'}):
        xp = '//*[@id="gsc_a_b"]/tr[' + str(count) + ']/td[1]/a'
        elem = driver.find_element_by_xpath(xp)
        elem.click()
        time.sleep(0.5)

        try:
            title = driver.find_element_by_xpath('//*[@id="gsc_vcd_title"]/a')
            title = title.text
        except:
            title = 'no title'

        try:
            pubdate = driver.find_element_by_xpath('//*[@id="gsc_vcd_table"]/div[2]/div[2]')
            pubdate = pubdate.text
        except:
            pubdate = 'no date'

        try:
            pdflink = driver.find_element_by_xpath('//*[@id="gsc_vcd_title_gg"]/div/a')
            pdflink = pdflink.get_attribute('href')
        except:
            pdflink = 'no link'

        try:
            desc = driver.find_element_by_xpath('//*[@id="gsc_vcd_descr"]/div/div')
            desc = desc.text
        except:
            desc = 'no description'

        study = {'title': title, 'publication date': pubdate, 'pdf link': pdflink, 'description': desc}
        stoodies.append(study)

        elem = driver.find_element_by_xpath('//*[@id="gs_md_cita-d-x"]/span[1]')
        elem.click()

        count += 1    
    driver.quit()
    profile = {'name': prof_info[0], 'organization': prof_info[1], 'topics': prof_info[2], 'profile pic': prof_pic,
               'studies': stoodies}
    return profile

