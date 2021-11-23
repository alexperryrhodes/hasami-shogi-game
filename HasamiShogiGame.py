# Author: Alexandra Rhodes
# Date: 11/22/21
# Description:

class HasamiShogiGame:
    """Represents"""

    def __init__(self):
        """Creates a Game object"""

        self._black_pieces = self.generate_pieces('BLACK')
        self._red_pieces = self.generate_pieces('RED')

        self._board = Board(self._black_pieces, self._red_pieces)
        self._black = Player(self._black_pieces)
        self._red = Player(self._red_pieces)

        self._game_state = 'UNFINISHED'
        self._player_turn = 'BLACK'

    def place_pieces_on_board(self):
        self._black.get_pieces()

    def get_game_state(self):
        """"""
        return self._game_state

    def get_active_player(self):
        """"""
        pass

    def get_num_captured_pieces(self, color):
        """"""
        pass

    def make_move(self, square_from, square_to):
        """"""
        pass

    def get_square_occupant(self, square):
        """"""
        pass

    def get_board(self):
        self._board.print_board()

    def generate_pieces(self, color):
        """"""
        piece_list = []
        for piece in range(1, 10):
            if color == 'RED':
                piece_list.append(Piece('a'+str(piece), 'RED'))
            else:
                piece_list.append(Piece('i' + str(piece), 'BLACK'))

        return piece_list

class Board:
    """Represents"""

    def __init__(self, black_pieces, red_pieces):
        """Creates a Board object"""
        self._board = self._make_initial_board()
        self._black_pieces = black_pieces
        self._red_pieces = red_pieces

    def _make_initial_board(self):
        """Creates the initial board"""

        rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        corners = ['a1', 'a9', 'i1', 'i9']
        board = []

        for row in rows:
            board_row = []
            for column in columns:
                location = row+column
                if row == 'a':
                    if location in corners:
                        board_row.append(Space('RED', location, True))
                    else:
                        board_row.append(Space('RED', location, False))
                elif row == 'i':
                    if location in corners:
                        board_row.append(Space('BLACK', location, True))
                    else:
                        board_row.append(Space('BLACK', location, False))
                else:
                    board_row.append(Space('None', location, False))
            board.append(list(board_row))

        return board

    def print_board(self):
        """Prints the board to the console"""

        row_labels = ['[a]', '[b]', '[c]', '[d]', '[e]', '[f]', '[g]', '[h]', '[i]']
        column_labels = ['   ', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']

        column_header = ""
        for label in column_labels:
            column_header +=label
        print(column_header)
        for row in zip(row_labels, self._board):
            print_row = row[0]
            for space in row[1]:
                occupant = space.get_occupant()
                if occupant == 'RED':
                    print_row += '[R]'
                elif occupant == 'BLACK':
                    print_row += '[B]'
                else:
                    print_row += '[ ]'
            print(print_row)


class Space:
    """Represents a space located on the Board"""

    def __init__(self, occupant, location, corner_bool):
        """Creates a initial Space object"""
        self._occupant = occupant
        self._location = location
        self._corner = corner_bool

    def get_occupant(self):
        """Returns the space's current occupant: Black, Red or None"""
        return self._occupant

    def get_location(self):
        """Returns the space's coordinates"""
        return self._location

    def get_corner(self):
        """Returns True if space is a corner space, False if otherwise"""
        return self._corner



class Player:
    """Represents"""

    def __init__(self, pieces):
        """Creates a Player object"""
        self._pieces = pieces


class Piece:
    """Represent"""

    def __init__(self, space, color):
        """"""
        self._space = space
        self._color = color


game = HasamiShogiGame()
game.get_board()
