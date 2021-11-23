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
        # Confirm active player is making move
        square_from_occupant = self._board.get_piece(square_from)
        square_from_occupant_color = square_from_occupant.get_color()
        if self._active_player != square_from_occupant_color:
            print('Error: Not active player')
            return False

        # Confirm move is Valid: orthogonal and along a clear path
        board_bool = self._board.validate_move(square_from, square_to)
        if board_bool is False:
            print('Error: move was not valid')

        # If move is valid, update square occupants
        current_square = self._board.get_square(square_from)
        target_square = self._board.get_square(square_to)
        current_square.set_occupant(None)
        target_square.set_occupant(square_from_occupant)

        # If move is valid: switch turns
        if self._active_player == 'BLACK':
            self._active_player = 'RED'
        else:
            self._active_player = 'BLACK'

    def get_square_occupant(self, square):
        """"""
        piece = self._board.get_piece()
        return piece.get_color()

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

    def get_square(self, square):
        """"""
        location = self.board_map(square)
        row = location[0]
        column = location[1]

        square = self._board[row][column]

        return square

    def get_piece(self, square):
        """"""
        location = self.board_map(square)
        row = location[0]
        column = location[1]

        square = self._board[row][column]

        piece = square.get_occupant()

        if piece is None:
            return 'NONE'
        else:
            return piece

    def validate_move(self, square_from, square_to):
        """"""
        current_square = self.board_map(square_from)
        target_square = self.board_map(square_to)

        # Checks if move is orthogonal
        move_direction = self.move_direction(current_square, target_square)
        if move_direction == 'Invalid':
            return False

        # Checks if path between squares is clear
        path = self.empty_path_check(move_direction,current_square, target_square)
        if path == 'Occupied':
            return False

        return True

    def move_direction(self, current_square, target_square):

        if (current_square[0] != target_square[0]) and (current_square[1] != target_square[1]):
            move_direction = 'Invalid'

        elif current_square[0] == target_square[0]:
            if current_square[1] - target_square[1] < 0:
                move_direction = ('Horizontal', 'Left')
            else:
                move_direction = ('Horizontal', 'Right')

        elif current_square[1] == target_square[1]:
            if current_square[0] - target_square[0] < 0:
                move_direction = ('Vertical', 'Down')
            else:
                move_direction = ('Vertical', 'Up')

        return move_direction

    def empty_path_check(self, direction,  current, target):
        path = 'Clear'
        c_row = current[0]
        c_column = current[1]
        t_row = target[0]
        t_column = target[1]

        if direction[1] == 'Up':
            square_list = list(range(c_row - 1, t_row - 1, -1))
        elif direction[1] == 'Down':
            square_list = list(range(c_row + 1, t_row + 1, 1))
        elif direction[1] == 'Left':
            square_list = list(range(c_column + 1, t_column - 1, -1))
        else:
            square_list = list(range(c_column + 1, t_column + 1, 1))

        if direction[0] == 'Vertical':
            for square in square_list:
                occupant = self._board[square][c_column].get_occupant()
                if occupant is not None:
                    path = 'Occupied'
                    return path
        elif direction[0] == 'Horizontal':
            for square in square_list:
                occupant = self._board[c_row][square].get_occupant()
                if occupant is not None:
                    path = 'Occupied'
                    return path

        return path


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
print('New Game\n')

game.make_move('i1', 'f1')
game.print_board()
print('Black moves Vertical Up\n')

game.make_move('a1', 'e1')
game.print_board()
print('Red moves Vertical Down\n')

game.make_move('f1', 'f6')
game.print_board()
print('Black moves Horizontal Right\n')

game.make_move('e1', 'e9')
game.print_board()
print('Red moves Horizontal Right\n')

game.make_move('f6', 'g6')
game.print_board()
print('Black moves Vertical Down\n')

game.make_move('e9', 'c9')
game.print_board()
print('Red moves Vertical Up\n')

game.make_move('g6', 'g2')
game.print_board()
print('Black moves Horizontal Left\n')

game.make_move('c9', 'c5')
game.print_board()
print('Red moves Horizontal Left\n')

