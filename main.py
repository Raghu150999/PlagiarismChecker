import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.tokenize import RegexpTokenizer
from paragraph import Paragraph
from document import Document
from indexer import Indexer
import os
import sys

def paragraph_tokenizer(text):
    """
    Parameters:
    str(text): raw text from a document
    Decomposes raw text into paragraphs
    """
    output = []
    string = ""
    i = 0
    while i < len(text):
        if i < len(text) and text[i] == '\n':
            if string != "\n" and string != "":
                output.append(string)
            string = ""
        else:
            string += text[i]
        i += 1
    if string != "\n" and string != "":
        output.append(string)
    return output

def preprocessor(text):
    """
    Parameters:
    str (text): raw text
    Performs preprocessing operations: tokenize, lowercase, remove stopwords, stemming (porter stemmer)
    """
    # Remove punctuations
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    # Convert to lower case
    for i, token in enumerate(tokens):
        tokens[i] = token.lower()
    
    # Removing stop words
    tokens = [w for w in tokens if not w in stop_words]

    # Perform stemming
    for i, token in enumerate(tokens):
        tokens[i] = stemmer.stem(token)
    return tokens


if __name__ == '__main__':
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    documents = []
    vocabulary = set()
    files = os.listdir('corpus')
    for i, file in enumerate(files):
        with open('corpus/' + file, encoding="utf8", errors='ignore') as f:
            raw = f.read()
            paras = paragraph_tokenizer(raw)
            paragraphs = []
            for j, para in enumerate(paras):
                # Preprocessing
                tokens = preprocessor(para)
                _id = (i, j)
                paragraph = Paragraph(_id, tokens)
                paragraphs.append(paragraph)
                for term in tokens:
                    vocabulary.add(term)
            document = Document(i, paragraphs)
            documents.append(document)

    # Length of vocabulary
    vocabularyLength = len(vocabulary)
    # print(vocabularyLength)
    
    # Creating the inverted index
    indexer = Indexer(documents)

    # Take filename as input for processing
    inputDocument = str(sys.argv[1])
    # inputDocument = 'test.txt'
    raw = None
    with open(inputDocument, encoding="utf8", errors="ignore") as input_file:
        raw = input_file.read()
    paras = paragraph_tokenizer(raw)
    paragraphs = []
    for j, para in enumerate(paras):
        tokens = preprocessor(para)
        _id = (-1, j) # -1 so that it is different from other documents in the corpus
        paragraph = Paragraph(_id, tokens)
        paragraphs.append(paragraph)
    input_doc = Document(-1, paragraphs)
    top_k, uniqueness = indexer.evaluate_input(input_doc, files, 10)
    for i in range(len(top_k)):
        score, filename = top_k[i]
        print('Document: ' + str(filename), 'Score: ' + str(score))
    print('Uniqueness: ' + str(uniqueness) + ' %')