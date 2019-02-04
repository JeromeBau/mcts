class MoveNotAllowedError(LookupError):
    pass

class GameStateError(Exception):
    pass

class Game(object):
    """ Defines the game
    To be used as a parent class to define the actual game

    Allows to implement a set of rules and processes of the game.
    """

    def __init__(self):
        self.current_game_state = None
        self.possible_moves = None

    def _check_game_correctly_initiated(self):
        """ Test if game can be played with given start variabled"""
        raise NotImplementedError

    def _check_move_possible(self, move):
        """ Test if move is allowed"""
        raise NotImplementedError

    def _check_game_over(self):
        """ Test if another move is possible or if the game has terminated"""
        raise NotImplementedError

    def make_a_move(self, move):
        """ Make a move if possible"""
        raise NotImplementedError

    def generate_next_moves(self):
        raise NotImplementedError

    def simulate_moves(self):
        """ Simulate next moves until the game ends"""
        raise NotImplementedError

    def evaluate_moves(self):
        """ """
        raise NotImplementedError
