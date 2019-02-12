from typing import List

from game import Game, GameInitiationError, MoveNotAllowedError
from sentence_classifier.sentence_classifier import SentenceClassifier


class NLGame(Game):
    def __init__(self, vocabulary: List[str], current_game_state: List[str], starting_word: str):
        super(NLGame, self).__init__()
        self.root = starting_word
        self.possible_moves = vocabulary
        self.current_game_state = current_game_state
        self._check_game_correctly_initiated()
        self.sentence_classifier = SentenceClassifier(acceptance_threshold=1.5, trigram_importance=5)
        self.sentence_length = 4

    def _check_game_correctly_initiated(self):
        duplicates = set([word for word in self.possible_moves if self.possible_moves.count(word) > 1])
        if len(duplicates) != 0:
            raise GameInitiationError("Found the following duplicates in possible moves: {dups}".format(dups=duplicates))
        if not isinstance(self.root, str) or not len(self.root):
            raise GameInitiationError("Starting word needs to be a string with at least one character.")
        if len(self.current_game_state) == 0:
            raise GameInitiationError("Need to start game with at least starting_word in current_game_state.")
        if self.current_game_state[0] != self.root:
            raise GameInitiationError("First word in current_game_state needs to be starting_word")

    def _check_move_possible(self, move):
        """ Test if move is allowed"""
        if move not in self.possible_moves:
            return False
        return True

    def _check_game_over(self):
        """ Test if another move is possible or if the game has terminated"""
        if len(self.current_game_state) >= self.sentence_length:
            return True
        return False

    def make_a_move(self, move):
        """ Make a move if possible"""
        if not self._check_move_possible(move):
            raise MoveNotAllowedError("Cannot make this move: '{}'.".format(move))
        self.current_game_state.append(move)
        return

    def generate_next_moves(self):
        return list(filter(lambda move: self._check_move_possible(move), self.possible_moves))

    def evaluate_game(self) -> int:
        """ Evaluate if this sentence is human or not

        :return: 1 if sentence is human, 0 if fake.
        """
        return int(self.sentence_classifier.sentence_is_human(self.current_game_state))

if __name__ == "__main__":
    N = NLGame(vocabulary=["my", "name", "is", "was", "john", "michael", "smith", "miller"],
               current_game_state=["my"],
               starting_word="my")
