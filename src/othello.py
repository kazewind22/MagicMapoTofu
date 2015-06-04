import pygame, sys, random
import copy
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
_BLACK_=0
_WHITE_=1
_NONE_=2

def terminate():
    pygame.quit()
    sys.exit()
#Game starting
def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = _NONE_

    board[3][3] = _BLACK_
    board[3][4] = _WHITE_
    board[4][3] = _WHITE_
    board[4][4] = _BLACK_

#build new board ([][])
def getNewBoard():
    board = []
    for i in range(8):
        board.append([_NONE_] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != _NONE_:
        return False

    board[xstart][ystart] = tile

    if tile == _BLACK_:
        otherTile = _WHITE_
    else:
        otherTile = _BLACK_

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

    board[xstart][ystart] = _NONE_ # restore the empty space

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
    cnt=[0,0,0]
    for x in range(8):
        for y in range(8):
            cnt[board[x][y]]+=1
    return (cnt[0], cnt[1])


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

def isOnGoodSide(x, y):
    if(x == 0 or x == 7):
        return y != 1 and y != 6
    if(y == 0 or y == 7):
        return x != 1 and x != 6
    return False

def isGameOver(board):
    if getValidMoves(mainBoard, _BLACK_) != []:
        return False
    if getValidMoves(mainBoard, _WHITE_) != []:
        return False
    return True

    
def opponentTile(myTile):
    if myTile >= 2:
        return _NONE_
    return myTile^1

def getBoardId(board):
    ID1 = 0
    ID2 = 0
    ID3 = 0
    ID4 = 0
    for x in range(8):
        for y in range(8):
            ID1+=board[x][y]<<((8*x+y)*2)
            ID2+=board[x][y]<<((8*y+x)*2)
            ID3+=board[x][y]<<((8*(7-x)+y)*2)
            ID4+=board[x][y]<<((8*(7-y)+x)*2)
    return min(min(ID1,ID2),min(ID3,ID4))

#where we need to work on.
def getComputer1Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)

    random.shuffle(possibleMoves)
    return possibleMoves[0]


def getComputer2Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for move in possibleMoves:
        if(isOnCorner(move[0],move[1])):
            return move
    return possibleMoves[0]


def getComputer3Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for move in possibleMoves:
        if(isOnCorner(move[0],move[1])):
            return move
    for move in possibleMoves:
        if(isOnGoodSide(move[0],move[1])):
            return move
    return possibleMoves[0]


def getComputer5Move(board, myTile):
    myMoves = getValidMoves(board, myTile)
    random.shuffle(myMoves)
    for move in myMoves:
        if(isOnCorner(move[0],move[1])):
            return move
    for move in myMoves:
        if(isOnGoodSide(move[0],move[1])):
            return move
    opTile=opponentTile(myTile)
    A=[]
    for move in myMoves:
        nboard = getBoardCopy(board)
        if makeMove(nboard, myTile, move[0], move[1]) == False:
            print 'bad program'
            break
        score = getScoreOfBoard(nboard)
        A.append((score[opTile]-score[myTile],move))
    A.sort()
    return A[0][1]

def flip(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = opponentTile(board[x][y])
    return 1

mp={}
    
def dfs_4_(board):
    BID = getBoardId(board)
    if BID in mp:
        return mp[BID]
    myMoves = getValidMoves(board, _BLACK_)
    opMoves = getValidMoves(board, _WHITE_)
    if len(myMoves) + len(opMoves) == 0:
        score = getScoreOfBoard(board)
        mp[BID]=(score[_BLACK_]-score[_WHITE_],(0,0))
        return mp[BID]
    if len(myMoves) == 0:
        nboard = getBoardCopy(board)
        flip(nboard)
        mp[BID]=(-dfs_4_(nboard)[0],(0,0))
        return mp[BID]
    tans=(65,(0,0))
    for move in myMoves:
        nboard = getBoardCopy(board)
        if makeMove(nboard, _BLACK_, move[0], move[1]) == False:
            print 'bad program'
            break
        flip(nboard)
        res = dfs_4_(nboard)
        if res[0] < tans[0]:
            tans =(res[0],move)
    mp[BID]=(-tans[0],tans[1])
    return mp[BID]

def dfs_4(board,myTile):
    nboard = getBoardCopy(board)
    if myTile == _WHITE_:
        flip(nboard)
    return dfs_4_(nboard)

def getComputer4Move(board, myTile):
    cnt = 0
    for x in range(8):
        for y in range(8):
            cnt = cnt + ( board[x][y] == _NONE_ )
    if cnt<=8:
        res = dfs_4(board,myTile)
        ##
        #if res[0] > 0:
        #    print 'I am ' + myTile + ', I will win.'
        #else:
        #    print 'I am ' + myTile + ', I will lose.'
        ##
        return res[1]
    if cnt<=12:
        getComputer5Move(board, myTile)
    return getComputer3Move(board, myTile)

def getComputerbadMove(board, computerTile):
    return 123, 456


pygame.init()
mainClock = pygame.time.Clock()

boardImage = pygame.image.load('board.png')
boardRect = boardImage.get_rect()
blackImage = pygame.image.load('black.png')
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load('white.png')
whiteRect = whiteImage.get_rect()

basicFont = pygame.font.SysFont(None, 48)

windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
pygame.display.set_caption('Othello')

mainBoard = getNewBoard()
resetBoard(mainBoard)
turn = 0
gameOver = False
#'H'    = human
#'C1'   = random
#'C2'   = corner first
#'C3'   = corner first side second
#'C4'   = MIX of C3 and C5 + end game diff maximized
#'C5'   = corner first side second big diff third(one level)
#'test' = invalid move
PLAYEROPT = ['C3','C4']
PLAYERWINS = [0,0]
HumanMoveIsGet = False
ShowFlag = True


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if gameOver == True:
                resetBoard(mainBoard)
                gameOver = False
                turn = 0
            elif gameOver == False and PLAYEROPT[turn] == 'H':
                x, y = pygame.mouse.get_pos()
                col = int((x-BOARDX)/CELLWIDTH)
                row = int((y-BOARDY)/CELLHEIGHT)
                HumanMoveIsGet = True
    if ( gameOver == False ):
        if(PLAYEROPT[turn] == 'C1'):
            x, y = getComputer1Move(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'C2'):
            x, y = getComputer2Move(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'C3'):
            x, y = getComputer3Move(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'C4'):
            x, y = getComputer4Move(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'C5'):
            x, y = getComputer5Move(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'test'):
            x, y = getComputerbadMove(mainBoard, turn)
        elif(PLAYEROPT[turn] == 'H' and HumanMoveIsGet == True):
            x, y = col, row
        else:
            x, y = 514, 514
        #print x, y ,turn
        if(makeMove(mainBoard, turn, x, y) == True):
            if getValidMoves(mainBoard, turn^1) != []:
                turn = turn^1
        elif(PLAYEROPT[turn] != 'H'):
            print 'bad AI ' + PLAYEROPT[turn] + ' made a invalid move!'
            gameOver = True
        else:
            HumanMoveIsGet = False
    if( ShowFlag == False ):
        if gameOver == True or isGameOver(mainBoard):
            gameOver == True
            res = getScoreOfBoard(mainBoard)
            PLAYERWINS[res[_BLACK_]<res[_WHITE_]]+=1
            #print PLAYEROPT[res[_BLACK_]<res[_WHITE_]] , 'win.'
            print PLAYERWINS[0], PLAYERWINS[1]
            resetBoard(mainBoard)
            gameOver == False
        continue
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)
    
    for x in range(8):
        for y in range(8):
            rectDst = pygame.Rect(BOARDX+x*CELLWIDTH+2, BOARDY+y*CELLHEIGHT+2, PIECEWIDTH, PIECEHEIGHT)
            if mainBoard[x][y] == _BLACK_:
                windowSurface.blit(blackImage, rectDst, blackRect)
            elif mainBoard[x][y] == _WHITE_:
                windowSurface.blit(whiteImage, rectDst, whiteRect)

    if gameOver == True or isGameOver(mainBoard):
        score01, score02 = getScoreOfBoard(mainBoard)
        outputStr = 'Game Over Score ' + str(score01) + ":" + str(score02)
        text = basicFont.render(outputStr, True, BLACK, BLUE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        gameOver = True
    
    pygame.display.update()
    mainClock.tick(FPS)

