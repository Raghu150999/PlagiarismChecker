import nltk
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.tokenize import RegexpTokenizer
from paragraph import Paragraph
from document import Document
import os

def paragraph_tokenizer(text):
	output = []
	string = ""
	i = 0
	while i < len(text):
		if i < len(text)-1 and text[i] == '\n' and text[i+1] == '\n':
			output.append(string)
			string = ""
		else:
			string += text[i]
		i += 1
	output.append(string)
	return output

stop_words = set(stopwords.words('english'))

def preprocessor(text):
	# Remove punctuations
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(text)

	# Convert to lower case
	for i, token in enumerate(tokens):
		tokens[i] = token.lower()
	
	# Removing stop words
	tokens = [w for w in tokens if not w in stop_words]

	# Perform stemming
	# tokens = porter_stemmer(tokens)
	return tokens

documents = []
vocabulary = set()
for i, file in enumerate(os.listdir('corpus')):
	with open('corpus/' + file, encoding="utf8", errors='ignore') as f:
		raw = f.read()
		paras = paragraph_tokenizer(raw)
		paragraphs = []
		for j, para in enumerate(paras):
			# Preprocessing
			tokens = preprocessor(para)
			id = (i, j)
			paragraph = Paragraph(id, tokens)
			paragraphs.append(paragraph)
			for term in tokens:
				vocabulary.add(term)
		document = Document(i, paragraphs)
		documents.append(document)

# Length of vocabulary
vocabularyLength = len(vocabulary)
