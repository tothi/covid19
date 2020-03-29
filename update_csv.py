#!/usr/bin/python
#
# update data-hun.csv:
# https://hu.wikipedia.org/wiki/2020-as_COVID-19_koronav%C3%ADrus-j%C3%A1rv%C3%A1ny_Magyarorsz%C3%A1gon

from bs4 import BeautifulSoup
import requests
import csv

r = requests.get("https://hu.wikipedia.org/wiki/2020-as_COVID-19_koronav%C3%ADrus-j%C3%A1rv%C3%A1ny_Magyarorsz%C3%A1gon")
soup = BeautifulSoup(r.content, "lxml")

table = soup.find("table", {"class": "wikitable"})

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text.strip())
    output_rows.append(output_row)
    
with open('data-hun.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(output_rows)
