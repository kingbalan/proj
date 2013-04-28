import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
from classes import *
import sys,getopt
from scipy.cluster import hierarchy
import numpy

def sumarize(document_vector,sentence,n,bag_of_words):
	X = numpy.array(document_vector)    #Convert list to Matrix For Use in Clustering of sentences
	#print X
	Z = hierarchy.linkage(X,method="single",metric="cosine")
	Z = numpy.clip(Z,0,10000000)
	#print Z
	res = hierarchy.fcluster(Z,n,depth=6,criterion="maxclust")
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
	
	#temp_global_vector = Vector(global_vector)
	#global_vector = Vector(global_vector)
	
	
	
	#for sen in sentence:
	#	sen.weight = cent_cluster[sen.group].cosine(sen.words)
	#	print sen.weight, sen.original
	
	sentence = sorted(sentence,key= lambda x: x.group)
	#print cent_cluster
	print total_sen
	print res
	#raw_input()
	
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
		#print "Iterating i = " + str(i)
		temp_sen = []
		temp_summary = []
		temp_vector = Vector([x for x in range(len(bag_of_words)) ])
		for j in sen_prev:
			if j.group == i:
				#print "Adding Sentence"
				temp_sen.append(j)
		#num_sen = n * num_sen_cluster[i]/total_sen
		num_sen = 1
		j = 0
		round(num_sen)
		print "Extracting " + str(num_sen) + " from cluster " + str(i)
		#print n * (int(num_sen_cluster[i])/int(total_sen))
		#if num_sen_cluster[i] > 1:
			#num_sen += 1
	
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
		
	return sentence
	
