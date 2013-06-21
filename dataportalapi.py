#Connects to the Socrata search API and loads data describing the tabular datasets in the catalog for use by D3 tree map
#Use: python dataportalapi.py > portaldata.json

import requests, json, math, re

def check_categories(d,category):
  for i in range(len(d)):
    if d[i]['name'] == category: return i
  return -1

#found a simpler url construct that works, keeping this here for now
def build_url(category,name,vid):
	if category != "None":
		category = re.sub('[^0-9a-zA-Z-\s]+', '', category)
		category = category.replace(" ","-")
	else:
		category = "dataset"
	name = re.sub('[^0-9a-zA-Z-\s]+', '', name)
	name = name.replace(" ","-")
	url = sURL + "/" + category + "/" + name + "/" + vid
	return url

#This is the url of your Socrata domain
sURL = 'https://data.sfgov.org'
out = []
page = 1
records = 0
total = 2
rwithdata = 0
while records < total:
	payload = {'limit' : 100, 'page' : page, 'limitTo' : 'TABLES'}
	r = requests.get(sURL + '/api/search/views.json', params=payload)

	responses = r.json()
	total = responses['count']

	for response in responses['results']:
		view = response['view']
		records += 1
		if len(view['columns']) != 0:
			rwithdata += 1
			name = view['name']
			vid = view['id']
			views = view['viewCount']
			size = view['columns'][0]['cachedContents']['non_null']
			if size == 0:
				size = 2 #probably should just skip these altogether, for now making them a tiny dataset so LOG(0) doesn't occur
			logsize = math.log(size)
			if 'category' in view:
				category = view['category']
			else:
				category = "None"
			if 'tags' in view:
				for tag in view['tags']:
					#tags aren't used in the json file yet, these could probably be used to do alternate visualizations or in a companion list, this is just a placeholder for now
					foo = tag
			index = check_categories(out,category)
			url = sURL + '/d/' + vid
			if index == -1:
				out.append({"name": category, "children": [ {"name": name, "value": size, "url": url, "log": logsize } ] })
			else:
				out[index]["children"].append({"name": name, "value": size, "url": url, "log": logsize })
	page += 1

final = {"name" :" San Francisco Data Portal", "count" : rwithdata, "children" : out}
print json.dumps(final)