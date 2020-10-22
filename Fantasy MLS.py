# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 08:16:58 2019

@author: admin
"""

# PLAYERS STATS

from bs4 import BeautifulSoup
#import requests   
from selenium import webdriver
import pandas as pd  
from datetime import datetime 
import time
import numpy as np
import re
import sys


def open_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5) 
    return driver  


url = 'https://fantasy.mlssoccer.com/#stats-center'

driver = open_url(url)
