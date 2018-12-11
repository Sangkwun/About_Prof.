yedvectors import KeyedVectors

finalmodel = 'finalmodel'
model = KeyedVectors.load_word2vec_format(finalmodel, binary=True)

def parametertunning(v):
    model = gensim.models.Doc2Vec(vector_size=v, window=10, min_count=1, workers=8, alpha=0.025, min_alpha=0.015,
                              epochs=20)
    profname = list(model.docvecs.doctags.keys())
    final = []
    for j in profname:
        count = 0
        mostsimilar = model.docvecs.most_similar(j)
        for a,b in mostsimilar:
            if a.split('/')[1] == i.split('/')[1]:
                count += 1
            else:
                pass
        final.append(count)
        average = sum(final)/len(final)
        return average

for i in range(1,200, 20):
    print(parametertunning(i))