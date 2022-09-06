#!/usr/bin/env python
# coding: utf-8

# In[7]:


import time
import requests
import pandas as pd
import fake_useragent
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
import os

from webdriver_manager.firefox import GeckoDriverManager
os.chdir("/home/pi/Desktop/yt/")
# In[2]:


ua = fake_useragent.UserAgent()
ua.random

sites = []
sites.append("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt")
sites.append("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")
sites.append("https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt")
sites.append("https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt")
sites.append("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt")
sites.append("https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxies.txt")
sites.append("https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt")
sites.append("https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt")
sites.append("https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt")
sites.append("https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt")
sites.append("https://raw.githubusercontent.com/RX4096/proxy-list/main/online/all.txt")
sites.append("https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt")
sites.append("https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt")
sites.append("https://raw.githubusercontent.com/almroot/proxylist/master/list.txt")
sites.append("https://raw.githubusercontent.com/takelley1/proxy-servers/master/proxy.list")
sites.append("https://raw.githubusercontent.com/ToShukKr/rProxyList/main/proxy-list.txt")





import logging
import sys

os.system("mkdir -p 00_log_folder")
def setup_custom_logger(name,fileName):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(fileName, mode='a')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

merger_logger = setup_custom_logger('RoboStock','proxy_url_log.nas')

merger_logger.info("Fetching proxy List!")


# In[3]:

def git_proxy(url):
    proxy_ = []
    page=requests.get(url, headers= {'User-Agent': ua.random}).text   
    proxy_list = page.split("\n")
    for proxy in proxy_list:
        if (":" in proxy):
            proxy_.append(proxy)
        else:
            continue
    return proxy_

def proxies(sites):
    url="https://hidemy.name/en/proxy-list/?type=s#list"
    page=requests.get(url, headers= {'User-Agent': ua.random}).text
    tables = pd.read_html(page)
    tables[0]["proxy1"] = tables[0]["IP address"].astype(str) +":"+ tables[0]["Port"].astype(str)
    proxies = tables[0]["proxy1"].values.tolist()
    
    url="https://free-proxy-list.net/"
    page=requests.get(url, headers= {'User-Agent': ua.random}).text
    tables = pd.read_html(page)
    df=tables[0]
    df1 = df[df['Https'] == 'yes']
    df1.reset_index(inplace = True, drop = True)
    df1["proxy1"] = df1['IP Address'].astype(str) +":"+ df1["Port"].astype(str)
    proxies.extend(df1["proxy1"].values.tolist())
    
    url="https://www.proxy-list.download/HTTP"
    page=requests.get(url, headers= {'User-Agent': ua.random}).text
    tables = pd.read_html(page)
    tables[0]["proxy1"] = tables[0]["IP Address"].astype(str) +":"+ tables[0]["Port"].astype(str)
    proxies.extend(tables[0]["proxy1"].values.tolist())
    
    for site in sites:
        proxies.extend(git_proxy(site))
        
    x = (set(proxies))
    refined = []
    for _ in x:
        if("://" in _):
            n=_.split("://")[1]
            if("\r" in n):
                i = n.split('\r')[0]
                refined.append(i)
            else:
                refined.append(n)
        else:
            if("\r" in _):
                i = _.strip("\r")
                refined.append(i)
            else:
                refined.append(_) 
                
    return refined


# In[4]:


def links():
    options = webdriver.ChromeOptions() 
    options.add_argument("user-data-dir=""C:\\Users\\vatsal\\Hez\\Actual work\\Untitled Folder\\bse_chitthe_web_driver") #Path to your chrome profile
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(executable_path= "chromedriver.exe", options=options)
    driver.get("https://www.youtube.com/channel/UCzSpDyGItbsvEtviWa1u_yg/videos")
    
    previous_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height
        
    time.sleep(5)
    
    lis = driver.find_elements(By.ID, "video-title")
    links = []
    for i in range(len(lis)):
        links.append(lis[i].get_attribute("href"))
    driver.quit()
    return links

# In[5]:

with Display(visible=False, size=(1200, 1500)):
    proxy_list = pd.DataFrame()
    proxy_list["PROXIES"] = proxies()
    links_list = pd.DataFrame()
    links_list["LINKS"] = links()


# In[ ]:


links_list.to_pickle('links_list.nas') 
proxy_list.to_pickle("proxy_list.nas")


# In[ ]:


# for lin in tqdm(link):
#     for prox in proxy:    
#         handle_web(prox, lin, 40)


# In[ ]:


# thread_list = list()


# In[ ]:


# for i in range(5):
#     t = threading.Thread(name='Test {}'.format(i), target=handle_web(random.choice(proxy), random.choice(link), 40))
#     t.start()
#     time.sleep(1)
#     print(t.name + ' started!')
#     thread_list.append(t)
#     for thread in thread_list:
#         thread.join()


# In[ ]:




merger_logger.info("Proxy List Fin!")