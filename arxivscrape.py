import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import os
import random
from multiprocessing import Pool
import sys

#check if arxiv block our ip
def get_one_page(url):
    response = requests.get(url)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
    if response.status_code == 200:
        return response.text

    return None


def grab(url):
    #scrape from arxiv
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    #print(soup)
    #content = soup.div
    #print(content)
    #date = soup.find('h3')
    #get rid of trash information
    list_abstracts = soup.find_all('div', class_ = 'tags is-inline-block')
    filtered = re.findall('data-tooltip=".*?"', str(list_abstracts))
    filtered = re.sub('data-tooltip="',"",str(filtered))
    filtered = re.sub('"',"",str(filtered))
    #filtered = re.sub(' '," ",str(filtered))
    filtered = re.sub('\'\,\ \''," not ",str(filtered))
    #filtered = re.sub('Machine Learning',"Machine_Learning",str(filtered))
    #filtered = re.sub('[\'',"",str(filtered))
    #filtered = re.sub('\']',"",str(filtered))
    print (filtered)


#use multiprocessing to speed up
def myprocesspool(num=10):
    pool = Pool(num)
    pool.map(grab,list)
    pool.close()
    pool.join()


if __name__=='__main__':
    #get keyword and scrape the first 1-99 pages
    kw = ""
    for i in range(1,len(sys.argv)):
        if(i != len(sys.argv) - 1):
            kw += sys.argv[i]
            kw += "+"
        else:
            kw += sys.argv[i]
    kw.lower()
    list = []
    for i in range(1,100):
        url = 'https://arxiv.org/search/?searchtype=all&query=%s&abstracts=show&size=200&order=&start=%s' % (str(kw),str(i))
        #print(url)
        list.append(url)
    myprocesspool(10)
