import unittest
import unittest.mock as mock
from random import Random
from typing import List

from helper_functions import _assert_almost_equel

from nlg import NLGame
from src.monte_carlo import MonteCarloTreeSearch
from src.traveling_tourist import TravelingTourist
from src.tree import SearchTree

# fix random seed
random = Random(42)


def patched_weighted_random_choice(self, choice: List[str], probability_vector: List[float], element=0):
    return choice[element]


def patched_random_choice(list_of_elements, element=0):
    return list_of_elements[element]


class TestMonteCarloWithTSP(unittest.TestCase):
    def setUp(self):
        traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Copenhagen"],
                                             home_town="Berlin",
                                             current_game_state=["Berlin"])
        tree = SearchTree()
        self.m = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)

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

    def test_upper_confidence_bound(self):
        self.m.total_simulations_run = 42
        self.m.upc_coefficient = 1000
        average_value = 4300
        n_simul_node = 4
        expected = round(5266.652680423968, 3)
        received = round(self.m.compute_upper_confidence_bound(average_value=average_value,
                                                               n_simul_node=n_simul_node), 3)
        self.assertEqual(expected, received)

    def test_select(self):
        current_path = self._mock_select()
        self.assertListEqual(current_path, ["Berlin"])
        self.assertListEqual(self.m.current_path, ["Berlin"])
        self.assertListEqual(self.m.current_game.current_game_state, ["Berlin"])

    def test_expand(self):
        self._mock_select()
        expanded_path = self._mock_expand()
        self.assertListEqual(expanded_path, ["Berlin", "Lisbon"])
        self.assertListEqual(self.m.current_path, ["Berlin", "Lisbon"])

    def test_simulate(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        rough_estimate = 2314.47 + 2199.68 + 1786.27 + 2073.02 + 354.96
        self.assertTrue(_assert_almost_equel(rough_estimate, evaluation))

    def test_backpropagate(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        self.assertEqual(self.m.search_tree["Berlin"].average_path_value, None)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].average_path_value, None)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].passes, 0)
        self.m.backpropagate(evaluation)
        self.assertEqual(self.m.search_tree["Berlin"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].passes, 1)

    def make_one_iteration_w_mock(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        self.m.backpropagate(evaluation)

    def test_select_second_iteration(self):
        self.make_one_iteration_w_mock()

        current_path = self._mock_select()
        self.assertListEqual(current_path, ["Berlin", "Lisbon"])
        self.assertListEqual(self.m.current_path, ["Berlin", "Lisbon"])
        self.assertListEqual(self.m.current_game.current_game_state, ["Berlin", "Lisbon"])

        current_path = self._mock_expand()
        self.assertListEqual(current_path, ["Berlin", "Lisbon", "Hamburg"])
        self.assertListEqual(self.m.current_path, ["Berlin", "Lisbon", "Hamburg"])
        self.assertListEqual(self.m.current_game.current_game_state, ["Berlin", "Lisbon", "Hamburg"])

        self.assertEqual(self.m.search_tree["Berlin"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].passes, 1)
        evaluation = self._mock_simulate()
        self.m.backpropagate(evaluation)
        self.assertEqual(self.m.search_tree["Berlin"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"].passes, 2)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"]["Hamburg"].average_path_value, 8732.433984335672)
        self.assertEqual(self.m.search_tree["Berlin"]["Lisbon"]["Hamburg"].passes, 1)

    def tearDown(self):
        pass


class TestMonteCarloWithNLG(unittest.TestCase):
    def setUp(self):
        nl_game = NLGame(vocabulary=["name", "is", "john", "was", "michael", "my"],
                         current_game_state=["my"],
                         starting_word="my")
        tree = SearchTree()
        self.m = MonteCarloTreeSearch(game_object=nl_game, tree_object=tree)

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

    def make_one_iteration_w_mock(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        self.m.backpropagate(evaluation)

    def test_select(self):
        current_path = self._mock_select()
        self.assertListEqual(current_path, ["my"])
        self.assertListEqual(self.m.current_path, ["my"])
        self.assertListEqual(self.m.current_game.current_game_state, ["my"])

    def test_expand(self):
        self._mock_select()
        expanded_path = self._mock_expand()
        self.assertListEqual(expanded_path, ["my", "name"])
        self.assertListEqual(self.m.current_path, ["my", "name"])

    def test_simulate(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        expected = 1
        self.assertEqual(expected, evaluation)

    def test_backpropagate(self):
        self._mock_select()
        self._mock_expand()
        evaluation = self._mock_simulate()
        self.assertEqual(self.m.search_tree["my"].average_path_value, None)
        self.assertEqual(self.m.search_tree["my"]["name"].average_path_value, None)
        self.assertEqual(self.m.search_tree["my"]["name"].passes, 0)
        self.m.backpropagate(evaluation)
        self.assertEqual(self.m.search_tree["my"].average_path_value, 1)
        self.assertEqual(self.m.search_tree["my"]["name"].average_path_value, 1)
        self.assertEqual(self.m.search_tree["my"]["name"].passes, 1)
        # Next iteration
        self._mock_select()
        self._mock_expand()
        self._mock_simulate()
        # override with 0
        self.m.backpropagate(0)
        self.assertEqual(self.m.search_tree["my"]["name"].passes, 2)
        self.assertEqual(self.m.search_tree["my"]["name"]["name"].passes, 1)
        self.assertEqual(self.m.search_tree["my"]["name"]["name"].average_path_value, 0)
        self.assertEqual(self.m.search_tree["my"]["name"].average_path_value, 0.5)

        # Next iteration
        self._mock_select()
        self._mock_expand()
        self._mock_simulate()
        # override with 0
        self.m.backpropagate(0)
        self.assertEqual(self.m.search_tree["my"]["name"].passes, 3)
        self.assertEqual(self.m.search_tree["my"]["name"]["name"].passes, 2)
        self.assertEqual(self.m.search_tree["my"]["name"]["name"].average_path_value, 0)
        self.assertEqual(self.m.search_tree["my"]["name"].average_path_value, 0.3333333333333333)
        # raise

    def test_random_iterations(self):
        for i in range(20):
            self.setUp()
            self.m.make_iteration(100)
            self.tearDown()

    def tearDown(self):
        pass
