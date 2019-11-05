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
                    _id = (i, j)
                    tf = para.freq_dist[term]
                    obj = {"id": _id, "tf": tf}
                    wt = (1 + math.log(tf))
                    if nc.get(_id):
                        nc[_id] += wt * wt
                    else:
                        nc[_id] = wt * wt
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
        for _id in nc:
            nc[_id] = math.sqrt(nc[_id])
        self.df = df
        self.invertedIndex = invertedIndex
        self.nop = nop
        self.nc = nc
    
    def evaluate_input(self, input_doc, files, K):
        '''
        score[(i, j, k)] - denotes cosine score between paragraph (i, j) in corpus and paragraph k from input document
        docScore[(i, k)] - denotes cosine score between document i and paragraph k in input document
        unique[k] - denotes how unique paragraph k of the input document is
        finalScore[i] - denotes score/similarity of document i with input document
        ncd[k] - normalisation constant for vector of paragraph k
        function returns file names of the top k matching documents
        '''
        score = {}
        docScore = {}
        finalScore = {}
        unique = {}
        # Normalization constants for input paragraph vectors
        ncd = {}
        # Repeated traversal of inverted index can be optimized?
        # Weight of paragraph (# of words) can be used to give weightage to similarity for bigger paragraphs
        for k, para in enumerate(input_doc.paras):
            ncd[k] = 0
            for term in para.freq_dist:
                # If term not present in the corpus
                if not self.df.get(term):
                    continue
                tfd = para.freq_dist[term]
                tf_idf = (1 + math.log(tfd)) * math.log(self.nop / self.df[term])
                ncd[k] += tf_idf * tf_idf
                for obj in self.invertedIndex[term]:
                    i, j = obj['id']
                    tf = obj['tf']
                    wt = (1 + math.log(tf))
                    if score.get((i, j, k)):
                        score[(i, j, k)] += wt * tf_idf
                    else:
                        score[(i, j, k)] = wt * tf_idf
        
        for i, j, k in score:
            score[(i, j, k)] /= self.nc[(i, j)] * math.sqrt(ncd[k])
            if docScore.get((i, k)):
                docScore[(i, k)] = max(docScore[(i, k)], score[(i, j, k)])
            else:
                docScore[(i, k)] = score[(i, j, k)]
            if unique.get(k):
                unique[k] = min(unique[k], 1 - docScore[(i, k)])
            else:
                unique[k] = 1 - docScore[(i, k)]
        
        for i, k in docScore:
            if finalScore.get(i):
                finalScore[i] += docScore[(i, k)] * input_doc.paras[k].size / input_doc.size
            else:
                finalScore[i] = docScore[(i, k)] * input_doc.paras[k].size / input_doc.size

        uniqueness = 0
        for k in unique:
            uniqueness += unique[k] * input_doc.paras[k].size
        uniqueness /= input_doc.size
        uniqueness *= 100
        ranks = []
        for i in finalScore:
            p = (finalScore[i], files[i])
            ranks.append(p)
        ranks.sort(reverse=True)
        l = min(len(ranks), K)
        ranks = ranks[:l]
        return ranks, uniqueness
        