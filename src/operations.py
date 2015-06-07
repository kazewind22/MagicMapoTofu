from constants import *
from array import array

def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = NONE

    board[3][3] = BLACK
    board[3][4] = WHITE
    board[4][3] = WHITE
    board[4][4] = BLACK

def getNewBoard():
    board = []
    for i in range(8):
        board.append(array('i',[NONE] * 8))
    return board

def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != NONE:
        return False

    board[xstart][ystart] = tile

    if tile == BLACK:
        otherTile = WHITE
    else:
        otherTile = BLACK

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

    board[xstart][ystart] = NONE # restore the empty space

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
            if board[x][y] == BLACK:
                xscore += 1
            if board[x][y] == WHITE:
                oscore += 1
    return {BLACK:xscore, WHITE:oscore}

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard

def isGameOver(board):
    return len(getValidMoves(board, WHITE))+len(getValidMoves(board, BLACK))==0
    return True
    for x in range(8):
        for y in range(8):
            if board[x][y] == NONE:
                return False
    return True

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBothValidMoves(board):
    BMoves = []
    WMoves = []
    for xy in range(64):
        if isValidMove(board, BLACK, xy>>3, xy&7) != False:
            BMoves.append([xy>>3, xy&7])
        if isValidMove(board, WHITE, xy>>3, xy&7) != False:
            WMoves.append([xy>>3, xy&7])
    return BMoves, WMoves

gBVM_lg = array('i',[0]*(1<<16))
for i in range(16):
    gBVM_lg[1<<i] = i
def getBothValidMoves_2(board, restnone):
    global gBVM_2_lg
    BMoves = []
    WMoves = []
    for k in range(4):
        mask = restnone[k]
        while mask!=0:
            lowbit = mask - ( mask&(mask-1) )
            xy = gBVM_lg[lowbit]
            x, y = k*2 + (xy>>3), xy&7
            mask-= lowbit
            if isValidMove(board, BLACK, x, y) != False:
                BMoves.append([x, y])
            if isValidMove(board, WHITE, x, y) != False:
                WMoves.append([x, y])
    return BMoves, WMoves

def isOnCorner(xy):
    x=xy[0]
    y=xy[1]
    return (x == 0 or x == 7) and (y == 0 or y == 7)

def isOnGoodSide(xy):
    x=xy[0]
    y=xy[1]
    if(x == 0 or x == 7):
        return y != 1 and y != 6
    if(y == 0 or y == 7):
        return x != 1 and x != 6
    return False

def opponentTile(myTile):
    if myTile >= 2:
        return NONE
    return myTile^1
