#!/usr/bin/python

from numpy import matrix
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
	for sen in sentence:
		orig.append(sen)
		sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sen).split() if word.lower() not in stopwords.words('english') ]
		ret.append(sen)
	return ret,orig
	
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
for tempfile in opt:
	fp = open(tempfile)
	data = fp.read()
	data = tokenizer.tokenize(data)

	for sen in data:
		sentence.append(sen)
	fp.close()


sentence,original_sentence = removeStopwords(sentence)
bag_of_words = []
for sen in sentence:
	for word in sen:
		if word not in bag_of_words:
			bag_of_words.append( word )

global_vector = [0 for x in range(len(bag_of_words)) ]
sentence_temp = []
B = []
i = 0
for sen in sentence:
	v = [ 0 for x in range(len(bag_of_words)) ]
	for word in sen:
		v[bag_of_words.index(word)] += 1
		global_vector[bag_of_words.index(word)] += 1	
	if len(sen) > 0:	
		sentence_temp.append(sentenceRepresentation(sen,v,original_sentence[i]))
		B.append(v)
	i = i + 1

sentence = sentence_temp
global_vector = Vector(global_vector)

#sentence = sorted(sentence,key= lambda x: global_vector.cosine(x.words))

summary = []
print "How many sentences : "
n = int(raw_input())

B = matrix(B)
print B
B0 = B.T*B
B0 = B0/.7
for i in range(n):
  for j in range(len(sentence)):
  	temp = B0.T[j]*B0.T[j].T
  	sentence[j].score = temp[0,0] / (1 + B[j,j])
	sentence = sorted(sentence,key = lambda x:x.score)
	sentence.reverse()
  summary.append(sentence[0].original)
  temp = B0.T[j].T*B0.T[j]
  temp = temp / (1 + B[j,j])
  B0 = B0 - temp




	


for sen in summary:
	print sen
	print "\n"
	
# TODO(balan1.618@gmail.com): Add the sentence regeneration

# TODO: Document all functions used within our code including the once that we created		


