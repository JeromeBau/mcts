import unittest
from typing import Union

from src.game import MoveNotAllowedError, GameInitiationError
from src.traveling_tourist import TravelingTourist


class TestTravelingTourist(unittest.TestCase):
    def setUp(self):
        pass

    def _assert_almost_equel(self, number_received: Union[float, int], number_expected: Union[float, int], message=None, factor=0.02):
        if message is None:
            message = "Expected {e}, received {r}".format(e=number_expected, r=number_received)
        return self.assertTrue(number_expected - factor * number_expected < number_received < number_expected + factor * number_expected, message)

    def test_game_initiation(self):
        test_sets = [
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Copenhagen"],
                "expect_raise": False
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Copenhagen"],
                "expect_raise": False
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": ["Berlin"],
                "expect_raise": False
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "Berlin",
                "current_game_state": [],
                "expect_raise": False
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": "",
                "current_game_state": [],
                "expect_raise": False
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": None,
                "current_game_state": [],
                "expect_raise": True
            },
            {
                "possible_moves": ["Berlin", "Paris", "Lisbon"],
                "home_town": ["Berlin"],
                "current_game_state": [],
                "expect_raise": True
            }
        ]
        for game in test_sets:
            print("----")
            print(game)
            if game["expect_raise"]:
                with self.assertRaises(GameInitiationError):
                    self.t = TravelingTourist(
                        possible_moves=game["possible_moves"],
                        home_town=game["home_town"],
                        current_game_state=game["current_game_state"]
                    )
                    print(self.t)
                    print(self.t.root)
            else:
                self.t = TravelingTourist(
                    possible_moves=game["possible_moves"],
                    home_town=game["home_town"],
                    current_game_state=game["current_game_state"]
                )

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
            self.t = TravelingTourist(
                possible_moves=test_set["possible_moves"],
                home_town=test_set["home_town"],
                current_game_state=test_set["current_game_state"]
            )

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
            self.t = TravelingTourist(
                possible_moves=test_set["possible_moves"],
                home_town=test_set["home_town"],
                current_game_state=test_set["current_game_state"]
            )
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
            self.t = TravelingTourist(
                possible_moves=test_set["possible_moves"],
                home_town=test_set["home_town"],
                current_game_state=test_set["current_game_state"]
            )
            if test_set["expect_raise"]:
                with self.assertRaises(MoveNotAllowedError):
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

    def test_cities_exist(self):
        cities_to_test = ['Barcelona', 'Belgrade', 'Berlin', 'Brussels', 'Bucharest', 'Budapest', 'Copenhagen', 'Dublin', 'Paris', 'Lisbon', 'Madrid', 'Cologne', 'Bern', 'Amsterdam', 'London', 'Manchester', 'Oslo', 'Rome', 'Sicily', 'Montpellier', 'Zurich', 'Vienna', 'Athens']
        self.t = TravelingTourist(
            possible_moves=cities_to_test,
            home_town="Athens",
            current_game_state=[]
        )
        self.assertListEqual(list(self.t.city_grid.cities.keys()), cities_to_test)

    def test_city_distances_roughly_correct(self):
        cities_to_test = ['Barcelona', 'Belgrade', 'Berlin', 'Brussels', 'Bucharest', 'Budapest', 'Copenhagen', 'Dublin', 'Paris', 'Lisbon', 'Madrid', 'Cologne', 'Bern', 'Amsterdam', 'London', 'Manchester', 'Oslo', 'Rome', 'Sicily', 'Montpellier', 'Zurich', 'Vienna', 'Athens']
        self.t = TravelingTourist(
            possible_moves=cities_to_test,
            home_town="Athens",
            current_game_state=[]
        )
        distance_estiamtes = [
            {
                "cities": ["Paris", "Berlin"],
                "distance_expected": 900
            },
            {
                "cities": ["Athens", "Lisbon"],
                "distance_expected": 2800
            }
        ]
        for distance_dict in distance_estiamtes:
            distance_computed = int(self.t.city_grid.distance_between_two_cities(*distance_dict["cities"]))
            self._assert_almost_equel(distance_computed, distance_dict["distance_expected"], factor=0.05)

    def test_evaluate_game(self):
        test_games = [
            {
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Paris", "Berlin"],
                "expected_evaluation": 1776.59
            },
            {
                "home_town": "Berlin",
                "current_game_state": ["Berlin", "Lisbon", "Athens", "London", "Berlin"],
                "expected_evaluation": 2314.47 + 2851.68 + 2391.61 + 932.37
            }
        ]
        for game in test_games:
            self.t = TravelingTourist(
                possible_moves=[],
                home_town=game["home_town"],
                current_game_state=game["current_game_state"]
            )
            self._assert_almost_equel(self.t.evaluate_game(), game["expected_evaluation"], factor=0.01)

    def tearDown(self):
        self.t = None
