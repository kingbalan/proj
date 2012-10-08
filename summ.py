

import nltk.data
from nltk.corpus import stopwords
import re
from nltk.stem.wordnet import WordNetLemmatizer
class sentenceRepresentation:
	sentence = []
	words = []
	
	def __init__(self,sen=[],word=[]):
		self.sentence = sen
		self.words = word

def removeStopwords(sentence):
	ret = []
	stmr = WordNetLemmatizer()
	for sen in sentence:
		sen = [ stmr.lemmatize(word.lower(),'v') for word in re.sub("[^\w]"," ",sen).split() if word.lower() not in stopwords.words('english') ]
		ret.append(sen)
	return ret
	

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("test.txt")
data = fp.read()
data = tokenizer.tokenize(data)
sentence = []
for sen in data:
	sentence.append(sen)
fp.close()
fp = open("test2.txt")
data = fp.read()
data = tokenizer.tokenize(data)
for sen in data:
	sentence.append(sen)

sentence = removeStopwords(sentence)

bag_of_words = []
for sen in sentence:
	for word in sen:
		if word not in bag_of_words:
			bag_of_words.append( word )
sentence_temp = []
for sen in sentence:
	a = sentenceRepresentation()
	li = []
	for word in sen:
		if word not in a.words:
			li.append(word)
		a.sentence = sen
	sentence_temp.append(sentenceRepresentation(a.sentence,li))
	
sentence = sentence_temp

sentence = sorted(sentence,key= lambda x: len(x.words))
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
			if w in sen.words:
				sen.words.remove(w)
	sentence = sorted(sentence,key = lambda x:len(x.words))
	sentence.reverse()

for sen in summary:
	print sen
	print "\n"
	
		


