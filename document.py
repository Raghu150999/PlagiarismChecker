class Document:
	"""
	This class is an abstraction for document and holds one or many paragraphs.
	Attributes:
		id: uniques identifier for the document in the corpus
		paras: list of Paragraph (see Paragraph class)
	"""
	def __init__(self, _id, paras):
		"""
		Constructor for Document class
		"""
		self._id = _id
		self.paras = paras