#!/usr/bin/python

import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt

# TODO(cliveverghese@gmail.com): Remove this function from this file and seperate it into a module.
def removeStopwords(sentence):
	ret = []
	stmr = WordNetLemmatizer()
	for sen in sentence:
		sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sen).split() if word.lower() not in stopwords.words('english') ]
		ret.append(sen)
	return ret
	
# TODO(cliveverghese@gmail.com): Add more command line options

args = sys.argv[1:]
try:
	arg,opt = getopt.getopt(args,"h")
	
except getopt.GetoptError:
	print "Usage: " + sys.argv[0] + " [OPTIONS] FILE..."
	sys.exit(1)
if len(opt) == 0:
	print "Usage: " + sys.argv[0] + " [OPTIONS] FILE..."
	sys.exit(1)
	

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentence = []
for tempfile in opt:
	fp = open("test.txt")
	data = fp.read()
	data = tokenizer.tokenize(data)

	for sen in data:
		sentence.append(sen)
	fp.close()


sentence = removeStopwords(sentence)

bag_of_words = []
for sen in sentence:
	for word in sen:
		if word not in bag_of_words:
			bag_of_words.append( word )

global_vector = [0 for x in range(len(bag_of_words)) ]
sentence_temp = []
for sen in sentence:
	v = [ 0 for x in range(len(bag_of_words)) ]
	for word in sen:
		v[bag_of_words.index(word)] += 1
		global_vector[bag_of_words.index(word)] += 1	
	sentence_temp.append(sentenceRepresentation(sen,v))
	
sentence = sentence_temp
global_vector = Vector(global_vector)

sentence = sorted(sentence,key= lambda x: global_vector.cosine(x.words))
sentence.reverse()
summary = []
print "How many sentences : "
n = int(raw_input())
for i in range(n):
	summary.append(sentence[0].sentence)
	temp = sentence[0].words
	sentence.remove(sentence[0])
	for sen in sentence:
		for w in temp:
			if w in bag_of_words:
				sen.words.remove(bag_of_words.index(w))
	sentence = sorted(sentence,key = lambda x:global_vector.cosine(x.words))
	sentence.reverse()

for sen in summary:
	print sen
	print "\n"
	
# TODO(balan1.618@gmail.com): Add the sentence regeneration

# TODO: Document all functions used within our code including the once that we created		


