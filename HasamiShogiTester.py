import unittest
import HasamiShogiGame


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.game = HasamiShogiGame.HasamiShogiGame()

    def test_make_first_move(self):
        # confirm make move returns false if Red player moved first
        self.assertFalse(self.game.make_move('a1', 'b1'))
        self.assertFalse(self.game.make_move('a2', 'b2'))
        self.assertFalse(self.game.make_move('a3', 'b3'))
        self.assertFalse(self.game.make_move('a4', 'b4'))
        self.assertFalse(self.game.make_move('a5', 'b5'))
        self.assertFalse(self.game.make_move('a6', 'b6'))
        self.assertFalse(self.game.make_move('a7', 'b7'))
        self.assertFalse(self.game.make_move('a8', 'b8'))
        self.assertFalse(self.game.make_move('a9', 'b9'))

    def test_make_move_turn(self):
        # confirm make move returns False if same player moves twice
        self.game.make_move('i1', 'f1')
        self.assertFalse(self.game.make_move('i2', 'f2'))

    def test_captured_pieces(self):
        self.game.make_move('i4', 'c4')
        self.game.make_move('a2', 'e2')
        self.game.make_move('c4', 'c5')
        self.game.make_move('a4', 'e4')
        # Confirm self capture not possible
        self.game.make_move('i3', 'e3')
        self.game.make_move('a6', 'b6')
        self.game.make_move('i5', 'd5')
        self.game.make_move('b6', 'b5')
        self.game.make_move('i6', 'e6')
        self.game.make_move('a7', 'e7')
        self.game.make_move('i9', 'h9')
        self.game.make_move('a8', 'f8')
        self.game.make_move('h9', 'i9')
        self.game.make_move('f8', 'f5')
        self.game.make_move('i9', 'h9')
        self.game.make_move('f5', 'e5')
        self.assertAlmostEqual(3, self.game.get_num_captured_pieces('BLACK'))


    def test_captured_corner_pieces(self):
        self.game.make_move('i2', 'c2')
        self.game.make_move('a1', 'h1')
        self.game.make_move('c2', 'c8')
        self.game.make_move('a2', 'i2')
        # Checking corner capture works in bottom left corner
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces('BLACK'))
        self.game.make_move('i7', 'b7')
        self.game.make_move('a9', 'h9')
        self.game.make_move('b7', 'b1')
        self.game.make_move('i2', 'h2')
        self.game.make_move('c8', 'c9')
        self.game.make_move('a7', 'i7')
        # Checking corner capture only works for a single corner
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces('BLACK'))
        self.game.make_move('i8', 'b8')
        self.game.make_move('a3', 'a1')
        self.game.make_move('b8', 'b2')
        # Checking corner capture works in bottom right corner
        self.game.make_move('a8', 'i8')
        self.assertAlmostEqual(2, self.game.get_num_captured_pieces('BLACK'))
        # Checking corner capture works in top left corner
        self.game.make_move('b2', 'a2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces('RED'))
        self.game.make_move('a6', 'a9')
        self.game.make_move('c9', 'b9')
        self.game.make_move('h1', 'i1')
        self.game.make_move('b1', 'b8')
        self.game.make_move('h2', 'i2')
        # Checking corner capture works in top right corner
        self.game.make_move('b8', 'a8')
        self.assertAlmostEqual(2, self.game.get_num_captured_pieces('RED'))


if __name__ == '__main__':
    unittest.main()
