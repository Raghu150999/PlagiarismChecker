import nltk

class Paragraph:
	def __init__(self, _id, tokens):
		self.tokens = tokens
		self._id = _id
		# Creating frequency distribution as a dictionary
		self.freq_dist = dict(nltk.FreqDist(tokens))
