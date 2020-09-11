import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
#import pymysql
from collections import Counter
import os
import random
from multiprocessing import Pool

def get_one_page(url):
    response = requests.get(url)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
    if response.status_code == 200:
        return response.text

    return None


def grab(i):
    url = 'https://arxiv.org/search/?searchtype=all&query=machine+learning&abstracts=show&size=200&order=&start=%s' % (str(i))
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    #print(soup)
    #content = soup.div
    #print(content)
    #date = soup.find('h3')
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



def myprocesspool(num=10):
    pool = Pool(num)
    pool.map(grab,pages)
    pool.close()
    pool.join()


if __name__=='__main__':

    pages = list(range(1, 100))
    myprocesspool(10)
