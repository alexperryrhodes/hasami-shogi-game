# Author: Alexandra Rhodes
# Date: 11/22/21
# Description:

class HasamiShogiGame:
    """Represents a Game object"""

    def __init__(self):
        """Creates a initial Game object with initial conditions:
        Generates Red and Black Piece objects
        Passes list of entire list of Piece objects to Board Object
        Passes red Pieces to one Player object and black Pieces to another Player object
        Sets game state
        Sets active player to black player and inactive player to red player
        """

        self._pieces = self.generate_pieces()

        self._board = Board(self._pieces)

        self._game_state = 'UNFINISHED'

        self._active_player = 'BLACK'
        self._inactive_player = 'RED'

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def get_active_player(self):
        """Returns the active player"""
        return self._active_player

    def get_num_captured_pieces(self, color: str):
        """Returns the number of captured pieces by ask each piece it's status"""
        num_captured = 0
        for piece in self._pieces:
            piece_color = piece.get_color()
            piece_status = piece.get_status()

            if piece_color == color and piece_status == 'CAPTURED':
                num_captured += 1

        return num_captured

    def get_square_occupant(self, str_square: str):
        """Returns the color on a square by asking the Board for it's Square at the parameter location
        and then the Square checking it's occupant and if the occupant is a Piece, then ask the Piece for it's color
        otherwise returns None"""
        occupant = self._board.get_square_occupant(str_square)
        if occupant is None:
            return 'NONE'
        else:
            return occupant.get_color()

    @staticmethod
    def generate_pieces():
        """Generates a initial list of Piece objects with a specified color"""
        piece_list = []
        for count in range(9):
            for color in ['RED', 'BLACK']:
                piece_list.append(Piece(color))

        return piece_list

    def make_move(self, str_square_from: str, str_square_to: str):
        """"""
        # Confirm game is still unfinished
        if self._game_state != 'UNFINISHED':
            print("Error: Game has already been won")
            return False

        # Confirm there is a piece on starting square
        piece = self._board.get_square_occupant(str_square_from)
        if piece is None:
            print("Error: There is no piece on the staring square")
            return False

        # Confirm the active player is making a move
        piece_color = piece.get_color()
        if self._active_player != piece_color:
            print("Error: Active player is ", self._active_player)
            return False

        # Confirm move is Valid: orthogonal and along a clear path
        valid_move = self._board.validate_move(str_square_from, str_square_to)
        if valid_move is False:
            print('Error: Move was not valid')
            return False

        # If move is valid, update square occupants
        self._board.set_square_occupant(str_square_from, None)
        self._board.set_square_occupant(str_square_to, piece)

        # If move is valid, check for capture, then update captures squares and pieces
        captured_squares = self._board.check_capture(str_square_to)
        for square_group in captured_squares:
            for square in square_group:
                piece = square.get_occupant()
                piece.set_status('CAPTURED')
                square.set_occupant(None)

        # Check for winner
        self.check_winner()
        if self._game_state != 'UNFINISHED':
            print(self._game_state)

        # If move is valid: switch turns
        active_player = self._active_player
        inactive_player = self._inactive_player
        self._active_player = inactive_player
        self._inactive_player = active_player

    def check_winner(self):
        """"""
        if self.get_num_captured_pieces('RED') == 9:
            self._game_state = 'BLACK_WON'
        elif self.get_num_captured_pieces('BLACK') == 9:
            self._game_state = 'RED_WON'
        else:
            self._game_state = 'UNFINISHED'


    def print_board(self):
        """Asks the Board to call it's print board function"""
        self._board.print_board()


class Board:
    """Represents a Board object within Hasami Shogi"""

    def __init__(self, pieces):
        """Creates the initial Board object by calling a make board function"""
        self._board = self._make_initial_board(pieces)

    @staticmethod
    def _make_initial_board(pieces):
        """Creates the initial Board objects which is composed of 81 Square objects.
        It then designates 4 square objects as corner squares and then sets 18 Piece objects
        as occupants of the squares"""

        board = []

        # Create an empty board
        for row in range(9):
            board_row = []
            for column in range(9):
                board_row.append(Square(row, column, None))
            board.append(list(board_row))

        # Designate corner spaces
        for row_corner in [0, 8]:
            for column_corner in [0, 8]:
                board[row_corner][column_corner].set_corner(True)

        # Place pieces on board
        for piece in pieces:
            piece_color = piece.get_color()
            for column in range(9):
                if piece_color == 'RED':
                    board[0][column].set_occupant(piece)
                elif piece_color == 'BLACK':
                    board[8][column].set_occupant(piece)
                else:
                    continue

        return board

    def get_square(self, str_square: str):
        """Takes in a string location (a1) and returns the Square object at the location"""
        row_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        column_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}

        square_row = str_square[:1]
        square_column = str_square[1:]

        row = row_map.get(square_row)
        column = column_map.get(square_column)

        return self._board[row][column]

    def get_square_occupant(self, str_square: str):
        """Takes in a string location (a1) and asks that Square for it's occupant and returns the occupant"""
        square = self.get_square(str_square)
        occupant = square.get_occupant()
        return occupant

    def set_square_occupant(self, str_square: str, piece):
        """Takes in a string location (a1) and a Piece object and asks that Square to set its occupant to the Piece"""
        square = self.get_square(str_square)
        square.set_occupant(piece)

    def validate_move(self, str_square_from, str_square_to):
        """Takes in two string location (a1) and returns a boolean in the move between the squares is valid"""
        from_row = self.get_square(str_square_from).get_row()
        from_column = self.get_square(str_square_from).get_column()
        to_row = self.get_square(str_square_to).get_row()
        to_column = self.get_square(str_square_to).get_column()

        direction = self.check_direction(from_row, from_column, to_row, to_column)
        if direction is False:
            print('Error: Pieces can only move vertically or horizontally')
            return False

        check_path = self.check_path(direction, from_row, from_column, to_row, to_column)
        if check_path is False:
            print('Error: Path between squares contains pieces')
            return False

    @staticmethod
    def check_direction(from_row, from_column, to_row, to_column):
        """Takes in four coordinates and determines the direction of movement between coordinates"""
        vertical = from_row - to_row
        horizontal = from_column - to_column

        if abs(vertical) > 0 and abs(horizontal) > 0:
            return False

        if vertical < 0:
            direction = (1, 0)
        elif vertical > 0:
            direction = (-1, 0)
        elif horizontal > 0:
            direction = (0, -1)
        else:
            direction = (0, 1)

        return direction

    def check_path(self, direction, from_row, from_column, to_row, to_column):
        """Takes in four coordinates and a direction and determines if the path between the coordinates is clear"""
        row_step = direction[0]
        column_step = direction[1]

        next_row = from_row
        next_column = from_column

        step_state = 1
        while step_state == 1:
            next_row = next_row + row_step
            next_column = next_column + column_step
            square = self._board[next_row][next_column]
            occupant = square.get_occupant()
            if occupant is not None:
                return False
            if self._board[next_row][next_column] == self._board[to_row][to_column]:
                step_state = 0

    def check_capture(self, str_square_to):
        """"""
        row = self.get_square(str_square_to).get_row()
        column = self.get_square(str_square_to).get_column()
        piece_color = self.get_square(str_square_to).get_occupant().get_color()

        potential_captures = []
        captured_squares = []

        for step in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            looking_state = 1
            capture_state = 0
            next_row = row
            next_column = column
            while looking_state == 1 and capture_state == 0:
                next_row = next_row + step[0]
                next_column = next_column + step[1]

                # Check if step moves off board, if so move in new direction
                if next_row > 8 or next_row < 0 or next_column > 8 or next_column < 0:
                    looking_state = 0
                    continue

                # Check is next square is occupied, if not, move in new direction
                square = self._board[next_row][next_column]
                occupant = square.get_occupant()
                if occupant is None:
                    looking_state = 0
                    continue

                next_color = occupant.get_color()

                # If the next piece is the opposite color add square to potential captures
                if piece_color != next_color:
                    potential_captures.append(square)

                # If the next piece is the same color, and at least one opposite color between has been captures
                # end looking and set potential captures as actual captures
                elif piece_color == next_color and len(potential_captures) > 0:
                    capture_state = 1
                    captured_squares.append(potential_captures)
                    potential_captures = []

                else:
                    looking_state = 0
                    continue

        return captured_squares

    def print_board(self):
        """Prints the Board object to the console"""

        row_labels = ['[a]', '[b]', '[c]', '[d]', '[e]', '[f]', '[g]', '[h]', '[i]']
        column_labels = ['   ', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']

        print(''.join(label for label in column_labels))
        for row in zip(row_labels, self._board):
            print_row = row[0]
            for square in row[1]:
                piece = square.get_occupant()
                if piece is not None:
                    if piece.get_color() == 'RED':
                        print_row += '[R]'
                    elif piece.get_color() == 'BLACK':
                        print_row += '[B]'
                else:
                    print_row += '[ ]'
            print(print_row)
        print()


class Square:
    """Represents a Square object within a Hasami Shogi Board Object"""

    def __init__(self, row, column, occupant, corner=False):
        """Creates a initial Square object that has row and column coordinates, a Piece object if occupied or
        None if empty and a boolean to indicate if it is a corner Square"""
        self._row = row
        self._column = column
        self._occupant = occupant
        self._corner = corner

    def get_occupant(self):
        """Returns the Squares current occupant: A Piece object or None"""
        return self._occupant

    def set_occupant(self, occupant):
        """Sets a Piece object on the square"""
        self._occupant = occupant

    def get_corner(self):
        """Returns True if Square is a corner Square, False if otherwise"""
        return self._corner

    def set_corner(self, corner):
        """Updates the boolean to set if this Square is a corner Square"""
        self._corner = corner

    def get_row(self):
        """Returns the Square's row"""
        return self._row

    def get_column(self):
        """Returns the Square's column"""
        return self._column


class Piece:
    """Represents a Piece object within Hasami Shogi"""

    def __init__(self, color):
        """"""
        self._color = color
        self._status = 'ACTIVE'

    def get_color(self):
        """Returns the Piece's color"""
        return self._color

    def get_status(self):
        """Returns the Piece's color"""
        return self._status

    def set_status(self, status):
        """Returns the Piece's color"""
        self._status = status


def main():
    game = HasamiShogiGame()
    game.print_board()

    game.make_move('i4', 'c4')

    game.make_move('a2', 'e2')

    game.make_move('c4', 'c5')

    game.make_move('a4', 'e4')

    game.make_move('i3', 'e3')

    game.make_move('a6', 'b6')

    game.make_move('i5', 'd5')

    game.make_move('b6', 'b5')

    game.make_move('i6', 'e6')

    game.make_move('a7', 'e7')

    game.make_move('i9', 'h9')

    game.make_move('a8', 'f8')

    game.make_move('h9', 'i9')

    game.make_move('f8', 'f5')

    game.make_move('i9', 'h9')

    game.print_board()
    game.make_move('f5', 'e5')
    game.print_board()


main()
