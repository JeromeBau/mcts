from typing import List

from src.game import Game


class TravelingTourist(Game):
    def __init__(self):
        super(TravelingTourist, self).__init__()
        self.home_town = "Berlin"
        self.possible_moves = ["Berlin", "Copenhagen", "Paris", "Lisbon"]
        self.current_game_state = []

    def _check_game_correctly_initiated(self):
        duplicates = set([city for city in self.possible_moves if self.possible_moves.count(city) > 1])
        assert len(duplicates) == 0, \
            "Found the following duplicates in possible moves: {dups}".format(dups=duplicates)
        raise NotImplementedError

    def _check_game_over(self):
        print("NOT IMPLEMENTED")
        pass

    def _check_move_possible(self, move: str):
        """ Check if move is allowed

        A move is allowed if
        (1) No city is visited twice (except for returning home)
        (2) The traveler returns to the home town at the end
        (3) At the end all cities have been visited
        :param move: city name
        :return:
        """
        if self._check_game_over():
            return False

        if move == self.home_town:
            # only allowed if all other cities have been visited
            if len(self.possible_moves) == 1 and self.possible_moves[0] == self.home_town:
                return True
            else:
                return False
        elif move in self.current_game_state:
            # City has already been visited
            return False
        elif move not in self.possible_moves:
            # not planned to visit this city
            return False
        else:
            return True

    def generate_next_moves(self) -> List[str]:
        """ Generates a list of possible next cities to visit

        If all cities have been visited, next city will be the root city
        :return: city name
        """
        return list(filter(lambda move: self._check_move_possible(move), self.possible_moves))

    def make_a_move(self, move: str):
        """ Change current_game_state and possible_moves

        :param move: city name
        :return:
        """
        if not self._check_move_possible(move):
            raise Exception("Cannot make move.")
        self.possible_moves.remove(move)
        self.current_game_state.append(move)
        return
