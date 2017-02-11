

import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt

import numpy



args = sys.argv[1:]
try:
	arg,opt = getopt.getopt(args,"h")
	
except getopt.GetoptError:
	usage()
	sys.exit(1)
if len(opt) == 0:
	usage()
	sys.exit(1)
	

def removeStopwords(sentence):
	'''Remove Stop words and stem the sentence. It also splits the sentences into words before stemming. '''
	# TODO(cliveverghese@gmail.com) : Add part of speach to each word hence produceds
	ret = []
	orig = []
	stmr = WordNetLemmatizer()
	sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sentence).split() if word.lower() not in stopwords.words('english') ]
	return sen


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentence = []
document_vector = []
doc_vec = [];
file_names ={}

j=0
total_sentences = 0
for tempfile in opt:
	fp = open(tempfile)
	file_names[tempfile] = j;
	data = fp.read()
	data = tokenizer.tokenize(data)
	i = 0
	tl = []
	for sen in data:
		#print "(" + str(i) + ")" + sen
		bog = removeStopwords(sen)
		tl.append(bog);
		sentence.append(sentenceRepresentation(bog,0,sen,tempfile,i))
		i = i + 1
	fp.close()
	doc_vec.append(tl)
	total_sentences += i
	j += 1