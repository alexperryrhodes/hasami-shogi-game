import unittest
import HasamiShogiGame

GAME_PLAYERS = ['RED', 'BLACK']
PLAYER_1 = GAME_PLAYERS[0]
PLAYER_2 = GAME_PLAYERS[1]

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
        # Test two direction capture
        self.assertAlmostEqual(3, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_single_only(self):
        self.game.make_move('i7', 'b7')
        self.game.make_move('a9', 'h9')
        self.game.make_move('b7', 'b1')
        self.game.make_move('a7', 'i7')
        self.assertAlmostEqual(0, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_bottom_left(self):
        self.game.make_move('i2', 'c2')
        self.game.make_move('a1', 'h1')
        self.game.make_move('c2', 'c8')
        self.game.make_move('a2', 'i2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_bottom_right(self):
        self.game.make_move('i8', 'b8')
        self.game.make_move('a9', 'h9')
        self.game.make_move('b8', 'b2')
        self.game.make_move('a8', 'i8')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_top_left(self):
        self.game.make_move('i1', 'b1')
        self.game.make_move('a2', 'c2')
        self.game.make_move('i2', 'd2')
        self.game.make_move('c2', 'c8')
        self.game.make_move('d2', 'a2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_1))

    def test_captured_corner_pieces_top_right(self):
        self.game.make_move('i9', 'b9')
        self.game.make_move('a8', 'c8')
        self.game.make_move('i8', 'd8')
        self.game.make_move('c8', 'c2')
        self.game.make_move('d8', 'a8')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_1))

    def test_get_square_occupant(self):
        self.assertEqual(PLAYER_1, self.game.get_square_occupant('a1'))
        self.assertEqual('NONE', self.game.get_square_occupant('e1'))
        self.assertEqual(PLAYER_2, self.game.get_square_occupant('i1'))

    def test_captured_corner_pieces_board_size10(self):
        self.game.make_move('j2', 'b2')
        self.game.make_move('a1', 'i1')
        self.game.make_move('b2', 'b10')
        self.game.make_move('a2', 'j2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_board_size8(self):
        self.game.make_move('h2', 'b2')
        self.game.make_move('a1', 'g1')
        self.game.make_move('b2', 'b8')
        self.game.make_move('a2', 'h2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_2))

    def test_captured_corner_pieces_board_size4(self):
        self.game.make_move('d2', 'b2')
        self.game.make_move('a1', 'c1')
        self.game.make_move('b2', 'b4')
        self.game.make_move('a2', 'd2')
        self.assertAlmostEqual(1, self.game.get_num_captured_pieces(PLAYER_2))

if __name__ == '__main__':
    unittest.main()
