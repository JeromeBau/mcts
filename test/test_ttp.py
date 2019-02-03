import unittest

from src.traveling_tourist import TravelingTourist


class TestTravelingTourist(unittest.TestCase):
    def setUp(self):
        self.t = TravelingTourist()

    def test_check_moves(self):
        test_sets = [
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen"],
                "test_possible": ["Paris"],
                "test_impossible": ["Copenhagen", "Berlin"]
            },
            {
                "possible_moves": [],
                "home_town": "Paris",
                "current_game_state": ["Paris", "Berlin", "Copenhagen", "Lisbon", "Paris"],
                "test_possible": [],
                "test_impossible": ["Paris", "xxx", "Copenhagen", "Lisbon"]
            }
        ]
        for test_set in test_sets:
            self.setUp()
            self.t.possible_moves = test_set["possible_moves"]
            self.t.home_town = test_set["home_town"]
            self.t.current_game_state = test_set["current_game_state"]

            for not_allowed in test_set["test_impossible"]:
                self.assertFalse(self.t._check_move_possible(not_allowed))

            for allowed in test_set["test_possible"]:
                self.assertTrue(self.t._check_move_possible(allowed))
            self.tearDown()

    def test_generate_next_move(self):
        test_sets = [
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen"],
                "expected_next_moves": ["Paris", "Lisbon"]
            },
            {
                "possible_moves": ["Berlin"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen", "Lisbon", "Paris"],
                "expected_next_moves": ["Berlin"]
            },
            {
                "possible_moves": [],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen", "Lisbon", "Paris"],
                "expected_next_moves": []
            }
        ]
        for test_set in test_sets:
            self.setUp()
            #
            self.t.possible_moves = test_set["possible_moves"]
            self.t.home_town = test_set["home_town"]
            self.t.current_game_state = test_set["current_game_state"]
            #
            self.assertListEqual(self.t.generate_next_moves(), test_set["expected_next_moves"],
                                 "Possible moves: {poss}\n "
                                 "Next moves proposed: {next} \n"
                                 "Expected moves: {exp}".format(poss=self.t.possible_moves,
                                                                next=self.t.generate_next_moves(),
                                                                exp=test_set["expected_next_moves"]))
            #
            self.tearDown()

    def test_make_a_move(self):
        test_sets = [
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen"],
                "move": "Paris",
                "expect_raise": False,
                "new_game_state": ["Berlin", "Copenhagen", "Paris"],
                "new_possible_moves": ["Berlin", "Lisbon"]
            },
            {
                "possible_moves": ["Berlin"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen", "Paris", "Lisbon"],
                "move": "Berlin",
                "expect_raise": False,
                "new_game_state": ["Berlin", "Copenhagen", "Paris", "Lisbon", "Berlin"],
                "new_possible_moves": []
            },
            {
                "possible_moves": [],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen", "Paris", "Lisbon", "Berlin"],
                "move": "Berlin",
                "expect_raise": True,
                "new_game_state": None,
                "new_possible_moves": None
            },
            {
                "possible_moves": ["Berlin"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen", "Paris", "Lisbon"],
                "move": "Shanghai",
                "expect_raise": True,
                "new_game_state": None,
                "new_possible_moves": None
            },
        ]
        for test_set in test_sets:
            self.setUp()
            #
            self.t.possible_moves = test_set["possible_moves"]
            self.t.home_town = test_set["home_town"]
            self.t.current_game_state = test_set["current_game_state"]
            #
            if test_set["expect_raise"]:
                with self.assertRaises(Exception):
                    self.t.make_a_move(test_set["move"])
            else:
                self.t.make_a_move(test_set["move"])
                self.assertListEqual(self.t.current_game_state, test_set["new_game_state"],
                                     "Possible moves: {poss}\n "
                                     "Next moves proposed: {next}".format(poss=self.t.possible_moves,
                                                                          next=self.t.generate_next_moves()))
                self.assertListEqual(self.t.possible_moves, test_set["new_possible_moves"],
                                     "Possible moves: {poss}\n "
                                     "Next moves proposed: {next}".format(poss=self.t.possible_moves,
                                                                          next=self.t.generate_next_moves()))
            #
            self.tearDown()




    def tearDown(self):
        self.t = None
