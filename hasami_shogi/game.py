import pygame
from .constants import BOARD_SIZE, GAME_PLAYERS, PLAYER_1, PLAYER_2, WIN
from .board import Board
from .piece import Piece


class Game:
    """Represents a Game object"""

    def __init__(self):
        """Creates a initial Game object with initial conditions:
        Generates a list of Piece objects equal to 2x the size of the board
        Passes list of entire list of Piece objects to Board Object
        Sets game state
        Sets active player to Player_2 and inactive player to Player_1
        """
        self._pieces = self._generate_pieces()
        self._board = Board(self._pieces)
        self._game_state = 'UNFINISHED'
        self._active_player = PLAYER_2
        self._inactive_player = PLAYER_1
        self._win = WIN
        self._move_state = False

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

    def get_square_occupant(self, row:int, column: int):
        """Returns a Square occupant by asking the Board for it's Square at the row, column 
        and then the Square checking it's occupant and if the occupant is a Piece, otherwise returns None"""
        occupant = self._board.get_square_occupant(row,column)
        return occupant

    @staticmethod
    def _generate_pieces():
        """Generates a initial list of Piece objects with a specified color"""
        piece_list = []
        for count in range(BOARD_SIZE):
            for color in GAME_PLAYERS:
                piece_list.append(Piece(color))

        return piece_list

    def update(self):
        """Asks the Board object to draw board"""
        self._board.draw(self._win)
        pygame.display.update()

    def make_move(self, from_row: int, from_column: int, to_row: int, to_column: int):
        """After first confirming move is valid, make_move moves piece between squares, checks for captures and checks
        for and updates game state and active player"""
        # Confirm game is still unfinished
        if self._game_state != 'UNFINISHED':
            print("Error: Game has already been won")
            return False

        # Confirm there is a piece on starting square
        occupant = self._board.get_square_occupant(from_row, from_column)
        if occupant is None:
            print("Error: There is no piece on the staring square")
            return False

        # Confirm the active player is making a move
        piece_color = occupant.get_color()
        if self._active_player != piece_color:
            print("Error: Active player is", self._active_player)
            return False

        # Confirm move is valid
        valid_move = self._board.validate_move(from_row, from_column, to_row, to_column)
        if valid_move is False:
            print('Error: Move was not valid')
            return False

        # If move is valid, update square occupants
        self._board.set_square_occupant(from_row, from_column, None)
        self._board.set_square_occupant(to_row, to_column, occupant)

        # If move is valid, check for capture
        # If there are captures print a message
        # Then update captures squares and pieces
        captured_squares = self._board.check_capture(to_row, to_column)
        corner_captured_squares = self._board.check_corner_capture(to_row, to_column)
        captured_squares = captured_squares + corner_captured_squares
        for cap_square in captured_squares:
            print(self._inactive_player, 'piece on', chr(cap_square.get_row()+97)+str(cap_square.get_column()+1), 'captured')
            cap_piece = cap_square.get_occupant()
            cap_piece.set_status('CAPTURED')
            cap_square.set_occupant(None)

        self._board.print_board()

        # Check for winner and update game state
        # If there is a winner, print message
        self._check_winner()
        if self._game_state != 'UNFINISHED':
            print(self._game_state)

        # If move is valid: switch turns
        active_player = self._active_player
        inactive_player = self._inactive_player
        self._active_player = inactive_player
        self._inactive_player = active_player

        return True

    def _check_winner(self):
        """Checks if there is a winner meaning the opposing player has one or fewer pieces"""
        if self.get_num_captured_pieces(PLAYER_1) >= BOARD_SIZE-1:
            self._game_state = PLAYER_2+'_WON'
        elif self.get_num_captured_pieces(PLAYER_2) >= BOARD_SIZE-1:
            self._game_state = PLAYER_1+'_WON'
        else:
            self._game_state = 'UNFINISHED'

    def print_board(self):
        """Asks the Board to call it's print board function"""
        self._board.print_board()

