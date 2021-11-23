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

        self._red_player = Player(self._red_pieces, 'RED')
        self._black_player = Player(self._black_pieces, 'BLACK')

        self._game_state = 'UNFINISHED'

        self._active_player = self._black_player
        self._inactive_player = self._red_player

    def get_game_state(self):
        """"""
        return self._game_state

    def get_active_player(self):
        """"""
        return self._active_player.get_player_color()

    def get_num_captured_pieces(self, color):
        """"""
        if color == 'RED':
            return self._red_player.get_captured_pieces
        elif color == 'BLACK':
            return self._black_player.get_captured_pieces
        else:
            print('Not a valid color, please try again.')

    def get_square_occupant(self, text_square):
        """"""
        square = self._board.board_map(text_square)
        piece = self._board.get_piece(square)
        return piece.get_color()

    def generate_pieces(self):
        """"""
        piece_list = []
        for row in zip([0, 8], ['RED', 'BLACK']):
            for column in range(0, 9):
                piece_list.append(Piece(row[0], column, row[1]))

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

    def make_move(self, text_square_from, text_square_to):
        """"""
        # Confirm game is still unfinished
        if self._game_state != 'UNFINISHED':
            print("Error: Game has already been won")
            return False

        current = self._board.board_map(text_square_from)
        target = self._board.board_map(text_square_to)

        # Confirm active player is making move
        piece = self._board.get_piece(current)
        piece_color = piece.get_color()
        player_color = self._active_player.get_player_color()
        if player_color != piece_color:
            print('Error: Not active player')
            return False

        # Confirm move is Valid: orthogonal and along a clear path
        board_bool = self._board.validate_move(current, target)
        if board_bool is False:
            print('Error: move was not valid')

        # If move is valid, update square occupants
        current_square = self._board.get_square(current)
        target_square = self._board.get_square(target)
        current_square.set_occupant(None)
        target_square.set_occupant(piece)

        # If move is valid, update piece coordinates
        piece.set_row(target[0])
        piece.set_column(target[1])

        # If move is valid, check for capture
        active_pieces = self._active_player.get_active_pieces()
        inactive_pieces = self._inactive_player.get_active_pieces()
        captured_squares = self._board.check_capture(active_pieces, inactive_pieces, target)

        # If move is valid: switch turns
        active_player = self._active_player
        inactive_player = self._inactive_player

        self._active_player = inactive_player
        self._inactive_player = active_player

    def print_board(self):
        return self._board.print_board()

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
        for row in row_map:
            board_row = []
            for column in column_map:
                board_row.append(Square(row, column, None))
            board.append(list(board_row))

        # Designate corner spaces
        for row_corner in [0, 8]:
            for column_corner in [0, 8]:
                board[row_corner][column_corner].set_corner(True)

        # Place pieces on board
        for piece in pieces:
            row = piece.get_row()
            column = piece.get_column()
            board[row][column].set_occupant(piece)

        return board

    def board_map(self, text_square):
        row_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        column_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}

        square_row = text_square[:1]
        square_column = text_square[1:]

        row = row_map.get(square_row)
        column = column_map.get(square_column)

        return self._board[row][column]

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
        print()

    def get_square(self, square):
        """"""
        row = square[0]
        column = square[1]

        square = self._board[row][column]

        return square

    def get_piece(self, square):
        """"""
        row = square[0]
        column = square[1]

        square = self._board[row][column]

        piece = square.get_occupant()

        return piece

    def validate_move(self, current, target):
        """"""
        # Checks if move is orthogonal
        move_direction = self.check_direction(current, target)
        if move_direction == 'Invalid':
            return False

        # Checks if path between squares is clear
        path = self.check_path(move_direction, current, target)
        if path == 'Occupied':
            return False

        return True

    def check_direction(self, current, target):

        if (current[0] != target[0]) and (current[1] != target[1]):
            direction = 'Invalid'

        elif current[0] == target[0]:
            if current[1] - target[1] < 0:
                direction = ('Horizontal', 'Left')
            else:
                direction = ('Horizontal', 'Right')

        elif current[1] == target[1]:
            if current[0] - target[0] < 0:
                direction = ('Vertical', 'Down')
            else:
                direction = ('Vertical', 'Up')

        return direction

    def check_path(self, direction, current, target):
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

    def check_capture(self, friendly_pieces, enemy_pieces, target):
        """"""
        t_row = target[0]
        t_column = target[1]

        row_friendly = []
        column_friendly = []
        row_enemy = []
        column_enemy = []

        # Generate list of coordinates of all friendly pieces in same row and column
        for piece in friendly_pieces:
            row = piece.get_row()
            column = piece.get_column()

            # Skip over adding the target piece to the list
            if t_row == row and t_column == column:  # don't add target piece
                continue

            # If friendly piece is in same row as target, add piece's column to list
            if t_row == row:
                row_friendly.append(column)

            # If friendly piece is in same column as target, add piece's row to list
            elif t_column == column:
                column_friendly.append(row)

        # Generate list of coordinates of all enemy pieces in same row and column
        for piece in enemy_pieces:
            # If enemy piece is in same row as target, add piece's column to list
            if t_row == piece.get_row():
                row_enemy.append(piece.get_column())

            # If enemy piece is in same column as target, add piece's row to list
            elif t_column == piece.get_row():
                column_enemy.append(piece.get_column())

        print('RF', row_friendly)
        print('CF', column_friendly)
        print('RE', row_enemy)
        print('CE', column_enemy)
        print('RT', t_row)
        print('CT', t_column)

        capture_list = []

        looking_state = 0
        capture_state = 0

        x = 1
        if t_row + x in row_enemy:
            looking_state = 1
            x +=1
        while looking_state == 1 and capture_state == 0:
            if t_row + x in row_friendly:
                capture_state = 1
            elif t_row + x in row_enemy:
                looking_state = 1
            else:
                looking_state = 0

    def board_state(self):
        square_list = list(range(9))
        red_pieces = []
        black_pieces = []

        for row in square_list:
            for column in square_list:
                location = (row, column)
                piece = self.get_piece(location)
                if piece is None:
                    continue
                elif piece.get_color() == 'RED':
                    red_pieces.append(location)
                else:
                    black_pieces.append(location)

        return red_pieces, black_pieces


class Square:
    """Represents a space located on the Board"""

    def __init__(self, row, column, occupant, corner=False):
        """Creates a initial Square object"""
        self._row = row
        self._column = column
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

    def __init__(self, pieces, color):
        """Creates a Player object"""
        self._active_pieces = pieces
        self._captured_pieces = []
        self._color = color

    def get_player_color(self):
        return self._color

    def get_active_pieces(self):
        """"""
        return self._active_pieces

    def get_captured_pieces(self):
        """"""
        return self._captured_pieces

    def remove_pieces(self, pieces):
        """"""
        pass


def main():
    game = HasamiShogiGame()

    game.make_move('i4', 'c4')
    #game.print_board()

    game.make_move('a2', 'e2')
    #game.print_board()

    game.make_move('c4', 'c5')
    #game.print_board()

    game.make_move('a4', 'e4')
    #game.print_board()

    game.make_move('i3', 'e3')
    #game.print_board()

    game.make_move('a6', 'b6')
    #game.print_board()

    game.make_move('i5', 'd5')
    #game.print_board()

    game.make_move('b6', 'b5')
    #game.print_board()

    game.make_move('i6', 'e6')
    #game.print_board()

    game.make_move('a7', 'e7')
    #game.print_board()

    game.make_move('i9', 'h9')
    #game.print_board()

    game.make_move('a8', 'f8')
    #game.print_board()

    game.make_move('h9', 'i9')
    #game.print_board()

    game.make_move('f8', 'f5')
    #game.print_board()

    game.make_move('i9', 'h9')
    #game.print_board()

    game.make_move('f5', 'e5')
    game.print_board()

main()
