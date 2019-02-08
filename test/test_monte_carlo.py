import unittest
import unittest.mock as mock
from random import Random
from typing import List

from helper_functions import _assert_almost_equel

from src.monte_carlo import MonteCarloTreeSearch
from src.traveling_tourist import TravelingTourist
from src.tree import SearchTree

# fix random seed
random = Random(42)


def patched_weighted_random_choice(self, choice: List[str], probability_vector: List[float]):
    return choice[0]


def patched_random_choice(list_of_elements):
    return list_of_elements[0]


class TestMonteCarloWithTSP(unittest.TestCase):
    def setUp(self):
        traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Copenhagen"],
                                             home_town="Berlin",
                                             current_game_state=["Berlin"])
        tree = SearchTree()
        self.m = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)
        # self._mock_select()
        # self._mock_expand()
        # self._mock_expand()
        # self._mock_simulate()

    def _mock_select(self):
        with mock.patch.object(MonteCarloTreeSearch, '_weighted_random_choice', new=patched_weighted_random_choice):
            current_path = self.m.select()
        return current_path

    def _mock_expand(self):
        with mock.patch('random.choice', patched_random_choice):
            expanded_path = self.m.expand()
        return expanded_path

    def _mock_simulate(self):
        with mock.patch('random.choice', patched_random_choice):
            evaluation = self.m.simulate()
        return evaluation

    def test_select(self):
        current_path = self._mock_select()
        self.assertListEqual(current_path, ["Berlin", "Lisbon"])
        self.assertListEqual(self.m.current_path, ["Berlin", "Lisbon"])
        self.assertListEqual(self.m.current_game.current_game_state, ["Berlin", "Lisbon"])

    def test_expand(self):
        self._mock_select()
        expanded_path = self._mock_expand()
        self.assertListEqual(expanded_path, ["Berlin", "Lisbon", "Hamburg"])
        self.assertListEqual(self.m.current_path, ["Berlin", "Lisbon", "Hamburg"])

    def test_simulate(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        # simulated_path = ['Berlin', 'Lisbon', 'Hamburg', 'Madrid', 'Copenhagen', 'Berlin']
        rough_estimate = 2314.47 + 2199.68 + 1786.27 + 2073.02 + 354.96
        self.assertTrue(_assert_almost_equel(rough_estimate, evaluation))
    #
    # def test_backpropagate(self):
    #     self._mock_simulate()
    #     self._mock_expand()
    #     evaluation = self._mock_simulate()
    #     print("*" * 20)
    #     print("Berlin-Lisbon", self.m.search_tree["Berlin"]["Lisbon"].average_path_value)
    #     print("Berlin-Lisbon-Hamburg", self.m.search_tree["Berlin"]["Lisbon"]["Hamburg"].average_path_value)
    #     print("----")
    #     self.m.backpropagate(evaluation)
    #     print("Berlin-Lisbon", self.m.search_tree["Berlin"]["Lisbon"].average_path_value)
    #     print("Berlin-Lisbon-Hamburg", self.m.search_tree["Berlin"]["Lisbon"]["Hamburg"].average_path_value)
    #     print("*"*20)
    #     raise

    def tearDown(self):
        pass


class TestMonteCarloWithNLG(unittest.TestCase):
    def setUp(self):
        pass

    def test_select(self):
        pass

    def tearDown(self):
        pass
