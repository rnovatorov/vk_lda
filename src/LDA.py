from datetime import datetime
from gensim import corpora, models


class LDA(object):
    """
    Clusterize docs into topics using latent Dirichlet allocation
    """
    def __init__(self, docs, num_topics, passes):
        self.docs = docs
        self.num_topics = num_topics
        self.passes = passes

        self.dictionary = corpora.Dictionary(self.docs)
        self.corpus = [self.dictionary.doc2bow(d) for d in self.docs]
        self.lda = models.ldamodel.LdaModel(self.corpus,
                                            num_topics=self.num_topics,
                                            id2word=self.dictionary,
                                            passes=self.passes)

    def get_topics(self):
        """
        Returns topics in the following format:
        [
          [(word1, prob1), (word2, prob2), ..., (wordn, probn)],
          [(word1, prob1), (word2, prob2), ..., (wordn, probn)],
          ...
          [(word1, prob1), (word2, prob2), ..., (wordn, probn)]
        ]
        """
        topics = self.lda.show_topics(formatted=False)
        return [t[1] for t in topics]

    def print_topics(self):
        """
        Prints topics in the following format:

        Topic 1:
            Word: w1                Prob: p1
            Word: w2                Prob: p2
            ...
            Word: wn                Prob: pn

        Topic 2:
            Word: w1                Prob: p1
            Word: w2                Prob: p2
            ...
            Word: wn                Prob: pn

        ...

        Topic m:
            Word: w1                Prob: p1
            Word: w2                Prob: p2
            ...
            Word: wn                Prob: pn

        """
        for n, topic in enumerate(self.get_topics()):
            print("Topic %d:" % (n + 1))
            for word, prob in topic:
                print(("    Word: %s" % word[:20]).ljust(30) +
                       "Prob: %.5f" % prob)
            print("\n")

    def save_html(self, name, path):
        """
        Saves visualisation in html format
        """

        print("\nSaving result...")

        # Making vis
        import pyLDAvis.gensim
        vis = pyLDAvis.gensim.prepare(self.lda,
                                      self.corpus,
                                      self.dictionary)

        # Making filename
        date = datetime.today().strftime("%Y%m%d%H%M")
 
        name = "%s/LDA_%s_%d_%d_%s.html" % (
            path, name, self.num_topics, self.passes, date
        )

        # Saving
        pyLDAvis.save_html(vis, name)
