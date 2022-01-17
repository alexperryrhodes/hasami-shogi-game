class Square:
    """Represents a Square object within a Hasami Shogi Board Object"""

    def __init__(self, row, column, occupant, corner=False):
        """Creates a initial Square object that has row and column coordinates, a Piece object if occupied or
        None if empty and a boolean to indicate if it is a corner Square"""
        self._row = row
        self._column = column
        self._occupant = occupant
        self._corner = corner
        self._selected = False
        self._in_path = False

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
