#!/bin/bash

import BeautifulSoup
import curl
crl = curl.Curl()
print "Fetching Rss Feed.. "
data = crl.get("http://syndication.indianexpress.com/rss/latest-news.xml")
doc = BeautifulSoup.BeautifulStoneSoup(data)
i = 0
for link in doc.findAll('link')[2:]:
	url = str(link.findAll(text=True)[0])
	print "Fetching data " + str(i) + " " + url
	data = crl.get(url + "0")
	data = BeautifulSoup.BeautifulSoup(data)
	content = data.find("div",{"class":"ie2013-contentstory"})
	print "Writing File"
	fp = open("temp-indianex-" + str(i),'w')
	for pdata in content.findAll("p"):
		fp.write(pdata.findAll(text=True)[0])
	i = i + 1

