# =============================================================================
# IMPORT MODULES
# =============================================================================

# Parse
from bs4 import BeautifulSoup

# Request
import requests

# Save file
import json

# =============================================================================
# MAKE GLOBAL VARS
# =============================================================================

# Main dict
heroes = {}

# Headers for requests
headers={'User-agent': 'ANY WORDS'}

# Main pages
site_db_h = 'https://ru.dotabuff.com/heroes'
site_db = 'https://ru.dotabuff.com'

# Main add for pages
counters = '/counters'
meta = '/meta'

# Dict for line-data
lines_dict = {
    'Сложная линия': 'h',
    'Центральная линия': 'm',
    'Легкая линия': 'e',
    'Роуминг': 'r',
    'Лес': 'f',
}

# =============================================================================
# GET HERO NAMES AND LINK TO EACH HERO
# =============================================================================
print('GET HERO NAMES')

req = requests.get(site_db_h, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

hero_square = soup.find('div', class_='hero-grid')
a_list = hero_square.find_all('a')

# Collect href's (aka links) 
href_list = []
for a in a_list:
    item = a['href']
    href_list.append(item)

# Collect heroes links
hero_links = []    
for href in href_list:
    full_link = '{}{}'.format(site_db, href)
    
    req = requests.get(full_link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    h1 = soup.find('h1')
    name = list(h1)[0]
    
    heroes[name] = {}
    
    hero_links.append(full_link)   

# =============================================================================
# GET LINES INFO
# =============================================================================
print('GET LINES INFO')

# Check every hero ones
for i_link in range(len(hero_links)):
    req = requests.get(hero_links[i_link], headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    name = list(heroes.keys())[i_link]
    
    tbody = soup.find_all('tbody')
    tr = tbody[1].find_all('tr')
    
    heroes[name]['lines'] = {}
    
    # Get every line
    for t in tr:
        td = t.find_all('td')
        value = td[2].text.split('%')[0]
        heroes[name]['lines'][lines_dict[td[0].text]] = float(value)
    
    # Create self-var for every hero
    for line in list(lines_dict.values()):
        try:
            heroes[name]['lines'][line] = heroes[name]['lines'][line]
        except KeyError:
            heroes[name]['lines'][line] = 0.    

# =============================================================================
# GET VERSUS VARS
# =============================================================================
print('GET VERSUS INFO')

# Go to counters pages
for i_link in range(len(hero_links)):
    counters_link = '{}{}'.format(hero_links[i_link], counters)
    
    req = requests.get(counters_link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    name = list(heroes.keys())[i_link]
    
    tbody = soup.find_all('tbody')
    tr = tbody[3].find_all('tr')
    
    heroes[name]['versus'] = {}

    for t in tr:
        c_name = t.find_all('td')[0]['data-value']
        c_rate = float(t.find_all('td')[3]['data-value'])
        c_rate -= 50
        c_rate = round(c_rate, 2)
        
        heroes[name]['versus'][c_name] = c_rate
        
    heroes[name]['versus'][name] = 0.
    
# =============================================================================
# GET RATE VALUES
# =============================================================================
print('GET RATE INFO')

req = requests.get('{}{}'.format(site_db_h, meta), headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

tbody = soup.find_all('tbody')
tr = tbody[0].find_all('tr')

for t in tr:
    td = t.find_all('td')

    name = td[0]['data-value']
    
    r_02k = td[3]['data-value']
    r_23k = td[5]['data-value']
    r_34k = td[7]['data-value']
    r_45k = td[9]['data-value']
    r_50k = td[11]['data-value']

    r_02k = float(r_02k)
    r_23k = float(r_23k)
    r_34k = float(r_34k)
    r_45k = float(r_45k)
    r_50k = float(r_50k)

    r_02k = round(r_02k, 2)
    r_23k = round(r_23k, 2)
    r_34k = round(r_34k, 2)
    r_45k = round(r_45k, 2)
    r_50k = round(r_50k, 2) 
    
    heroes[name]['rate'] = {}
    
    heroes[name]['rate']['02k'] = r_02k
    heroes[name]['rate']['23k'] = r_23k
    heroes[name]['rate']['34k'] = r_34k
    heroes[name]['rate']['45k'] = r_45k
    heroes[name]['rate']['50k'] = r_50k
    
# =============================================================================
# SAVE FILE
# =============================================================================
    
json.dump(heroes, open('../json/heroes.json', 'w'))

print('FILE SAVED!')