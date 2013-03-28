from Vector import *

class sentenceRepresentation:
	sentence = []
	original = []
	words = 0
	score = 0
	
	def __init__(self,sen=[],word=[],orig=[],original_file="",file_position=0):
		self.original = orig
		self.sentence = sen
		self.words = Vector(word)
		self.score = 0
		self.weight = 0
		self.relevane = 0
		self.cluster = 0
		self.original_file = original_file
		self.file_position = file_position
		self.length = len(sen)
		

