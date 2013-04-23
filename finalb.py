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
	
temp_global_vector = Vector(global_vector)
global_vector = Vector(global_vector)



for sen in sentence:
	sen.weight = global_vector.cosine(sen.words)

sentence = sorted(sentence,key= lambda x: x.weight)

print "How many sentences : "
n = int(raw_input())
#for i in range(n):
#	print "\rChecking sentence (" + str(i) + ")",
#	summary.append(sentence[0])
#	summary_vector = summary_vector + sentence[0].words
#	for word in sentence[0].sentence:
#		temp_global_vector[bag_of_words.index(word)] = 0;
#	sentence.remove(sentence[0])
#	
#	for sen in sentence:
#		sen.score = temp_global_vector.cosine(sen.words)
#		sen.relevance = sen.score
#	sentence = sorted(sentence,key = lambda x: x.relevance)
#	sentence.reverse()
prev_len = len(sentence) + 1
fact = 0

while len(sentence) > n :
	prev_len = len(sentence)
	while sentence[0].weight < fact + 0.10:
		print "Removing sentence with weight " + str(sentence[0].weight) 
		temp_global_vector = temp_global_vector - sentence[0].words
		sentence.remove(sentence[0])
	for sen in sentence:
		flag = 0
		for sen1 in sentence:
			temp = sen1.words.cosine(sen.words)
			if temp > 0.40 - fact and sentence.index(sen) != sentence.index(sen1):
				flag = 1
		if flag == 1:
			print "Removing redundant sentence with " + str(temp)
			#temp_global_vector = temp_global_vector - sen.words
			sentence.remove(sen)
	for sen in sentence:
		sen.weight = temp_global_vector.cosine(sen.words)		
	fact += 0.01




print "\rSummary Of the given text"

"""i = max(global_vector.data)
printed = 0
while printed < 3:
	for t in range(len(global_vector.data)):
		if 	global_vector[t] == i:
			print bag_of_words[t] + " ",
			printed += 1
	i -= 1	
"""

print "\n"
for sen in sentence:
	print sen.original + "(" + sen.original_file + "," + str(sen.file_position) +"," + str(sen.length) + "," + str(sen.weight) + ")"


#Ordering by file position	
sentence = sorted(sentence,key = lambda x: x.file_position)



print "\n"
for sen in sentence:
	print sen.original + "(" + sen.original_file + "," + str(sen.file_position) +"," + str(sen.length) + "," + str(sen.weight) + ")"
	for i in range(0,sen.file_position) :
		for word in doc_vec[file_names[sen.original_file]][i]:
			v =  [0 for x in range(len(bag_of_words)) ]
			if word in bag_of_words:
				v[bag_of_words.index(word)] += 1
		print Vector(v).cosine(sen.words)


for sen in sentence:
	print sen.original + "(" + sen.original_file + "," + str(sen.file_position) +"," + str(sen.length) + "," + str(sen.weight) + ")"

	for i in range(sen.file_position+1,len(doc_vec[file_names[sen.original_file]])) :
		for word in doc_vec[file_names[sen.original_file]][i]:
			v =  [0 for x in range(len(bag_of_words)) ]
			if word in bag_of_words:
				v[bag_of_words.index(word)] += 1
		print Vector(v).cosine(sen.words)	



	
# TODO(balan1.618@gmail.com): Add the sentence reordering

# TODO: Document all functions used within our code including the once that we created		


