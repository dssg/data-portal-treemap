#!/usr/bin/env python2.7

import csv
import pprint
import math

## This code converts the data portal metadata csv file into JSON format that can be more easily 
## used with d3

## A function that checks whether the category in each row is the first
## instance of that category or has been created already.
def check_categories(d,category):
  for i in range(len(d)):
    if d[i]['name'] == category: return i
  return none

out = []

## Open the csv file with the data portal 
with open('chicagometadata2.csv','r') as f:

## the size of the dataset is being log-transformed because there's such a huge difference
## between the largest datasets and the smallest datasets on the portal. Using log-transformed values
## will allow for a better visualization
  csvf = csv.reader(f)
  csvf.next()
  for i in csvf:
    category = i[1]
    name     = i[0]
    views    = i[3]
    link     = i[5]
    size     = int(i[6])
    logsize  = math.log(size)
    index = check_categories(out,category)
    if index == -1:
      out.append({'name': category, 'children': [ {'name': name, 'value': size, 'link': link, 'log': logsize } ] })
    else:
      out[index]['children'].append({'name': name, 'value': size, 'link': link, 'log': logsize })

for i in out:
  print(i)
