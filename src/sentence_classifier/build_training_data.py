import re


class TrainingDataBuilder(object):
    special_chars_no_whitespace = {'`', '~', '$', '%', '^', '&', '*', '_', '-', '+', '=', '|', '\\', '"', '\'', '<', ',', '>', '/', '#'}
    special_chars_with_whitespace = {',', '.', ';', ':', '?', '!', '{', '[', '}', '}', '(', ')', '”', '–'}

    def __init__(self,path_true_sentences: str, path_false_sentences: str):
        self.path_sentences_true = path_true_sentences
        self.path_sentences_false = path_false_sentences
        self._sentences_true = None
        self._sentences_false = None
        self._known_bigrams = None
        self._known_trigrams = None

    @property
    def sentences_true(self):
        if self._sentences_true is None:
            self._read_sentences()
        return self._sentences_true

    @property
    def sentences_false(self):
        if self._sentences_false is None:
            self._read_sentences()
        return self._sentences_false

    def _read_sentences(self):
        with open(self.path_sentences_true, "r") as f:
            self._sentences_true = f.read()
        with open(self.path_sentences_false, "r") as f:
            self._sentences_false = f.read()

    def clean_sentence(self, sentence):
        sentence = " ".join(filter(lambda word: not word.startswith("http") and not word.startswith("www."), sentence.split()))
        for char in self.special_chars_no_whitespace:
            sentence = sentence.replace(char, "")
        for char in self.special_chars_with_whitespace:
            sentence = sentence.replace(char, " ")
        sentence = re.sub(' +', ' ', sentence)
        return sentence.lower()

    def make_features(self, sentence):
        tokens = ["@>"] + self.clean_sentence(sentence).split() + ["<@"]
        bigrams = [tup for tup in zip(tokens,tokens[1:])]
        trigrams = [trip for trip in zip(tokens,tokens[1:], tokens[2:])]
        raise NotImplementedError


if __name__ == "__main__":
    T = TrainingDataBuilder(path_true_sentences="data/true.txt",
                            path_false_sentences="data/false.txt")
    print(T.sentences_true)

    # def read_in_chunks(self, file_object, chunk_size=1024):
    #     """Lazy load, chunked file reader"""
    #     while True:
    #         data = file_object.read(chunk_size)
    #         if not data:
    #             break
    #         yield data
    #
    # f = open('really_big_file.dat')
    # for piece in read_in_chunks(f):
    #     process_data(piece)

