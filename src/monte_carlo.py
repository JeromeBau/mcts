import math
import random
from copy import deepcopy
from pprint import pprint
from typing import List

from numpy.random import choice
from traveling_tourist import TravelingTourist
from tree import SearchTree


class MonteCarloTreeSearch(object):
    def __init__(self, game_object, tree_object: SearchTree):
        self.game_master = game_object
        self.current_game = deepcopy(game_object)
        self.current_path = [self.game_master.root]
        self.search_tree = tree_object
        self.upc_coefficient = 1
        self.total_simulations_run = 0

    def compute_upper_confidence_bound(self, average_value: float, n_simul_node: int) -> float:
        return average_value + self.upc_coefficient * math.sqrt((math.log(self.total_simulations_run) / n_simul_node))

    @staticmethod
    def _weighted_random_choice(choices: List[str], probability_vector: List[float]) -> str:
        return choice(choices, 1, p=probability_vector)[0]

    def select(self):
        self.current_game = deepcopy(self.game_master)
        self.current_path = [self.game_master.root]

        branch = self.search_tree[self.game_master.root]
        children_ucb = {k: self.compute_upper_confidence_bound(average_value=branch[k].average_path_value, n_simul_node=branch[k].passes)
                        for k in branch.keys()}
        sum_ucb = sum(children_ucb.values())
        children_probs = {k: v / sum_ucb for k, v in children_ucb.items()}

        while len(children_probs.keys()) and self.current_game._check_game_over() is False:
            chosen = self._weighted_random_choice(list(children_probs.keys()), list(children_probs.values()))
            self.current_path.append(chosen)
            self.current_game.make_a_move(chosen)
            branch = branch[chosen]
            if isinstance(branch, dict):
                children_ucb = {k: self.compute_upper_confidence_bound(average_value=branch[k].average_path_value, n_simul_node=branch[k].passes) for k in branch.keys() if isinstance(k, str)}
                sum_ucb = sum(children_ucb.values())
                children_probs = {k: v / sum_ucb for k, v in children_ucb.items()}
            else:
                break
        return self.current_path

    def expand(self):
        # Retrieve possible children
        children = self.current_game.generate_next_moves()
        if not len(children):
            return False
        # Randomly choose one of them
        expansion_child = random.choice(children)
        # Make move
        self.current_game.make_a_move(expansion_child)
        self.current_path.append(expansion_child)
        # Expand the tree
        current_leaf = self.search_tree
        for next_leaf in self.current_path:
            current_leaf = current_leaf[next_leaf]
        return self.current_path

    def simulate(self):
        simulated_game = deepcopy(self.current_game)
        simulated_path = deepcopy(self.current_path)
        while simulated_game._check_game_over() is False:
            # Retrieve possible children
            children = simulated_game.generate_next_moves()
            if not len(children):
                return False
            # Randomly choose one of them
            expansion_child = random.choice(children)
            # Make move
            simulated_game.make_a_move(expansion_child)
            simulated_path.append(expansion_child)
        evaluation = simulated_game.evaluate_game()
        self.total_simulations_run += 1
        return evaluation

    def _backpropagate_change_leave_value(self, path, value):
        current_child = self.search_tree
        print("start", current_child)
        for next_child in self.current_path:
            current_child = current_child[next_child]
            print("current", current_child)
        if current_child.passes == 1:
            current_child.average_path_value = value
        else:
            current_child.average_path_value = (current_child.passes * current_child.average_path_value + value) / (current_child.passes + 1)

    def _backpropagate_change_passes(self):
        current_child = self.search_tree
        for next_child in self.current_path:
            current_child = current_child[next_child]
            current_child.passes += 1

    def backpropagate(self, simulation_evaluation):
        # self._backpropagate_change_passes()
        # self._backpropagate_change_leave_value(path=self.current_path, value=simulation_evaluation)
        current_child = self.search_tree
        for next_child in self.current_path:
            current_child = current_child[next_child]
            current_child.passes += 1
            if current_child.passes == 1:
                current_child.average_path_value = simulation_evaluation
            else:
                current_child.average_path_value = ((current_child.passes - 1)* current_child.average_path_value + simulation_evaluation) / (current_child.passes)

    def make_iteration(self):
        self.select()
        self.expand()
        simulation_evaluation = self.simulate()
        if simulation_evaluation:
            self.backpropagate(simulation_evaluation)

    def find_best_path(self):
        best_path = []

        def get_best_child(children: List[SearchTree]):
            child_value_tups = [[child, child.average_path_value] for child in children]
            if len(child_value_tups):
                return sorted(child_value_tups, key=lambda tup: tup[1])[0][0]
            else:
                return None
        best_child_name = get_best_child(self.search_tree.values())
        current_node = self.search_tree[best_child_name]

        while best_child_name is not None:
            import ipdb
            ipdb.set_trace()
            best_child_name = get_best_child(self.search_tree.values())
            current_node = self.search_tree[best_child_name]

        return best_path

    def start(self, rounds=6):
        for i in range(round):
            self.make_iteration()



if __name__ == "__main__":
    traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Oslo", "Rome", "Copenhagen", "Budapest"],
                                         home_town="Berlin",
                                         current_game_state=["Berlin"])
    tree = SearchTree()
    M = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)
    for i in range(5):
        M.make_iteration()
    print(M.find_best_path())