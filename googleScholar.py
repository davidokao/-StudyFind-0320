import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time 

driver = webdriver.Chrome('//Users/shardulkothapalli/Desktop/SCHOOL/6.spring2021/cs3312/StudyFind-0320/chromedriver')
url = 'https://scholar.google.com/citations?user=mG4imMEAAAAJ&hl=en'
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