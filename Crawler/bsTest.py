# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import wget
import re
import os.path


url = 'http://www.digikey.com/product-detail/en/MIC5205YM5%20TR/576-1262-6-ND/1770866'
# check if file exist
fname = url.split('/')[-1]

if os.path.isfile(fname):
    # file exits
    ptr = open(fname,mode='r', encoding='utf-8')
    source = ''.join(str(line) for line in ptr if "valign=top>Packaging" not in str(line))
else:
    # file not exist
    temp = wget.download(url)
    ptr = open(temp, mode='r', encoding='utf-8')
    source = ''.join(str(line) for line in ptr if "valign=top>Packaging" not in str(line))
ptr.close()
soup = bs(source, 'html.parser')


big_table = soup.find_all("td", "attributes-table-main")


item = big_table[0].find_all("th")
# print(item)

for star in soup.find("td", "attributes-table-main"):
    # value = star.find_all("td")
    print()
    print(star)
# print(value)

