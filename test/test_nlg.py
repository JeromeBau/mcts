import unittest

from game import MoveNotAllowedError, GameInitiationError
from nlg import NLGame
from sentence_classifier.sentence_classifier import SentenceClassifier
from traveling_tourist import TravelingTourist
from helper_functions import _assert_almost_equel

class TestNLG(unittest.TestCase):
    def setUp(self):
        pass

    def test_game_initiation(self):
        test_sets = [
            {
                "possible_moves": ["my", "name", "is","was", "not", "john", "michael"],
                "starting_word": "my",
                "current_game_state": ["my", "name"],
                "expect_raise": False
            },
            {
                "possible_moves": ["my", "name", "is", "was", "not", "john", "michael"],
                "starting_word": "my",
                "current_game_state": ["name"],
                "expect_raise": True
            },
            {
                "possible_moves": ["my", "name", "is", "was", "not", "john", "michael"],
                "starting_word": "my",
                "current_game_state": [],
                "expect_raise": True
            },
            {
                "possible_moves": ["my", "name", "is", "was", "not", "john", "michael"],
                "starting_word": "",
                "current_game_state": ["my"],
                "expect_raise": True
            }
        ]
        for game in test_sets:
            print(game)
            if game["expect_raise"]:
                with self.assertRaises(GameInitiationError):
                    self.t = NLGame(
                        vocabulary=game["possible_moves"],
                        starting_word=game["starting_word"],
                        current_game_state=game["current_game_state"]
                    )
            else:
                self.t = NLGame(
                    vocabulary=game["possible_moves"],
                    starting_word=game["starting_word"],
                    current_game_state=game["current_game_state"]
                )
                
                
    def test_check_moves(self):
        test_sets = [
            {
                "possible_moves": ["my", "name", "is","was", "not", "john", "michael"],
                "starting_word": "my",
                "current_game_state": ["my", "name"],
                "test_possible":["is", "john"],
                "test_impossible": ["slkdfj", ""]
            }
        ]
        for test_set in test_sets:
            self.t = NLGame(
                vocabulary=test_set["possible_moves"],
                starting_word=test_set["starting_word"],
                current_game_state=test_set["current_game_state"]
            )
            for not_allowed in test_set["test_impossible"]:
                self.assertFalse(self.t._check_move_possible(not_allowed))

            for allowed in test_set["test_possible"]:
                self.assertTrue(self.t._check_move_possible(allowed))
            self.tearDown()

class TestSentenceClassifier(unittest.TestCase):
    def setUp(self):
        self.sentence_classifier =SentenceClassifier()

    def test_accept(self):
        human = ["my name is michael", "my name is michael"]
        not_human = ["my name name name", "john my michael name"]
        for sentence in human:
            self.assertTrue(self.sentence_classifier.sentence_is_human(sentence.split()))
