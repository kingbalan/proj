#!/bin/bash
# indiawires//note complete
import BeautifulSoup
import curl
crl = curl.Curl()
print "Fetching Rss Feed.. "
data = crl.get("http://indiawires.com/feed/")
doc = BeautifulSoup.BeautifulStoneSoup(data)
i = 0
for link in doc.findAll('link')[1:]:
	url = str(link.findAll(text=True)[0])
	print "Fetching data " + str(i) + " " + url
	data = crl.get(url)
	data = BeautifulSoup.BeautifulSoup(data)
	content = data.find("div",{"class":"entry1"})
	print "Writing File"
	fp = open("temp-indiawires-" + str(i),'w')
	for pdata in content.findAll("p"):
		temp = pdata.findAll(text=True)
		if len(temp) > 0 :
			fp.write(temp[0].encode("ascii","ignore"))
	i = i + 1

