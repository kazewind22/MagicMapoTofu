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

def isValidMoveBool(board, myTile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != NONE:
        return False
    opTile = myTile^1
    for dx, dy in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        x, y = xstart+dx, ystart+dy
        l = 0
        while isOnBoard(x, y) and board[x][y] == opTile:
            l = 1
            x += dx
            y += dy
        if l and isOnBoard(x, y) == True and board[x][y] == myTile:
            return True
    return False

def getTileToFlip(board, myTile, xstart, ystart):
    opTile = myTile^1
    tilesToFlip=[]
    for dx, dy in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        x, y = xstart+dx, ystart+dy
        l = 0
        while isOnBoard(x, y) and board[x][y] == opTile:
            l += 1
            x += dx
            y += dy
        if l==0 or isOnBoard(x, y) == False or board[x][y] != myTile:
            continue
        while l>0:
            l-=1
            x-=dx
            y-=dy
            tilesToFlip.append([x,y])
    return tilesToFlip

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def isFrontier(board, x, y):
    for dx, dy in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        _x = x + dx
        _y = y + dy
        if isOnBoard(_x, _y) and board[_x][_y] == NONE:
            return True
    return False

def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    score = [0,0,0]
    for x in range(8):
        for y in range(8):
            score[board[x][y]]+=1
    return (score[0],score[1])

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
    return len(getValidMoves(board, WHITE))==0 and len(getValidMoves(board, BLACK))==0

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBothValidMoves(board):
    Moves = [[],[]]
    for xy in range(64):
        if isValidMoveBool(board, BLACK, xy>>3, xy&7) != False:
            Moves[BLACK].append([xy>>3, xy&7])
        if isValidMoveBool(board, WHITE, xy>>3, xy&7) != False:
            Moves[WHITE].append([xy>>3, xy&7])
    return Moves

gBVM_lg = array('i',[0]*(1<<16))
for i in range(16):
    gBVM_lg[1<<i] = i
def getBothValidMoves_2(board, myTile, restnone):
    global gBVM_2_lg
    lowMoves = []
    midMoves = []
    vipMoves = []
    opMoveslen = 0
    for k in range(4):
        mask = ( ( restnone>>(k<<4) )&65535 )
        while mask!=0:
            lowbit = mask - ( mask&(mask-1) )
            xy = gBVM_lg[lowbit] + (k<<4)
            x, y = xy>>3, xy&7
            mask-= lowbit
            if isValidMoveBool(board, myTile, x, y) == True:
                if isOnCorner([x, y]):
                    vipMoves.append([x, y])
                elif isOnGoodSide([x, y]):
                    midMoves.append([x, y])
                else:
                    lowMoves.append([x, y])
            opMoveslen = opMoveslen or isValidMoveBool(board, myTile^1, x, y)
    vipMoves.extend(midMoves)
    vipMoves.extend(lowMoves)
    return vipMoves, opMoveslen

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

def getBoardID(board):
    ID = [0,0,0]
    for x in range(8):
        for y in range(8):
            ID[board[x][y]]+= 1<<((x<<3)+y)
    return (ID[0],ID[1],ID[2])

def Mobility(board, myTile):
    opTile=myTile^1
    f = array('i',[
        +90,-60,+10,+10,+10,+10,-60,+90,
        -60,-80,+05,+05,+05,+05,-80,-60,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        -60,-80,+05,+05,+05,+05,-80,-60,
        +90,-60,+10,+10,+10,+10,-60,+90])
    Moves = getValidMoves(board, myTile)
    score = 0
    for move in Moves:
        score += f[(move[0]<<3)+(move[1])]
        for fliptile in getTileToFlip(board, myTile, move[0], move[1]):
            if isFrontier(board, fliptile[0], fliptile[1]):
                score -= f[(fliptile[0]<<3)+(fliptile[1])]
    return score
