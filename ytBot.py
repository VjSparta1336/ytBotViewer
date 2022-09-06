#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import requests
import pandas as pd
from tqdm import tqdm
import threading
import os
import random
import psutil
from pyvirtualdisplay import Display
os.chdir("/home/pi/Desktop/yt/")

total_avlbl_ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

total_cpu_usage = psutil.cpu_percent()



import logging
import sys

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

merger_logger = setup_custom_logger('RoboStock','log.nas')

merger_logger.info("Views Gaining Started!")


if (total_avlbl_ram < 10) or (total_cpu_usage > 80):
    merger_logger.info("RAM Khatam")
    exit(1)
import subprocess
output = subprocess.check_output("ps -ef | grep python | wc -l", shell=True)

merger_logger.info(f"Number of processes running {str(output)}")



# In[ ]:
# webdriver.FirefoxOptions

def handle_web(PROXY,vids,xtra_time):
#     
    options = webdriver.ChromeOptions() 
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(executable_path= "chromedriver.exe", options=options)
    try:
        for vid in vids:
            vid = vid.replace("shorts","watch")
            driver.implicitly_wait(0.6)
            driver.get(vid)
            ytbtn = driver.find_elements(by=By.CLASS_NAME, value="ytp-large-play-button") 
            duration = driver.find_elements(by=By.CLASS_NAME, value="ytp-time-duration")
            ytbtn[0].click() 
            minutes_in_sec = int(duration[0].text.split(':')[0]) * 60
            sec = int(duration[0].text.split(':')[1])
            t = minutes_in_sec + sec + xtra_time
            time.sleep(t)
            flag = random.choice(range(2))
            if(flag == 0):
                driver.quit()
            else:
                continue
    except:
        time.sleep(3)
        driver.quit()

# In[5]:


df1 = pd.read_pickle("links_list.nas")
df2 = pd.read_pickle("proxy_list.nas")


# In[8]:


proxies = df2["PROXIES"].to_list()


# In[10]:


links = df1["LINKS"].to_list()


# In[ ]:


for proxy in proxies:
    vids = random.choices(links, k = 4)
    handle_web(proxy, vids, 40)


# In[ ]:




merger_logger.info("Fin!")