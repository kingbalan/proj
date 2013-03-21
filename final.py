#!/usr/bin/python

import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt



def usage():
	''' Print the command line usage of the program'''
	print "Usage: " + sys.argv[0] + " [OPTIONS] FILE..."
	print "See " + sys.argv[0] + " -h for more details"
	
# TODO(cliveverghese@gmail.com): Remove this function from this file and seperate it into a module.
def removeStopwords(sentence):
	'''Remove Stop words and stem the sentence. It also splits the sentences into words before stemming. '''
	# TODO(cliveverghese@gmail.com) : Add part of speach to each word hence produceds
	ret = []
	orig = []
	stmr = WordNetLemmatizer()
	sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sentence).split() if word.lower() not in stopwords.words('english') ]
	return sen
	
# TODO(cliveverghese@gmail.com): Add more command line options

args = sys.argv[1:]
try:
	arg,opt = getopt.getopt(args,"h")
	
except getopt.GetoptError:
	usage()
	sys.exit(1)
if len(opt) == 0:
	usage()
	sys.exit(1)
	

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentence = []
total_sentences = 0
for tempfile in opt:
	fp = open(tempfile)
	data = fp.read()
	data = tokenizer.tokenize(data)
	i = 0
	for sen in data:
		#print "(" + str(i) + ")" + sen
		bog = removeStopwords(sen)
		sentence.append(sentenceRepresentation(bog,0,sen,tempfile,i))
		i = i + 1
	fp.close()
	total_sentences += i


bag_of_words = []
for sen in sentence:
	for word in sen.sentence:
		if word not in bag_of_words:
			bag_of_words.append( word )
i = 0
global_vector = [0 for x in range(len(bag_of_words)) ]
sentence_temp = []
for sen in sentence:
	v = [ 0 for x in range(len(bag_of_words)) ]
	for word in sen.sentence:
		v[bag_of_words.index(word)] += 1
		global_vector[bag_of_words.index(word)] += 1
	sen.words = Vector(v)
	i = i + 1
	
global_vector = Vector(global_vector)


for sen in sentence:
	sen.weight = global_vector.cosine(sen.words)
sentence = sorted(sentence,key= lambda x: x.weight)
sentence.reverse()
summary = []
print "How many sentences : "
n = int(raw_input())
for i in range(n):
	print "\rChecking sentence (" + str(i) + ")",
	summary.append(sentence[0])
	sentence.remove(sentence[0])
	for word in sentence[0].sentence:
		global_vector[bag_of_words.index(word)] = 0;
	for sen in sentence:
		sen.weight = global_vector.cosine(sen.words)
	sentence = sorted(sentence,key = lambda x: x.weight)
	sentence.reverse()
	
	
	

for sen in summary:
	print sen.original + "(" + sen.original_file + "," + str(sen.file_position) +"," + str(sen.length) + "," + str(sen.weight) + ")"
	
# TODO(balan1.618@gmail.com): Add the sentence regeneration

# TODO: Document all functions used within our code including the once that we created		


