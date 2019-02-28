import pickle
import random
from typing import List, Tuple, Dict
from typing import Union

import pandas as pd
from sklearn.svm import LinearSVC


class SentenceClassifier(object):
    def __init__(self, acceptance_threshold: float = 0.7, trigram_importance: Union[int, float] = 3):
        self._known_bigrams = None
        self._known_trigrams = None
        self.acceptance_threshold = acceptance_threshold
        self.trigram_importance = trigram_importance
        self.log = {}
        self._fake_sentences = None
        self._human_sentences = None
        self.sentence_classifier = LinearSVC(random_state=0, tol=1e-5)
        self.load_trained_model()

    @property
    def known_bigrams(self):
        if self._known_bigrams is None:
            self._load_bigrams_trigrams()
        return self._known_bigrams

    @property
    def known_trigrams(self):
        if self._known_trigrams is None:
            self._load_bigrams_trigrams()
        return self._known_trigrams

    @property
    def fake_sentences(self):
        if self._fake_sentences is None:
            self._load_sentences()
        return self._fake_sentences

    @property
    def human_sentences(self):
        if self._human_sentences is None:
            self._load_sentences()
        return self._human_sentences

    def _load_sentences(self):
        with open("/home/jjb/Dropbox/Programming/GIT/mcts/data/false.csv", "r") as f:
            self._fake_sentences = set(filter(lambda tup: len(tup) > 0, f.read().split("\n")))
        with open("/home/jjb/Dropbox/Programming/GIT/mcts/data/true.csv", "r") as f:
            self._human_sentences = set(filter(lambda tup: len(tup) > 0, f.read().split("\n")))

    def _load_bigrams_trigrams(self):
        with open("/home/jjb/Dropbox/Programming/GIT/mcts/data/known_bigrams.csv", "r") as f:
            self._known_bigrams = set(map(lambda tup: tuple(tup.split()), filter(lambda tup: len(tup) > 0, f.read().split("\n"))))
        with open("/home/jjb/Dropbox/Programming/GIT/mcts/data/known_trigrams.csv", "r") as f:
            self._known_trigrams = set(map(lambda tup: tuple(tup.split()), filter(lambda tup: len(tup) > 0, f.read().split("\n"))))

    def sentence_is_human(self, word_sequence: List[str]) -> bool:
        """ Determine if sentence is human or fake

        :param word_sequence:
        :return: True if sentence is human, False if fake
        """
        features = self.sentence_to_features(word_sequence)
        overlap_scores = self.compute_score_overlap_with_known(bigrams=features["bigrams"], trigrams=features["trigrams"])
        # score = overlap_scores["bigram"] + self.trigram_importance * overlap_scores["trigram"]
        # self.log[" ".join(word_sequence)] = score
        # return score >= self.acceptance_threshold
        return bool(self.sentence_classifier.predict([[overlap_scores["bigram"], overlap_scores["trigram"]]])[0])

    def compute_feature(self, word_sequence: List[str]) -> bool:
        """ Determine if sentence is human or fake

        :param word_sequence:
        :return: True if sentence is human, False if fake
        """
        features = self.sentence_to_features(word_sequence)
        overlap_scores = self.compute_score_overlap_with_known(bigrams=features["bigrams"], trigrams=features["trigrams"])
        return overlap_scores

    def compute_score_overlap_with_known(self, bigrams: List[Tuple[str, str]], trigrams: List[Tuple[str, str, str]]) -> Dict:
        score_bigram = sum(list(map(lambda bigram: bigram in self.known_bigrams, bigrams))) / len(bigrams)
        score_trigram = sum(list(map(lambda trigram: trigram in self.known_trigrams, trigrams))) / len(trigrams)
        return {"bigram": score_bigram, "trigram": score_trigram}

    def train_model(self):
        training_data_false = [{"label": 0, **self.compute_feature(sentence.split())} for sentence in self.fake_sentences]
        training_data_true = [{"label": 1, **self.compute_feature(sentence.split())} for sentence in self.human_sentences]
        training_data = training_data_false + training_data_true
        random.shuffle(training_data)
        p = pd.DataFrame(training_data)
        x = p[["bigram", "trigram"]]
        y = p["label"]
        self.sentence_classifier.fit(x, y)
        print("Model trained on {t} human-like sentences and {f} fake sentences".format(t=len(training_data_true), f=len(training_data_false)))
        with open('/home/jjb/Dropbox/Programming/GIT/mcts/models/sentence_classifier.pkl', 'wb') as f:
            pickle.dump(self.sentence_classifier, f)

    def load_trained_model(self):
        with open('/home/jjb/Dropbox/Programming/GIT/mcts/models/sentence_classifier.pkl', 'rb') as f:
            self.sentence_classifier = pickle.load(f)

    def sentence_to_features(self, word_sequence):
        tokens = ["@>"] + word_sequence + ["<@"]
        bigrams = [tuple(tup) for tup in zip(tokens, tokens[1:])]
        trigrams = [tuple(trip) for trip in zip(tokens, tokens[1:], tokens[2:])]
        return {"bigrams": bigrams, "trigrams": trigrams}
