#!/bin/bash

import BeautifulSoup
import curl

crl = curl.Curl()
#print "Fetching Rss Feed.. "
#data = crl.get("http://www.thehindu.com/?service=rss")
#doc = BeautifulSoup.BeautifulStoneSoup(data)
#i = 0
#for link in doc.findAll('link')[1:3]:
#	url = str(link.findAll(text=True)[0])
#	print "Fetching data " + str(i) + " " + url
#	data = crl.get(url)
#	data = BeautifulSoup.BeautifulSoup(data)
#	content = data.find("div",{"class":"article-text"})
#	print "Writing File"
#	fp = open("temp-hindu-" + str(i),'w')
#	for pdata in content.findAll("p",{"class":"body"}):
#		fp.write(pdata.findAll(text=True)[0])
#	i = i + 1

print "Fetching RSS Feed.."
data = crl.get("http://ibnlive.in.com/ibnrss/top.xml")
doc = BeautifulSoup.BeautifulStoneSoup(data)
i = 0
for link in doc.findAll('link')[2:4]:
	url = str(link.findAll(text=True)[0])
	print "Fetching data " + str(i) + " " + url
	data = crl.get(url)
	data = BeautifulSoup.BeautifulSoup(data)
	content = data.find("div",{"id":"windowclassic"})
	print "Writing File"
	fp = open("temp-ibnlive-" + str(i),'w')
	for pdata in content.findAll("p"):
		fp.write(pdata.findAll(text=True)[0].encode("ascii","ignore"))
	i = i + 1
