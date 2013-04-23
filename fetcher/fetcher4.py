#!/bin/bash
# hindustantimes..note 10 seconds delay due to microsoft adds...
import BeautifulSoup
import curl
crl = curl.Curl()
print "Fetching Rss Feed.. "
data = crl.get("http://feeds.hindustantimes.com/HT-HomePage-TopStories")
doc = BeautifulSoup.BeautifulStoneSoup(data)
i = 0
for link in doc.findAll('link')[2:3]:
	url = str(link.findAll(text=True)[0])
	print "Fetching data " + str(i) + " " + url
	data = crl.get(url)
	data = BeautifulSoup.BeautifulSoup(data)
	content = data.find("div",{"id":"ctl00_ContentPlaceHolder1_HTStoryPageControl_strytext.sty_txt"})
	print "Writing File"
	fp = open("temp-hindutimes-" + str(i),'w')
	for pdata in content.findAll("p"):
		temp = pdata.findAll(text=True)
		if len(temp) > 0 :
			fp.write(temp[0].encode("ascii","ignore"))
	i = i + 1

