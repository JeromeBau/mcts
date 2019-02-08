import random
from copy import deepcopy
from pprint import pprint
from typing import List

from numpy.random import choice

from src.traveling_tourist import TravelingTourist
from src.tree import SearchTree


class MonteCarloTreeSearch(object):
    def __init__(self, game_object, tree_object: SearchTree):
        self.game_master = game_object
        self.current_game = deepcopy(game_object)
        self.current_path = [self.game_master.root]
        self.search_tree = tree_object
        self.initiate()

    def initiate(self):
        if len(self.game_master.possible_moves) > 1:
            children = self.game_master.generate_next_moves()
            for child in children:
                self.search_tree[self.game_master.root][child] = SearchTree()
                self.search_tree[self.game_master.root][child].average_path_value = 1 / len(children)
        else:
            # TODO
            raise NotImplementedError

    @staticmethod
    def _weighted_random_choice(choices: List[str], probability_vector: List[float]) -> str:
        return choice(choices, 1, p=probability_vector)[0]

    def select(self):
        """

        :return:
        """
        self.current_game = deepcopy(self.game_master)

        branch = self.search_tree[self.game_master.root]
        children_distances = {k: branch[k].average_path_value for k in branch.keys()}
        sum_distances = sum(children_distances.values())
        children_probs = {k: v / sum_distances for k, v in children_distances.items()}

        while len(children_probs.keys()) and self.current_game._check_game_over() is False:
            chosen = self._weighted_random_choice(list(children_probs.keys()), list(children_probs.values()))
            self.current_path.append(chosen)
            self.current_game.make_a_move(chosen)
            branch = branch[chosen]
            if isinstance(branch, dict):
                children_distances = {k: branch[k].average_path_value for k in branch.keys() if isinstance(k, str)}
                sum_distances = sum(children_distances.values())
                children_probs = {k: v / sum_distances for k, v in children_distances.items()}
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
        return evaluation

    def backpropagate(self, simulation_evaluation):
        current_leaf = self.search_tree
        for next_leaf in self.current_path:
            current_leaf = current_leaf[next_leaf]
        print(self.current_path)
        current_leaf.average_path_value = simulation_evaluation

    def main(self):
        for i in range(3):
            self.select()
            self.expand()
            simulation_evaluation = self.simulate()
            if simulation_evaluation:
                self.backpropagate(simulation_evaluation)


if __name__ == "__main__":
    for i in range(10):
        traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Copenhagen"],
                                             home_town="Berlin",
                                             current_game_state=["Berlin"])
        tree = SearchTree()
        M = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)
        pprint(M.search_tree)
        M.main()
