from gensim.models.keyedvectors import KeyedVectors

def totalvector(p):
    finalmodel = str(p)
    model = KeyedVectors.load_word2vec_format(finalmodel, binary=True)

    docvec = model.docvecs.vectors_docs
    wordvec = model.wv.vectors
    return totalvector = np.vstack((docvec,wordvector))
