import unittest

from src.traveling_tourist import TravelingTourist


class TestTravelingTourist(unittest.TestCase):
    def setUp(self):
        self.t = TravelingTourist()

    def test_check_moves(self):
        test_sets = {
            1: {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen"],
                "test_possible": ["Paris"],
                "test_impossible": ["Copenhagen", "Berlin"]
            },
            2: {
                "possible_moves": [],
                "home_town": "Paris",
                "current_game_state": ["Paris", "Berlin", "Copenhagen", "Lisbon", "Paris"],
                "test_possible": [],
                "test_impossible": ["Paris", "xxx", "Copenhagen", "Lisbon"]
            },

        }
        for test_set in test_sets.values():
            self.setUp()
            self.t.possible_moves = test_set["possible_moves"]
            self.t.home_town = test_set["home_town"]
            self.t.current_game_state = test_set["current_game_state"]

            for not_allowed in test_set["test_impossible"]:
                self.assertFalse(self.t._check_move_possible(not_allowed))

            for allowed in test_set["test_possible"]:
                print("tested", allowed)
                print("possible moves", self.t.possible_moves)
                print("test if possible:", self.t._check_move_possible(allowed))
                print("---")
                self.assertTrue(self.t._check_move_possible(allowed))
            self.tearDown()

    def test_generate_next_move(self):
        pass

    def tearDown(self):
        self.t = None
