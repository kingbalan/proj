#!/bin/env python

import numpy
from scipy.cluster import hierarchy
import numpy
import nltk.data
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt
import glob
import os
from nltk.tag.simplify import simplify_wsj_tag

def removeStopwords(sentence):
	'''Remove Stop words and stem the sentence. It also splits the sentences into words before stemming. '''
	# TODO(cliveverghese@gmail.com) : Add part of speach to each word hence produceds
	ret = []
	orig = []
	temp = nltk.word_tokenize(sentence)
	temp = nltk.pos_tag(temp)
	stmr = WordNetLemmatizer()
	temp = [(word, simplify_wsj_tag(tag)) for word, tag in temp]
	#sen = [ stmr.lemmatize(x.lower(),'n') for x,tag in temp if tag in ['N','NP','NUM']]
	
	sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sentence).split() if word.lower() not in stopwords.words('english') ]
	return sen
	
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
os.chdir("fetcher/")
bag_of_words = []
global_vector = []
doc_vector = []
files = []
bag_of_words_size = 0
for fileLoc in glob.glob("temp*") :
	print "Scanning file " + fileLoc
	
	temp_vector = [0 for x in range(bag_of_words_size)]
	fp = open(fileLoc)
	data = fp.read()
	data = tokenizer.tokenize(data)
	num_sen = 0
	for sen in data:
		num_sen += 1
		bog = removeStopwords(sen)
		for word in bog:
			if word not in bag_of_words:
				bag_of_words.append(word)
				bag_of_words_size = bag_of_words_size + 1
				temp_vector.append(0)
				global_vector.append(0)
				for i in range(len(doc_vector)):
					doc_vector[i].append(0)
			temp_vector[bag_of_words.index(word)] += 1
			global_vector[bag_of_words.index(word)] += 1
	doc_vector.append(temp_vector)
	files.append(fileLoc)
print doc_vector
threshold = 3
itr_range = len(global_vector)
x = 0
while x < itr_range:
	#print "iteration " + str(x)
	#print "Threshold is " + str(global_vector[x])
	if global_vector[x] < threshold:
		global_vector.pop(x)
		word = bag_of_words.pop(x)
		#print "Removing word : " + word
		itr_range = itr_range - 1
		for i in range(len(doc_vector)):
			doc_vector[i].pop(x)
	else :
		x = x + 1
X = numpy.array(doc_vector)
#print X
res = hierarchy.fclusterdata(X,1,depth=4,metric="correlation",method="average",criterion="maxclust")
bag_of_words.sort()
print bag_of_words
print global_vector
for x in range(len(files)):
	print files[x] + " (" + str(res[x]) + ")"
	
