import pygame, sys, random
from pygame.locals import *
from constants import *
from operations import *
from players import *
import time

def terminate():
    pygame.quit()
    sys.exit()

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

advisor1 = Fisrt8AI('./count_win.txt')
advisor2 = Fisrt8AI('./count_win_Yuehs_271_BLACK.txt')
advisor3 = Fisrt8AI('./count_win_Yuehs_271_WHITE.txt')

player0 = SetPlayer('human')

player1 = SetPlayer('sauce')
player1.player.setgrader(Yuehs_271())
player1.player.setfBound(8)
player1.player.setadvise(advisor2,BLACK)
player1.player.setadvise(advisor3,WHITE)
player1.player.setsBound(13)
player1.player.setxLevel(2)

player2 = SetPlayer('sauce')
player2.player.setgrader(Kart())
player2.player.setfBound(8)
player2.player.setadvise(advisor1,BLACK)
player2.player.setadvise(advisor1,WHITE)
player2.player.setsBound(13)
player2.player.setxLevel(2)

players = [player0, player2]
playersTile = [BLACK, WHITE]
playersWins = [0, 0]
#random.seed(7122)
starttime = time.clock()
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
    if gameOver == True or isGameOver(mainBoard):
        score = getScoreOfBoard(mainBoard)
        scorePlayer = score[playersTile[0]]
        scoreComputer = score[playersTile[1]]
        if score[0] != score[1]:
            playersWins[score[0]<score[1]]+=1
        gameOver = True
        outputStr = gameoverStr + str(scorePlayer) + ":" + str(scoreComputer)
        text = basicFont.render(outputStr, True, BLACK_COLOR, BLUE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if gameOver == True and event.type == MOUSEBUTTONDOWN and event.button == 1:
            terminate()
            
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)

    if (gameOver == False):
        x, y = players[now].getMove(mainBoard, playersTile[now])
        if makeMove(mainBoard, now, x, y) == False and players[now] != player0:
            print 'bad AI ' + playersTile[now] + ' made a invalid move!'
            gameOver = True
        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
    mainClock.tick(FPS)

raw_input("")
