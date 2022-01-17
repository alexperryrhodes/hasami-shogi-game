# Author: Alexandra Rhodes
# Date: 12/27/21
# Description:

import pygame
from hasami_shogi.constants import WIDTH, HEIGHT, SQUARE_SIZE
from hasami_shogi.board import Board
from hasami_shogi.game import Game

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if game._move_state == True:
                    to_pos = pygame.mouse.get_pos()
                    to_row, to_column = get_row_col_from_mouse(to_pos)
                    game.make_move(from_row, from_column, to_row, to_column)
                    game._move_state = False
                
                else:
                    from_pos = pygame.mouse.get_pos()
                    from_row, from_column = get_row_col_from_mouse(from_pos)
                    game._move_state = True

        game.update()

    pygame.quit()

main()