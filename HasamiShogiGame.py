# Author: Alexandra Rhodes
# Date: 11/22/21
# Description:

class HasamiShogiGame:
    """Represents"""

    def __init__(self):
        """Creates a Game object"""

        self._pieces = self.generate_pieces()
        self._red_pieces = self.get_red_pieces(self._pieces)
        self._black_pieces = self.get_black_pieces(self._pieces)

        self._board = Board(self._pieces)

        self._red = Player(self._red_pieces)
        self._black = Player(self._black_pieces)

        self._game_state = 'UNFINISHED'

        self._active_player = 'BLACK'

    def get_game_state(self):
        """"""
        return self._game_state

    def get_active_player(self):
        """"""
        return self._active_player

    def get_num_captured_pieces(self, color):
        """"""
        if color == 'RED':
            return self._red.get_captured_pieces
        elif color == 'BLACK':
            return self._black.get_captured_pieces
        else:
            print('Not a valid color, please try again.')

    def make_move(self, square_from, square_to):
        """"""
        current_square = self._board.get_square_occupant(square_from)
        target_square = self._board.get_square_occupant(square_from)

        if self._active_player != current_square:
            print('Not active player')
            return False

        board_bool = self._board.validate_move(square_from, square_to)

    def get_square_occupant(self, square):
        """"""
        return self._board.get_square_occupant(square)

    def generate_pieces(self):
        """"""
        piece_list = []
        for row in zip(['a', 'i'], ['RED', 'BLACK']):
            for column in range(1, 10):
                piece_list.append(Piece(row[0], str(column), row[1]))

        return piece_list

    def get_red_pieces(self, pieces):
        """"""
        red_list = []
        for piece in pieces:
            if piece.get_color() == 'RED':
                red_list.append(piece)

        return red_list

    def get_black_pieces(self, pieces):
        black_list = []
        for piece in pieces:
            if piece.get_color() == 'BLACK':
                black_list.append(piece)

        return black_list

    def print_board(self):
        self._board.print_board()


class Board:
    """Represents"""

    def __init__(self, pieces):
        """Creates a Board object"""
        self._board = self._make_initial_board(pieces)

    def _make_initial_board(self, pieces):
        """Creates the initial Board objects which is composed of 81 space objects
        with 4 corner spaces, and 18 spaces each occupied by 9 red and 9 black pieces"""

        board = []

        row_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        column_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}

        # Create an empty board
        for _ in row_map:
            board_row = []
            for _ in column_map:
                board_row.append(Square(None))
            board.append(list(board_row))

        # Designate corner spaces
        for row_corner in [0, 8]:
            for column_corner in [0, 8]:
                board[row_corner][column_corner].set_corner(True)

        # Place pieces on board
        for piece in pieces:
            row = piece.get_row()
            row_index = row_map.get(row)
            column = piece.get_column()
            column_index = column_map.get(column)
            board[row_index][column_index].set_occupant(piece)

        return board

    def board_map(self, square):
        row_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        column_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}

        square_row = square[:1]
        square_column = square[1:]

        row = row_map.get(square_row)
        column = column_map.get(square_column)

        return (row, column)

    def print_board(self):
        """Prints the Board object to the console"""

        row_labels = ['[a]', '[b]', '[c]', '[d]', '[e]', '[f]', '[g]', '[h]', '[i]']
        column_labels = ['   ', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']

        print(''.join(label for label in column_labels))
        for row in zip(row_labels, self._board):
            print_row = row[0]
            for space in row[1]:
                occupant = space.get_occupant()
                if occupant is not None:
                    if occupant.get_color() == 'RED':
                        print_row += '[R]'
                    elif occupant.get_color() == 'BLACK':
                        print_row += '[B]'
                else:
                    print_row += '[ ]'
            print(print_row)

    def get_square_occupant(self, square):
        """"""
        location = self.board_map(square)
        row = location[0]
        column = location[1]

        square = self._board[row][column]

        piece = square.get_occupant()

        if piece is None:
            return 'NONE'
        else:
            return piece.get_color()

    def validate_move(self, square_from, square_to):
        """"""
        move_horizontal = False
        move_vertical = False
        square_count = 0

        current_square = self.board_map(square_from)
        target_square = self.board_map(square_to)

        current_row = current_square[0]
        current_column = current_square[1]
        target_row = target_square[0]
        target_column = target_square[1]

        if current_row == target_row:
            move_horizontal = True

        if current_column == target_column:
            move_vertical = True

        if not (move_horizontal or move_vertical):
            print('Error: pieces can only move vertically or horizontally ')
            return False
        print('CR:', current_row)
        print('CC:', current_column)
        print('TR:', target_row)
        print('TC:', target_column)
        print('H:', move_horizontal)
        print('V:', move_vertical)

        if move_horizontal:
            square_count = target_column - current_column
            print(square_count)

        if move_vertical:
            square_count = target_row - current_row
            print(square_count)

            if square_count < 0:
                for each in range(-1, square_count-1, -1):
                    occupant = self._board[current_row + each][current_column].get_occupant()
                    if occupant is not None:
                        print("Error: you cannot jump over other pieces")
                        return False
            else:
                for each in range(1, square_count+1, 1):
                    print(self._board[current_row + each][current_column].get_occupant())


class Square:
    """Represents a space located on the Board"""

    def __init__(self, occupant, corner=False):
        """Creates a initial Square object"""
        self._occupant = occupant
        self._corner = corner

    def get_occupant(self):
        """Returns the space's current occupant: Black, Red or None"""
        return self._occupant

    def set_occupant(self, occupant):
        self._occupant = occupant

    def get_corner(self):
        """Returns True if space is a corner space, False if otherwise"""
        return self._corner

    def set_corner(self, corner):
        """"""
        self._corner = corner


class Piece:
    """Represent"""

    def __init__(self, row, column, color):
        """"""
        self._row = row
        self._column = column
        self._color = color

    def get_row(self):
        """"""
        return self._row

    def set_row(self, row):
        """"""
        self._row = row

    def get_column(self):
        """"""
        return self._column

    def set_column(self, column):
        """"""
        self._column = column

    def get_color(self):
        """"""
        return self._color


class Player:
    """Represents"""

    def __init__(self, pieces):
        """Creates a Player object"""
        self._active_pieces = pieces
        self._captured_pieces = []

    def get_active_pieces(self):
        """"""
        return self._active_pieces

    def get_captured_pieces(self):
        """"""
        return self._captured_pieces

    def remove_pieces(self, pieces):
        """"""
        pass


game = HasamiShogiGame()
game.print_board()
#print(game.get_square_occupant('a3'))
#print(game.get_square_occupant('i7'))
#print(game.get_square_occupant('f4'))
#game.make_move('a1','h1')
game.make_move('i1','f1')
#game.make_move('i1','h2')