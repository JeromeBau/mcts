import math
import random
from copy import deepcopy
from typing import List

from numpy.random import choice

from nlg import NLGame
from tree import SearchTree


class MonteCarloTreeSearch(object):
    def __init__(self, game_object, tree_object: SearchTree):
        self.game_master = game_object
        self.current_game = deepcopy(game_object)
        self.current_path = [self.game_master.root]
        self.search_tree = tree_object
        self.upc_coefficient = 1000
        self.total_simulations_run = 0

    def compute_upper_confidence_bound(self, average_value: float, n_simul_node: int) -> float:
        if n_simul_node == 0:
            return 99 ** 10
        value = average_value + self.upc_coefficient * math.sqrt((math.log(self.total_simulations_run) / n_simul_node))
        if value == 0:
            # TODO: dirty fix?
            value += 0.01
        return value

    @staticmethod
    def _weighted_random_choice(choices: List[str], probability_vector: List[float]) -> str:
        return choice(choices, 1, p=probability_vector)[0]

    def select(self):
        self.current_game = deepcopy(self.game_master)
        self.current_path = [self.game_master.root]
        branch = self.search_tree[self.game_master.root]
        children_ucb = {k: self.compute_upper_confidence_bound(average_value=branch[k].average_path_value, n_simul_node=branch[k].passes) for k in branch.keys()}
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

    def _expand_tree(self, child):
        path_to_expand = self.current_path + [child]
        current_leaf = self.search_tree
        for next_leaf in path_to_expand:
            current_leaf = current_leaf[next_leaf]

    def expand(self):
        # Retrieve possible children
        children = self.current_game.generate_next_moves()
        if not len(children):
            return False
        for child in children:
            self._expand_tree(child)
        # Randomly choose one of them
        expansion_child = random.choice(children)
        # Make move
        self.current_game.make_a_move(expansion_child)
        self.current_path.append(expansion_child)

        return self.current_path

    def simulate(self):
        simulated_game = deepcopy(self.current_game)
        simulated_path = deepcopy(self.current_path)
        while simulated_game._check_game_over() is False:
            # Retrieve possible children
            children = simulated_game.generate_next_moves()
            if not len(children):
                raise Exception("No children left")
            # Randomly choose one of them
            expansion_child = random.choice(children)
            # Make move
            simulated_game.make_a_move(expansion_child)
            simulated_path.append(expansion_child)
        evaluation = simulated_game.evaluate_game()
        # print("simulated evaluation", simulated_game.sentence_classifier.log)
        self.total_simulations_run += 1
        return evaluation

    def backpropagate(self, simulation_evaluation):
        current_child = self.search_tree
        for next_child in self.current_path:
            current_child = current_child[next_child]
            current_child.passes += 1
            if current_child.passes == 1:
                current_child.average_path_value = simulation_evaluation
            else:
                assert current_child != 0
                current_child.average_path_value = ((current_child.passes - 1) * current_child.average_path_value + simulation_evaluation) / (current_child.passes)

    def make_iteration(self, n=1):
        for i in range(n):
            self.select()
            self.expand()
            simulation_evaluation = self.simulate()
            if isinstance(simulation_evaluation, int):
                # TODO: Not sure if int is sufficient
                self.backpropagate(simulation_evaluation)
            if i%10==0:
                print("iteration nr: ", i+1, "/",n)

    def get_best_path(self):
        best_path = [self.game_master.root]

        current = self.search_tree[self.game_master.root]
        child_value_pairs = sorted(filter(lambda tup: isinstance(tup[1], float) or isinstance(tup[1], int),
                                          map(lambda x: [x, current[x].average_path_value], current.keys())),
                                   key=lambda tup: tup[1], reverse=True)
        while len(child_value_pairs):
            best_child_name = child_value_pairs[0][0]
            best_path.append(best_child_name)
            current = current[best_child_name]
            child_value_pairs = sorted(filter(lambda tup: isinstance(tup[1], float) or isinstance(tup[1], int),
                                              map(lambda x: [x, current[x].average_path_value], current.keys())),
                                       key=lambda tup: tup[1], reverse=True)
        return best_path

    def start(self, rounds=6):
        for i in range(round):
            self.make_iteration()


if __name__ == "__main__":
    # traveling_tourist = TravelingTourist(possible_moves=["Berlin", "Lisbon", "Hamburg", "Madrid", "Oslo", "Rome", "Copenhagen", "Budapest"],
    #                                      home_town="Berlin",
    #                                      current_game_state=["Berlin"])
    # tree = SearchTree()
    # M = MonteCarloTreeSearch(game_object=traveling_tourist, tree_object=tree)
    # for i in range(5):
    #     M.make_iteration()
    # print(M.find_best_path())
    import pandas as pd
    vocab = list(pd.read_csv("/home/jjb/Dropbox/Programming/GIT/mcts/data/most_common_words.csv", header=None)[0])[:100]
    print(vocab[:20])
    nl_game = NLGame(vocabulary=list(set(vocab + ["house", "tree", "is", "big", "tall"])), #["name", "is", "john", "was", "michael", "my"]
                     current_game_state=["the"],
                     starting_word="the")
    nl_game.sentence_length = 5
    tree = SearchTree()

    M = MonteCarloTreeSearch(game_object=nl_game, tree_object=tree)
    print("sentence length", nl_game.sentence_length)
    M.make_iteration(1000)
    print(M.get_best_path())
