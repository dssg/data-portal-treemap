#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
import time

from pattern.web import URL, DOM, plaintext, strip_between 
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs
from bs4 import BeautifulSoup
import urllib2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

## Paul Meinshausen
## Chicago Data Portal scraper

## Open (create) the csv file that the data will be written to. 
output = open("chicagometadata3.csv", "wb")
writer = csv.writer(output)

## Open the selenium webdriver that will open the webpage and wait until
## the data is loaded on the page before scraping.
ff = webdriver.Firefox()
ff.implicitly_wait(30)

## The datasets in the portal are spread over several pages, this loop
## instructs the scraper to go through each page. 
## The html for the pages just updates the page number, so the URL() code 
## keeps track of p and uses it to specify the page number
for p in range(1, 12):
    url = URL('https://data.cityofchicago.org/browse?limitTo=datasets&sortBy=oldest&utf8=%E2%9C%93&page=' + str(p))
    dom = DOM(url.download(cached=True))

## The list of datasets is in a table, so this loop cycles through the row
## elements to scrape each dataset.
    for i in dom.by_tag('tbody')[0:]:
        for g in i.by_tag('tr')[0:]:
            for h in g.by_tag('a.name')[0:]:
                name = h.content
                name = plaintext(name)
                name = name.encode('ascii', 'ignore')
            for j in g.by_class('category infoItem')[0:]:
                category = j.content
                category = plaintext(category)
                category = category.encode('ascii', 'ignore')
            if (g.by_class('tags infoItem')):
                tag = g.by_class('tags infoItem')[0].content
                tag = tag.encode('ascii', 'ignore')
            else: 
                tag = " "
            for k in g.by_class('visits')[0:]:
                visits = k.content
                visits = visits[0:-6]
                visits = visits.encode('ascii', 'ignore')
            for l in g.by_class('description')[0:]:
                description = l.content
                description = description.encode('ascii', 'ignore')
            for link in g.by_tag('a')[1:2]:
                links = abs(link.attributes.get('href', ''), base=url.redirect or url.string)
                ff.get(links+"/about")
                element = ff.find_element_by_class_name("row_count")
                time.sleep(8)
                element_text = element.text

## Write each row to the file
            writer.writerow([name, category, tag, visits, description, links, element_text])


output.close()