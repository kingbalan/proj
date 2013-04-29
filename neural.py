#!/usr/bin/python
import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *

from Vector import *

import neurolab as nl
import numpy as np
from neurolab.tool import minmax



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
	

def addvector(v1,v2):
	for i in range(0,len(v1)):
		v1[i] += v2[i]
	return v1

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentence = []
document_vector = []
doc_vec = [];
file_names ={}

j=0
k=0
total_sentences = 0

tempfile = "e/e5.txt"

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

print bag_of_words


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

print global_vector

inp =[]

for sent in sentence:
	inp.append( vectorise(sent.sentence,bag_of_words) )



tar =[]

param = 3

for temp in sentence:
		i=0
		x =  [0 for j in range(len(bag_of_words)) ] 
		while(doc_vec[file_names[temp.original_file]][i+temp.file_position +1 ][0] != ' ' and i<param  and temp.file_position +i <= len(doc_vec[file_names[temp.original_file]]) ):
			v = vectorise(  doc_vec[file_names[temp.original_file]][i+temp.file_position +1 ] ,bag_of_words)
			x = addvector(x,v)
			i+=1
		
		tar.append(x)
	
		

"""




# Create train samples
input = [[0,0],[0,1],[1,0],[1,1]]
target = [[0,0],[1,1],[1,1],[0,0]]


print input
"""

"""
inp = inp[0:2]
tar = tar[0:2]

for i in range(0,2):
	inp[i] = inp[i][0:20]
	tar[i] = tar[i][0:20]
"""

l = len(bag_of_words)

print l

inp = np.reshape(inp,(-1,l))


print tar[1]
print inp

#target = np.reshape(target,(-1,1))

# Create network with 2 layers and random initialized
#norm = Norm(input)
#input = norm(input)


net = nl.net.newff(minmax(inp), [10, l], transf = [nl.trans.TanSig(), nl.trans.LogSig()])
net.trainf = nl.train.train_bfgs

error = net.train(inp, tar, epochs=10, show=5, goal=0.01)
"""
test = [0,1]

test = np.reshape(test,(-1,2))

out = net.sim(test)

print out


"""