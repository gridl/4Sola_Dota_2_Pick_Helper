# =============================================================================
# IMPORT MODULES
# =============================================================================

# For getting HTML
import requests

# For parsing
from bs4 import BeautifulSoup

# For saving imgs
import urllib.request as urre

# For getting img-folder path
import os

# =============================================================================
# GLOBAL VARS
# =============================================================================

# Urls
site_url = 'https://ru.dotabuff.com'
img_preurl = '/assets/heroes/'
heroes_preurl = '/heroes'

# Img-folder
save_folder = '/../imgs/heroes_icons/'
dir_path = os.getcwd() + save_folder

# JPG :)
jpg = '.jpg'

# My header
headers={'User-agent': 'Not Andy :)'}

# =============================================================================
# MAIN ACTION
# =============================================================================

# Get HTML
req = requests.get('{}{}'.format(site_url, heroes_preurl), headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

# Get every heroes div's
squares = soup.find_all('div', class_='hero')

# Loop for checking name and get/save icon
for sq in squares:
    name = sq.find_all('div', class_='name')[0].text
    img_url = img_preurl + sq['style'].split()[1].split('/')[3].split(')')[0]
    
    print('I am doing it with {}'.format(name))
    
    full_url = site_url + img_url
    full_dir = dir_path + name + jpg
    
    # Saving
    urre.urlretrieve(full_url, full_dir)

print('WORK IS OVER!')