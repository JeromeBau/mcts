import unittest

from src.game import TravelingTourist


class TestTravelingTourist(unittest.TestCase):
    def setUp(self):
        self.t = TravelingTourist()

    def test_check_moves(self):
        self.t.possible_moves = ["Berlin", "Copenhagen", "Paris", "Lisbon"]
        self.t.home_town = "Berlin"
        self.t.current_game_state = ["Berlin", "Copenhagen"]

        # Copenhagen not allowed because already visited
        self.assertFalse(self.t._check_move_possible("Copenhagen"))
        # Berlin not allowed because home town and not yet visited all cities
        self.assertFalse(self.t._check_move_possible("Berlin"))
        # Paris is allowed
        self.assertTrue(self.t._check_move_possible("Paris"))

    def tearDown(self):
        pass
