class Piece:
    """Represents a Piece object within Hasami Shogi"""

    def __init__(self, color: str):
        """"""
        self._color = color
        self._status = 'ACTIVE'

    def get_color(self):
        """Returns the Piece's color"""
        return self._color

    def get_status(self):
        """Returns the Piece's color"""
        return self._status

    def set_status(self, status: str):
        """Returns the Piece's color"""
        self._status = status