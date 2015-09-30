__author__ = 'khjto'

import re

a="-40°C ~ 85°C "

for letter in a:
    if not re.match('[0-9a-zA-Z_]', letter):
        print(letter)
        a = a.replace(letter,'')
print("end")
print(a)