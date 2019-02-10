import random
from typing import List, Tuple, Dict


class SentenceClassifier(object):
    def __init__(self):
        self._known_bigrams = None
        self._known_trigrams = None
        self.acceptence_threshold = 0.2

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

    def _load_bigrams_trigrams(self):
        with open("data/known_bigrams", "r") as f:
            self._known_bigrams = list(map(lambda tup: tuple(tup.split()),filter(lambda tup: len(tup) > 0, f.read().split("\n"))))
        with open("data/known_trigrams", "r") as f:
            self._known_trigrams = list(map(lambda tup: tuple(tup.split()),filter(lambda tup: len(tup) > 0, f.read().split("\n"))))

    def sentence_is_human(self, word_sequence: List[str]) -> bool:
        """ Determine if sentence is human or fake

        :param word_sequence:
        :return: True if sentence is human, False if fake
        """
        features = self.sentence_to_features(word_sequence)
        overlap_scores = self.compute_score_overlap_with_known(bigrams=features["bigrams"], trigrams=features["trigrams"])
        trigram_importance = 2
        score = overlap_scores["bigram"] + trigram_importance * overlap_scores["trigram"]
        return score >= self.acceptence_threshold

    def compute_score_overlap_with_known(self, bigrams: List[Tuple[str, str]], trigrams: List[Tuple[str, str, str]]) -> Dict:
        score_bigram = sum(list(map(lambda bigram: bigram in self.known_bigrams, bigrams)))/len(bigrams)
        score_trigram = sum(list(map(lambda trigram: trigram in self.known_trigrams, trigrams)))/len(trigrams)
        return {"bigram": score_bigram, "trigram": score_trigram}


    def sentence_to_features(self, word_sequence):
        tokens = ["@>"] + word_sequence + ["<@"]
        bigrams = [tuple(tup) for tup in zip(tokens, tokens[1:])]
        trigrams = [tuple(trip) for trip in zip(tokens, tokens[1:], tokens[2:])]
        return {"bigrams": bigrams, "trigrams": trigrams}
