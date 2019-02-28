import os
import re
from typing import List
import pandas as pd
import random

class BrownCoprus(object):
    def __init__(self, path_to_brown_corpus_directory: str):
        self.path_to_dir = path_to_brown_corpus_directory
        self.sentences = []
        self.bigrams = []
        self.trigrams = []
        self.vocab = None

    def save_all(self):
        try:
            bigrams_so_far = pd.read_csv("/home/jjb/Desktop/brown/bigrams.csv", header=None)
            new = pd.Series(list(map(lambda trip: " ".join(trip), self.bigrams)))
            pd.concat([bigrams_so_far, new]).to_csv("/home/jjb/Desktop/brown/bigrams.csv", index=None, header=None)
            trigrams_so_far = pd.read_csv("/home/jjb/Desktop/brown/trigrams.csv", header=None)
            new = pd.Series(list(map(lambda trip: " ".join(trip), self.trigrams)))
            pd.concat([trigrams_so_far, new]).to_csv("/home/jjb/Desktop/brown/trigrams.csv", index=None, header=None)
            sentences_so_far = pd.read_csv("/home/jjb/Desktop/brown/sentences.csv", header=None)
            new = pd.Series(self.sentences)
            pd.concat([sentences_so_far, new]).to_csv("/home/jjb/Desktop/brown/sentences.csv", index=None, header=None)
        except:
            print("except")
            pd.Series(list(map(lambda trip: " ".join(trip), self.bigrams))).to_csv("/home/jjb/Desktop/brown/bigrams.csv", index=None, header=None)
            pd.Series(list(map(lambda trip: " ".join(trip), self.trigrams))).to_csv("/home/jjb/Desktop/brown/trigrams.csv", index=None, header=None)
            pd.Series(self.sentences).to_csv("/home/jjb/Desktop/brown/sentences.csv", index=None, header=None)

    def clear_cache(self):
        self.save_all()
        self.sentences = []
        self.bigrams = []
        self.trigrams = []

    def extract_segments_from_file(self, filename):
        with open(self.path_to_dir + "/" + filename, "r") as f:
            data = f.read().replace("\n", "")
        return re.findall(r"<p><s n=\"\d+\">(.*?)</s></p>", data)

    def extract_sentences_from_segment(self, segment):
        if "mw pos" not in segment:
            sentence = list(map(lambda tup: tup[1], re.findall(r"<w type=\".{0,4}\"( subtype=\".{0,4}\")?>(.*?)</w>", segment)))
            self.sentences.append(" ".join(sentence))
            return sentence

    def build_sentences_and_features(self):
        for filename in filter(lambda filename: filename.endswith("xml"), os.listdir(self.path_to_dir)):
            print(filename)
            all_segments = self.extract_segments_from_file(filename)
            for segment in all_segments:
                sentence = self.extract_sentences_from_segment(segment)
                if sentence:
                    self.make_features(sentence)
            self.clear_cache()
        return

    def make_features(self, word_sequence: List[str]):
        tokens = ["@>"] + word_sequence + ["<@"]
        self.bigrams.extend([tup for tup in zip(tokens, tokens[1:])])
        self.trigrams.extend([trip for trip in zip(tokens, tokens[1:], tokens[2:])])


    def build_vocab(self):
        sentences_so_far = pd.read_csv("/home/jjb/Desktop/brown/sentences.csv", header=None)
        self.vocab = list(set(" ".join(list(sentences_so_far[0])).split()))

    def generate_a_sentence(self):
        sentence_length = random.randint(4,15)
        return " ".join(random.choices(self.vocab, k=sentence_length))

    def build_false_data(self, dataset_size=10000):
        pd.Series([self.generate_a_sentence() for _ in range(dataset_size)]).to_csv("/home/jjb/Desktop/brown/false.csv", header=None, index=None)



if __name__ == "__main__":
    B = BrownCoprus("/home/jjb/Desktop/brown/brown_tei")
    # B.build_sentences_and_features()
    B.build_vocab()
    B.build_false_data(100)