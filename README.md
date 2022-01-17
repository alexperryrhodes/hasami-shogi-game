# Hasami Shogi

This was a portfolio project created for my CS162 class. The original speciations were to create a version of the board game Hasami Shogi using the rules for "**Variant 1**" on [the Wikipedia page](https://en.wikipedia.org/wiki/Hasami_shogi). There did not need to be any physical representation of the board as game would be played using "algebraic notation", with rows labeled a-i and rows labeled 1-9. We were given a few specific methods that needed to be included, otherwise any implantation of the game was allowed.

I implemented my project by creating four classes: the board, the squares on the board, the pieces on the squares and the game itself. The board object was created as a list of lists. The most challenging parts of the project were accounting for literal corner cases for corner captures and validated each move. 

Overall it was a very fun project. My original game looked like this:

![](original.jpg)

After the class concluded, I chose to add onto the game by creating a GUI version with pygame. My goals for the first implementation:

- Draw the board
- Draw the pieces in the correct place on the board
- Move piece to new square with two mouse clicks

The project had a few challenges. The biggest challenge was implementing the mouse click logic as two separate clicks needed to be captured. I solved this by creating a move_state data member to game, which allowed mouse clicks to be differentiated. Here is a gif of the game in it's current state:


I want to continue to work on the project. My next steps are:
- Add more visual cues to uses including:
    * Highlighting selected square
    * Coloring squares that are valid to move to
    * Text indicating current player's turn
- Allow user to unselect piece they selected before choosing square to move to
- Create messages for start and end of game
- Allow user to restart game