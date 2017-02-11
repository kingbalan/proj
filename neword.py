#!/usr/bin/python

#Main Program

import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt
from scipy.cluster import hierarchy
import numpy



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


def vectorise(sent,bag_of_words):
	v =  [0 for x in range(len(bag_of_words)) ]
	for word in sent:
			if word in bag_of_words:
				v[bag_of_words.index(word)] += 1
	return v
	



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
document_vector = []
doc_vec = [];
file_names ={}

j=0
k=0


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
		if(bog[0] == 'p'):
			bog[0] = ' '
			tl.append(bog);
		else :
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
	document_vector.append(v)
	i = i + 1
	
X = numpy.array(document_vector)    #Convert list to Matrix For Use in Clustering of sentences
#print X
Z = hierarchy.linkage(X,method="single",metric="cosine")
Z = numpy.clip(Z,0,10000000)
#print Z
res = hierarchy.fcluster(Z,1.5,depth=6)
#res = hierarchy.fclusterdata(X,1.5,depth=4,metric="cosine",method="single")	

num_sen_cluster = {}
cent_cluster = {}
total_sen = 0
for i in range(len(res)):
	sentence[i].group = res[i]
	if not num_sen_cluster.has_key(res[i]):
		num_sen_cluster[res[i]] = 0
		temp_list = [0 for x in range(len(bag_of_words)) ]
		temp_vector = Vector(temp_list)
		cent_cluster[res[i]] = temp_vector
	cent_cluster[res[i]] += sentence[i].words
	num_sen_cluster[res[i]] += 1
	total_sen += 1

#for i in range(1,len(num_sen_cluster) + 1):
#	for j in range(len(cent_cluster[i].data)):
#		cent_cluster[i].data[j] = cent_cluster[i].data[j] / num_sen_cluster[i]

temp_global_vector = Vector(global_vector)
global_vector = Vector(global_vector)



#for sen in sentence:
#	sen.weight = cent_cluster[sen.group].cosine(sen.words)
#	print sen.weight, sen.original

sentence = sorted(sentence,key= lambda x: x.group)
#print cent_cluster
print total_sen
print res
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
sen_prev = sentence[:]
sentence = []
print num_sen_cluster
for i in range(1,len(cent_cluster) + 1):
	temp_sen = []
	temp_summary = []
	temp_vector = Vector([x for x in range(len(bog)) ])
	for j in sen_prev:
		if j.group == i:
			#print "Adding Sentence"
			temp_sen.append(j)
	num_sen = n * num_sen_cluster[i]/total_sen
	j = 0
	print n * (int(num_sen_cluster[i])/int(total_sen))
	if num_sen_cluster[i] > 1:
		num_sen += 1

	#print "Extracting " + str(num_sen)
	while len(temp_sen) > 0 and j < num_sen :
		temp_sen = sorted(temp_sen,key = lambda x: x.weight)
		if temp_vector.cosine(temp_sen[0].words) < 0.8:
			temp_vector += temp_sen[0].words
			temp_summary.append(temp_sen[0])
			j += 1
		temp_sen.remove(temp_sen[0])
	for j in range(len(temp_summary)):
		sentence.append(temp_summary[j])
		
#print sentence

#while len(sentence) > n :
#	prev_len = len(sentence)
#	while sentence[0].weight < fact + 0.10:
#		print "Removing sentence with weight " + str(sentence[0].weight) 
#		temp_global_vector = temp_global_vector - sentence[0].words
#		sentence.remove(sentence[0])
#	for sen in sentence:
#		flag = 0
#		for sen1 in sentence:
#			temp = sen1.words.cosine(sen.words)
#			if temp > 0.40 - fact and sentence.index(sen) != sentence.index(sen1):
#				flag = 1
#		if flag == 1:
#			print "Removing redundant sentence with " + str(temp)
#			#temp_global_vector = temp_global_vector - sen.words
#			sentence.remove(sen)
#	for sen in sentence:
#		sen.weight = temp_global_vector.cosine(sen.words)		
#	fact += 0.01




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
print "\n"
print "\n"


year_sent = []


#Getting the year out

for sent in sentence:
	string = str(sent.original)
	res = re.findall("(year|in|In) ([1-3][0-9]{3})",string)
	year = 0

	if len(res)>0:
		print res
		sent.year = res[0][1][0:4]
		sentence.remove(sent)
		year_sent.append(sent)

year_sent = sorted(year_sent,key = lambda x: x.year)	





ordered = []

ordered.append(sentence[0]);
sentence = sentence[1:len(sentence)];

n_ordered = 0


param = 3

top = 0


while len(sentence) > 0:

	temp = ordered[n_ordered]

	top =0
	for sen in sentence:

		i = 0;
		tot =0
		
		while(doc_vec[file_names[temp.original_file]][i+temp.file_position +1 ][0] != ' ' and i<param  and temp.file_position +i <= len(doc_vec[file_names[sen.original_file]]) ):
			v = vectorise(  doc_vec[file_names[temp.original_file]][i+temp.file_position +1 ] ,bag_of_words)
			val =  Vector(v).cosine(sen.words)
			
			tot += val

			i += 1
			
		
		#print tot
		
		if(i>0):
			tot = tot /i

		if(tot > top):
			top = tot
			top_index = sen




	#print top 
	print top
	if(top > 0):
		ordered.append(top_index)
		sentence.remove(top_index)
		n_ordered += 1
	else:

		print "else"
		top = 0
		for sent in sentence:
			val = temp.words.cosine(sent.words)
			print val
			if(val >top ):
				top_index = sent
				top = val
		if(top > 0):
			ordered.append(top_index)
			sentence.remove(top_index)
			n_ordered += 1
		else:
			ordered.remove(temp)
			n_ordered -= 1



i = 0
for sent in ordered:
	print str(i)+" : "+sent.original
	i+=1

print "\n"

for sent in year_sent:
	print sent.original

param2 =len(ordered) / 2

ind = 1

for sent in year_sent:
	maxval =0
	if(ind + param2 < len(ordered)):
		j = ind +param2
	else:
		j = len(ordered)
	tmp = ind
	for i in range(ind,j):
		
		val = sent.words.cosine(ordered[i].words)
		if(val > maxval):
			maxval = val
			tmp = i
	

	ind = tmp +1
	print ind









