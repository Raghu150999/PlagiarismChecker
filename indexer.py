import math

class Indexer:
	"""
	Indexer is responsilbe for creation of the inverted index
	Attributes:
		documents: list of all documents in the entire corpus
		invertedIndex: dictionary of term to posting lists
		df: dictionary of term to document frequency
		nop: number of paragraphs in the corpus
		nc: normalization coefficient (dictionary)
	"""
	def __init__(self, documents):
		"""
		Constructor for Indexer
		list (documents): all documents in the corpus
		"""
		self.documents = documents
		# create indexing here
		invertedIndex = {}
		# document (in this case document unit is paragraph) frequency
		df = {}
		# Variable for number of paragraphs in the corpus
		nop = 0
		# Normalization coefficients
		nc = {}
		for i, doc in enumerate(documents):
			for j, para in enumerate(doc.paras):
				for term in para.freq_dist:
					nop += 1
					obj = {"id": (i, j), "tf": para[term]}
					# Updating document frequency
					if df.get(term):
						df[term] += 1
					else:
						df[term] = 1
					# Adding current para to the posting list of the 'term'
					if invertedIndex.get(term):
						invertedIndex[term].append(obj)
					else:
						invertedIndex[term] = [obj]
		# Normalization coefficient calculations
		for term in invertedIndex:
			for obj in invertedIndex[term]:
				t = obj["id"]
				tf = obj["tf"]
				tf_idf = tf * math.log(nop/df[term])
				if nc.get(t):
					nc[t] += tf_idf * tf_idf
				else:
					nc[t] = tf_idf * tf_idf
		for term in nc:
			nc[term] = math.sqrt(nc[term])
		self.df = df
		self.invertedIndex = invertedIndex
		self.nop = nop
		self.nc = nc