import pygame, sys, random
from pygame.locals import *
from constants import *
from operations import *
from players import *

#where we need to work on.
def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)

    random.shuffle(possibleMoves)

    return possibleMoves[0]

pygame.init()
mainClock = pygame.time.Clock()

boardImage = pygame.image.load('board.png')
boardRect = boardImage.get_rect()
blackImage = pygame.image.load('black.png')
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load('white.png')
whiteRect = whiteImage.get_rect()

basicFont = pygame.font.SysFont(None, 48)
gameoverStr = 'Game Over Score '

mainBoard = getNewBoard()
resetBoard(mainBoard)

windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
pygame.display.set_caption('Othello')

gameOver = False

player1 = SetPlayer('human')
player2 = SetPlayer('mix')
players = [player1, player2]
playersTile = [BLACK, WHITE]
now = 0

while True:
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)
    
    for x in range(8):
        for y in range(8):
            rectDst = pygame.Rect(BOARDX+x*CELLWIDTH+2, BOARDY+y*CELLHEIGHT+2, PIECEWIDTH, PIECEHEIGHT)
            if mainBoard[x][y] == BLACK:
                windowSurface.blit(blackImage, rectDst, blackRect)
            elif mainBoard[x][y] == WHITE:
                windowSurface.blit(whiteImage, rectDst, whiteRect)
    if isGameOver(mainBoard):
        scorePlayer = getScoreOfBoard(mainBoard)[playersTile[0]]
        scoreComputer = getScoreOfBoard(mainBoard)[playersTile[1]]
        outputStr = gameoverStr + str(scorePlayer) + ":" + str(scoreComputer)
        text = basicFont.render(outputStr, True, BLACK_COLOR, BLUE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        break
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
    
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)

    if (gameOver == False):
        x, y = players[now].getMove(mainBoard, playersTile[now])
        makeMove(mainBoard, playersTile[now], x, y)

        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
    
    mainClock.tick(FPS)

raw_input("")
