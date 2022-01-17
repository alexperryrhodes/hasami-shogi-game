import pygame.draw

from .square import Square
from .constants import BOARD_SIZE, PLAYER_1, PLAYER_2, BLACK, SQUARE_SIZE, WOOD, BLACK_PIECE, RED_PIECE, PIECE_MARGIN


class Board:
    """Represents a Board object within Hasami Shogi"""

    def __init__(self, pieces):
        """Creates the initial Board object by calling a make board function"""
        self._board = self._make_initial_board(pieces)

    @staticmethod
    def _make_initial_board(pieces):
        """Creates the initial Board objects which is composed of BOARD_SIZE^2 Square objects.
        It then designates 4 square objects as corner squares and then sets BOARD_SIZE*2 Piece objects
        as occupants of the squares"""
        board = []

        # Create an empty board
        for row in range(BOARD_SIZE):
            board_row = []
            for column in range(BOARD_SIZE):
                board_row.append(Square(row, column, None))
            board.append(list(board_row))

        # Designate corner spaces
        for row_corner in [0, BOARD_SIZE-1]:
            for column_corner in [0, BOARD_SIZE-1]:
                board[row_corner][column_corner].set_corner(True)

        # Place pieces on board
        top_column = 0
        bottom_column = 0
        for piece in pieces:
            piece_color = piece.get_color()
            if piece_color == PLAYER_1:
                board[0][top_column].set_occupant(piece)
                top_column += 1
            elif piece_color == PLAYER_2:
                board[BOARD_SIZE-1][bottom_column].set_occupant(piece)
                bottom_column += 1
            else:
                continue

        return board

    def get_board(self):
        return self._board

    def get_square(self, row:int, column: int):
        """Takes in a row and column and returns the Square object at the location"""
        return self._board[row][column]

    def get_square_occupant(self, row:int, column: int):
        """Takes in a string location (a1) and asks that Square for it's occupant and returns the occupant"""
        square = self.get_square(row, column)
        occupant = square.get_occupant()
        return occupant

    def set_square_occupant(self, row:int, column: int, piece):
        """Takes in a row and column and a Piece object and asks that Square to set its occupant to that Piece"""
        square = self.get_square(row, column)
        square.set_occupant(piece)

    def validate_move(self, from_row: int, from_column: int, to_row: int, to_column: int):
        """Takes in two string location (a1) and returns False if the move between the squares is valid"""

        direction = self._check_direction(from_row, from_column, to_row, to_column)
        if direction is False:
            print('Error: Pieces can only move vertically or horizontally')
            return False

        check_path = self._check_path(direction, from_row, from_column, to_row, to_column)
        if check_path is False:
            print('Error: Path between squares contains pieces')
            return False

    @staticmethod
    def _check_direction(from_row: int, from_column: int, to_row: int, to_column: int):
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

    def _check_path(self, direction, from_row: int, from_column: int, to_row: int, to_column: int):
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

    def check_capture(self, row: int, column: int):
        """Checks if there are any potential captures by stepping in all four directions around the square and
        looking for the sandwich pattern of the pieces"""
        piece_color = self.get_square(row, column).get_occupant().get_color()

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
                if next_row > BOARD_SIZE-1 or next_row < 0 or next_column > BOARD_SIZE-1 or next_column < 0:
                    looking_state = 0
                    potential_captures = []
                    continue

                # Check is next square is occupied, if not, move in new direction
                square = self._board[next_row][next_column]
                occupant = square.get_occupant()
                if occupant is None:
                    looking_state = 0
                    potential_captures = []
                    continue

                next_color = occupant.get_color()

                # If the next piece is the opposite color add square to potential captures
                if piece_color != next_color:
                    potential_captures.append(square)

                # If the next piece is the same color, and at least one opposite color between has been captures
                # end looking and set potential captures as actual captures
                elif piece_color == next_color and len(potential_captures) > 0:
                    capture_state = 1
                    captured_squares.extend(potential_captures)
                    potential_captures = []

                else:
                    looking_state = 0
                    potential_captures = []
                    continue

        return captured_squares

    def check_corner_capture(self,  row: int, column: int):
        """Checks specifically to see if a corner capture has occurred"""
        piece_color = self.get_square(row, column).get_occupant().get_color()

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
                if next_row > BOARD_SIZE-1 or next_row < 0 or next_column > BOARD_SIZE-1 or next_column < 0:
                    looking_state = 0
                    continue

                # Check is next square is occupied, if not, move in new direction
                square = self._board[next_row][next_column]
                corner = square.get_corner()
                occupant = square.get_occupant()
                if occupant is None or corner is False:
                    looking_state = 0
                    continue

                next_color = occupant.get_color()

                # If the next piece is the opposite color add square to potential captures
                if piece_color != next_color:
                    potential_captures.append(square)

                else:
                    looking_state = 0
                    continue

                if next_row == next_column:
                    adj_row, adj_column = column, row
                elif row == 0:
                    adj_row = row + 1
                    adj_column = column + 1
                elif row == 1:
                    adj_row = row - 1
                    adj_column = column - 1
                elif row == BOARD_SIZE - 2:
                    adj_row = row + 1
                    adj_column = column + 1
                elif row == BOARD_SIZE - 1:
                    adj_row = row - 1
                    adj_column = column - 1
                else:
                    continue

                adj_square = self._board[adj_row][adj_column]
                adj_occupant = adj_square.get_occupant()
                if adj_occupant is None:
                    looking_state = 0
                    continue

                adj_color = adj_occupant.get_color()

                # If the next piece is the same color, and at least one opposite color between has been captures
                # end looking and set potential captures as actual captures
                if piece_color == adj_color:
                    capture_state = 1
                    captured_squares.extend(potential_captures)
                    potential_captures = []

                else:
                    looking_state = 0
                    continue

        return captured_squares

    def draw(self, win):
        win.blit(WOOD, (0,0))
        for line in range(BOARD_SIZE):
            pygame.draw.line(win, BLACK, (line * 100, 0), (line * 100, BOARD_SIZE * 100))
            pygame.draw.line(win, BLACK, (0, line * 100), (BOARD_SIZE * 100, line * 100))

        for row in self._board:
            for square in row:
                square_row = square.get_row()
                square_col = square.get_column()
                piece = square.get_occupant()
                if piece is not None:
                    if piece.get_color() == PLAYER_1:
                        win.blit(RED_PIECE, (square_col*SQUARE_SIZE+PIECE_MARGIN, square_row* SQUARE_SIZE+PIECE_MARGIN))
                    elif piece.get_color() == PLAYER_2:
                        win.blit(BLACK_PIECE,(square_col*SQUARE_SIZE+PIECE_MARGIN, square_row* SQUARE_SIZE+PIECE_MARGIN))


    def print_board(self):
        """Prints the Board object to the console"""
        row_labels = []
        column_labels = ['   ']
    
        for row in range(BOARD_SIZE):
            row = chr(row+97)
            row = '['+row+']'
            row_labels.append(row)
    
        for column in range(BOARD_SIZE):
            column = str(column + 1)
            column = '['+column+']'
            column_labels.append(column)
    
        print(''.join(label for label in column_labels))
        for row in zip(row_labels, self._board):
            print_row = row[0]
            for square in row[1]:
                piece = square.get_occupant()
                if piece is not None:
                    if piece.get_color() == PLAYER_1:
                        print_row += '['+PLAYER_1[:1]+']'
                    elif piece.get_color() == PLAYER_2:
                        print_row += '['+PLAYER_2[:1]+']'
                else:
                    print_row += '[ ]'
            print(print_row)
        print()
