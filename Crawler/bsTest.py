# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import wget
import re
import os.path


url = 'http://www.digikey.com/product-detail/en/52806-0410/WM5316-ND/2046766'
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


# big_table = soup.find_all("td", "attributes-table-main")
# big_table = soup.find("table", class_="product-additional-info")
main_table = soup.find("td", class_="attributes-table-main")
for item in main_table.find_all("tr"):
    print(item.th.string)
    if item.td.a is None:
        print(item.td.string)
    else:
        print(item.td.a.get("href"))
# item = big_table[0].find_all("tr")
# print([lol.string for lol in item])

# for star in soup.find("td", "attributes-table-main"):
    # value = star.find_all("td")
    # print("FOUND ONE\n")
    # print(star)
    # print([name.string for name in star])
# print(value)

