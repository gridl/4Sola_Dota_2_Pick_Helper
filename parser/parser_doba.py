#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:52:35 2019

@author: andy
"""

from bs4 import BeautifulSoup
import requests

site_dotabuff = 'https://dotabuff.com/heroes/meta'

page_main_dotabuff = requests.get(site_dotabuff, headers = {'User-agent': 'Andy, just Andy'})
print('Status code: {}'.format(page_main_dotabuff.status_code))

page_content = BeautifulSoup(page_main_dotabuff.content, 'html.parser')
print(type(page_content))

all_tr = page_content.find_all('tr')

print(all_tr[0])