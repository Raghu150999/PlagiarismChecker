import nltk
from nltk.corpus import PlaintextCorpusReader
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

i = 0
documents = []
for i, file in enumerate(os.listdir('corpus')):
	with open('corpus/' + file, encoding="utf8", errors='ignore') as f:
		raw = f.read()
		paras = paragraph_tokenizer(raw)
		paragraphs = []
		for j, para in enumerate(paras):
			tokens = nltk.word_tokenize(para)
			id = (i, j)
			paragraph = Paragraph(id, tokens)
			paragraphs.append(paragraph)
		document = Document(i, paragraphs)
		documents.append(document)

