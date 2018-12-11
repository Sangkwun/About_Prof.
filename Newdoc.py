import numpy as np
import preprocessing

class Newdoc(object):
    def __init__(self, model):
        self.model = model

    def wordvectorize(self, doc):
        # Identify the vector values for each word in the given document
        words = preprocessing.docs_preprocessor(doc)
        word_vecs = []
        for word in words:
            try:
                vec = self.model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        docvector = np.mean(word_vecs, axis=0)
        return docvector