from typing import List, Dict

import geopy
import pandas as pd
from geopy import distance

from src.game import Game, MoveNotAllowedError, GameStateError, GameInitiationError


class City(object):
    def __init__(self, city_name: str):
        self.name = city_name.lower()
        self.longitude = None
        self.latitude = None

    def compute_coordinates(self):
        distances = pd.read_csv("/home/jjb/Dropbox/Programming/GIT/mcts/src/resources/large_cities.csv")
        search = distances[distances["City"] == self.name]
        if len(search) == 1 and len(list(search["Latitude"])) == 1 and len(list(search["Longitude"])) == 1:
            self.latitude = float(list(search["Latitude"])[0])
            self.longitude = float(list(search["Longitude"])[0])
        else:
            raise KeyError("City {name} not found.".format(name=self.name))

    @property
    def coordinates(self) -> Dict[str, float]:
        if self.latitude is None or self.longitude is None:
            self.compute_coordinates()
        return geopy.Point(self.latitude, self.longitude)


class CityGrid(object):
    def __init__(self, city_names: List[str]):
        self.city_names = city_names
        self.cities = {name: City(name) for name in self.city_names}

    def distance_between_two_cities(self, city1_name: str, city2_name: str) -> float:
        """
        :param city1: Name of one city
        :param city2: Name of another city
        :return: The distance in meters
        """
        for name in [city1_name, city2_name]:
            assert name in self.cities, "City name was not found in list given with initiation."
        city1 = self.cities[city1_name]
        city2 = self.cities[city2_name]
        return distance.distance(city1.coordinates, city2.coordinates).km


class TravelingTourist(Game):
    def __init__(self, possible_moves: List[str], current_game_state: List[str], home_town: str):
        super(TravelingTourist, self).__init__()
        self.root = home_town
        self.possible_moves = possible_moves
        self.current_game_state = current_game_state
        self.city_grid = CityGrid(self.possible_moves + self.current_game_state)
        self._check_game_correctly_initiated()

    def _check_game_correctly_initiated(self):
        duplicates = set([city for city in self.possible_moves if self.possible_moves.count(city) > 1])
        if len(duplicates) != 0:
            raise GameInitiationError("Found the following duplicates in possible moves: {dups}".format(dups=duplicates))
        if not isinstance(self.root, str):
            raise GameInitiationError("Home Town needs to be a string.")

    def _check_game_over(self):
        if len(self.possible_moves) == 0:
            return True
        return False

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

        if move == self.root:
            # only allowed if all other cities have been visited
            if len(self.possible_moves) == 1 and self.possible_moves[0] == self.root:
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
            raise MoveNotAllowedError("Cannot make this move: '{}'.".format(move))
        self.possible_moves.remove(move)
        self.current_game_state.append(move)
        return

    def evaluate_game(self):
        if not self._check_game_over():
            raise GameStateError("Game has not been terminated")
        total_distance = 0
        for i in range(len(self.current_game_state) - 1):
            # TODO: Can be done more elegantly with a map reduce
            city1 = self.current_game_state[i]
            city2 = self.current_game_state[i + 1]
            distance = self.city_grid.distance_between_two_cities(city1, city2)
            total_distance += distance
        return total_distance
