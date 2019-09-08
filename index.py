import nltk
from nltk.corpus import PlaintextCorpusReader
# Need to download these first
# nltk.download('punkt')
# nltk.download('stopwords')
sentence = '''Hi, folks how is it going. \
Folks wassup'''
tokens = nltk.word_tokenize(sentence)
text = nltk.Text(tokens)
text.concordance('folks')
print(tokens)
print(list(nltk.bigrams(text))) # get bigrams
f = open('corpus/g0pA_taska.txt', 'r')
raw = f.read()
tokens = nltk.word_tokenize(raw)
text = nltk.Text(tokens)
text.concordance('the')
# vocabulary size, "set()" removes repetitions
print(len(set(text)))
fdist = nltk.FreqDist(text)
print(list(fdist)) # frequency of tokens
corpus_root = 'corpus/'
# loading the corpus strict regx would be: '([a-z]|[0-9]|[A-Z]|_)*.txt'
filelists = PlaintextCorpusReader(corpus_root, '.*.txt')
# print(filelists.fileids())