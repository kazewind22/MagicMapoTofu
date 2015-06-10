import pygame, sys, random
from pygame.locals import *
from constants import *
from operations import *
from grader import *
from players_noGUI import *

class SetPlayer:
    def __init__(self, Type):
        self.player = self.setSolver(Type)
        self.playerType = Type
    def setSolver(self, Type):
        return {
            'human':Human(),
            'random':RandomAI(),
            'corner':CornerAI(),
            'cornerside':CornerSideAI(),
            'mix':EndAllWithMinMaxAI(),
            'sauce':LiyianAI(),
        }.get(Type, RandomAI())
    def getMove(self, board, Tile):
        return self.player.getMove(board, Tile)

class Human:
    def getMove(self, board, Tile):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    col = int((x-BOARDX)/CELLWIDTH)
                    row = int((y-BOARDY)/CELLHEIGHT)
                    if isValidMove(board, Tile, col, row) != False:
                        return [col, row]   
