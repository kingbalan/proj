from Vector import *

class sentenceRepresentation:
	sentence = []
	words = 0
	
	def __init__(self,sen=[],word=[]):
		self.sentence = sen
		self.words = Vector(word)
