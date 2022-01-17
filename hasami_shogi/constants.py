# Author: Alexandra Rhodes
# Date: 12/27/21
# Description:


import pygame
import os

BOARD_SIZE = 9

SQUARE_SIZE = 100

WIDTH = BOARD_SIZE*SQUARE_SIZE
HEIGHT = BOARD_SIZE*SQUARE_SIZE

PIECE_SIZE = SQUARE_SIZE*.8

PIECE_MARGIN = 10

GAME_PLAYERS = ['RED', 'BLACK']
PLAYER_1 = GAME_PLAYERS[0]
PLAYER_2 = GAME_PLAYERS[1]

BLACK = (0, 0, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hasami Shogi')

WOOD =  pygame.transform.scale(pygame.image.load(
    os.path.join('hasami_shogi','Assets', 'wood.jpeg')), (WIDTH, HEIGHT))

BLACK_PIECE_IMAGE =  pygame.transform.scale(pygame.image.load(
    os.path.join('hasami_shogi','Assets', 'black_piece.png')), (WIDTH, HEIGHT))

RED_PIECE_IMAGE =  pygame.transform.scale(pygame.image.load(
os.path.join('hasami_shogi','Assets', 'red_piece.png')), (WIDTH, HEIGHT))


BLACK_PIECE = pygame.transform.scale(BLACK_PIECE_IMAGE, (PIECE_SIZE, PIECE_SIZE))

RED_PIECE = pygame.transform.scale(RED_PIECE_IMAGE, (PIECE_SIZE, PIECE_SIZE))
