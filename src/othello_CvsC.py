import pygame, sys, random
from pygame.locals import *

BACKGROUNDCOLOR = (255, 255, 255)
BLACK = (255, 255, 255)
BLUE = (0, 0, 255)
CELLWIDTH = 50
CELLHEIGHT = 50
PIECEWIDTH = 47
PIECEHEIGHT = 47
BOARDX = 35
BOARDY = 35
FPS = 40

def terminate():
    pygame.quit()
    sys.exit()

#Game starting
def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = 'none'

    board[3][3] = 'black'
    board[3][4] = 'white'
    board[4][3] = 'white'
    board[4][4] = 'black'

#build new board ([][])
def getNewBoard():
    board = []
    for i in range(8):
        board.append(['none'] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
        return False

    board[xstart][ystart] = tile

    if tile == 'black':
        otherTile = 'white'
    else:
        otherTile = 'black'

    tilesToFlip = []
    for xdirection, ydirection in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = 'none' # restore the empty space

    if len(tilesToFlip) == 0:   # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'black':
                xscore += 1
            if board[x][y] == 'white':
                oscore += 1
    return {'black':xscore, 'white':oscore}


def randomGoFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

#print len(tilesToFlip)
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
#       print x, y
        board[x][y] = tile
    return True

def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard

def isOnCorner(x, y):
    return (x == 0 or x == 7) and (y == 0 or y == 7)

#where we need to work on.
def getComputer1Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)

    random.shuffle(possibleMoves)

    return possibleMoves[0]

def getComputer2Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    for move in possibleMoves:
        if(isOnCorner(move[0],move[1])):
            return move
    random.shuffle(possibleMoves)
    return possibleMoves[0]
def isGameOver(board):
    if getValidMoves(mainBoard, computerTile) != []:
        return False
    if getValidMoves(mainBoard, playerTile) != []:
        return False
    return True


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

#random choosing who goes first.
#turn = randomGoFirst()
turn = 0

if turn == 0:
    playerTile = 'black'
    computerTile = 'white'
else:
    playerTile = 'white'
    computerTile = 'black'

windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
pygame.display.set_caption('Othello')


gameOver = False


while True:
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)
    if (gameOver == True):
        flag = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                flag = True
        if flag == True:
            break
    elif (gameOver == False and turn == 0):
        x, y = getComputer1Move(mainBoard, playerTile)
        makeMove(mainBoard, playerTile, x, y)
        savex, savey = x, y

        if getValidMoves(mainBoard, computerTile) != []:
            turn = 1
    
    elif (gameOver == False and turn == 1):
        x, y = getComputer2Move(mainBoard, computerTile)
        makeMove(mainBoard, computerTile, x, y)
        savex, savey = x, y

        if getValidMoves(mainBoard, playerTile) != []:
            turn = 0

    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)
    
    for x in range(8):
        for y in range(8):
            rectDst = pygame.Rect(BOARDX+x*CELLWIDTH+2, BOARDY+y*CELLHEIGHT+2, PIECEWIDTH, PIECEHEIGHT)
            if mainBoard[x][y] == 'black':
                windowSurface.blit(blackImage, rectDst, blackRect)
            elif mainBoard[x][y] == 'white':
                windowSurface.blit(whiteImage, rectDst, whiteRect)

    if gameOver == True or isGameOver(mainBoard):
        scorePlayer = getScoreOfBoard(mainBoard)[playerTile]
        scoreComputer = getScoreOfBoard(mainBoard)[computerTile]
        outputStr = gameoverStr + str(scorePlayer) + ":" + str(scoreComputer)
        text = basicFont.render(outputStr, True, BLACK, BLUE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        gameOver = True
    
    pygame.display.update()
    mainClock.tick(FPS)


