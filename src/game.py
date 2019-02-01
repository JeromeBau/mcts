class Game(object):
    """ Defines the game
    To be used as a parent class to define the actual game

    Allows to implement a set of rules and processes of the game.
    """

    def __init__(self):
        self.current_game_state = None
        self.possible_moves = None

    def _check_move_possible(self, move):
        """ Test if move is allowed"""
        raise NotImplementedError

    def _check_game_over(self):
        """ Test if another move is possible or if the game has terminated"""
        raise NotImplementedError

    def make_a_move(self):
        """ Make a move if possible"""
        raise NotImplementedError

    def generate_next_move(self):
        raise NotImplementedError

    def simulate_moves(self):
        """ Simulate next moves until the game ends"""
        raise NotImplementedError

    def evaluate_moves(self):
        """ """
        raise NotImplementedError


class TravelingTourist(Game):
    def __init__(self):
        super(TravelingTourist, self).__init__()
        self.home_town = "Berlin"
        self.possible_moves = ["Berlin", "Copenhagen", "Paris", "Lisbon"]
        self.current_game_state = []

    def _check_move_possible(self, move: str):
        """ Check if move is allowed

        A move is allowed if
        (1) No city is visited twice (except for returning home)
        (2) The traveler returns to the home town at the end
        (3) At the end all cities have been visited
        :param move: city name
        :return:
        """
        if move == self.home_town:
            # only allowed if all other cities have been visited
            if len(self.possible_moves) == 1 and self.possible_moves[0] == self.home_town:
                return True
            else:
                return False
        elif move in self.current_game_state:
            # City has already been visited
            return False
        else:
            return True

    def generate_next_move(self) -> str:
        """ Generates a next city to visit

        If all cities have been visited, next city will be the root city
        :return: city name
        """
        if self.possible_moves:
            pass
