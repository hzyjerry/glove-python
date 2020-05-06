# Cooccurrence matrix construction tools
# for fitting the GloVe model.
import numpy as np
try:
    # Python 2 compat
    import cPickle as pickle
except ImportError:
    import pickle

from .corpus_cython import construct_cooccurrence_matrix, construct_pmi_matrix
# from .corpus_cython import construct_cooccurrence_matrix


class Corpus(object):
    """
    Class for constructing a cooccurrence matrix
    from a corpus.

    A dictionry mapping words to ids can optionally
    be supplied. If left None, it will be constructed
    from the corpus.
    """

    def __init__(self, dictionary=None):

        self.dictionary = {}
        self.dictionary_supplied = False
        self.matrix = None
        self.pmi = None

        if dictionary is not None:
            self._check_dict(dictionary)
            self.dictionary = dictionary
            self.dictionary_supplied = True

    def _check_dict(self, dictionary):

        if (np.max(list(dictionary.values())) != (len(dictionary) - 1)):
            raise Exception('The largest id in the dictionary '
                            'should be equal to its length minus one.')

        if np.min(list(dictionary.values())) != 0:
            raise Exception('Dictionary ids should start at zero')

    def fit(self, corpus, window=10, ignore_missing=False):
        """
        Perform a pass through the corpus to construct
        the cooccurrence matrix.

        Parameters:
        - iterable of lists of strings corpus
        - int window: the length of the (symmetric)
          context window used for cooccurrence.
        - bool ignore_missing: whether to ignore words missing from
                               the dictionary (if it was supplied).
                               Context window distances will be preserved
                               even if out-of-vocabulary words are
                               ignored.
                               If False, a KeyError is raised.
        """

        self.matrix, self.pmi = construct_pmi_matrix(corpus,
                                        self.dictionary,
                                        int(self.dictionary_supplied),
                                        int(window),
                                        int(ignore_missing),
                                        positive=False)


    def save(self, model_name, pmi_name=None):
        import pdb; pdb.set_trace()
        with open(model_name, 'wb') as savefile: pickle.dump((self.dictionary, self.matrix), savefile)
        if pmi_name:
            with open(pmi_name, 'wb') as savefile: pickle.dump((self.pmi), savefile)

    @classmethod
    def load(cls, model_name, pmi_name=None):

        instance = cls()

        with open(model_name, 'rb') as savefile:
            instance.dictionary, instance.matrix = pickle.load(savefile)
        if pmi_name:
            with open(pmi_name, 'rb') as savefile:
                instance.pmi = pickle.load(savefile)

        return instance
