import unittest
from random import Random
from typing import List
import unittest.mock as mock
from src.monte_carlo import MonteCarloTreeSearch
from src.traveling_tourist import TravelingTourist
from src.tree import SearchTree

# fix random seed
random = Random(42)


def patched_weighted_random_choice(self, choice:List[str], probability_vector: List[float]):
    return choice[0]

class TestMonteCarloWithTSP(unittest.TestCase):
    def setUp(self):
        traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Copenhagen"],
                                             home_town="Berlin",
                                             current_game_state=[])
        tree = SearchTree()
        self.m = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)

    def test_select(self):
        with mock.patch.object(MonteCarloTreeSearch, '_weighted_random_choice', new=patched_weighted_random_choice):
            current_path = self.m.select()

        self.assertListEqual(current_path, ["Berlin", "Lisbon"])

    def tearDown(self):
        pass


class TestMonteCarloWithNLG(unittest.TestCase):
    def setUp(self):
        pass

    def test_select(self):
        pass

    def tearDown(self):
        pass
