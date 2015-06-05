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
        x = xstart + xdirection
        y = ystart + ydirection
        if isOnBoard(x, y) == False or board[x][y] != otherTile:
            continue
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


def getBothValidMoves(board):
    AvalidMoves = []
    BvalidMoves = []
    for xy in range(64):
        if isValidMove(board, _BLACK_, xy>>3, xy&7) != False:
            AvalidMoves.append([xy>>3, xy&7])
        if isValidMove(board, _WHITE_, xy>>3, xy&7) != False:
            BvalidMoves.append([xy>>3, xy&7])
    return AvalidMoves, BvalidMoves


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
    for xy in range(64):
        ID1+=board[xy>>3][xy&7]<<((xy^ 0)*2)
        ID2+=board[xy>>3][xy&7]<<((xy^ 7)*2)
        ID3+=board[xy>>3][xy&7]<<((xy^56)*2)
        ID4+=board[xy>>3][xy&7]<<((xy^63)*2)
    return min(ID1,ID2,ID3,ID4)

#where we need to work on.
def getComputer1Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)

    random.shuffle(possibleMoves)
    return possibleMoves[0]


def getComputer2Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for move in possibleMoves:
        if(isOnCorner(move)):
            return move
    return possibleMoves[0]


def getComputer3Move(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for move in possibleMoves:
        if(isOnCorner(move)):
            return move
    for move in possibleMoves:
        if(isOnGoodSide(move)):
            return move
    return possibleMoves[0]


def getComputer5Move(board, myTile):
    myMoves = getValidMoves(board, myTile)
    random.shuffle(myMoves)
    for move in myMoves:
        if(isOnCorner(move)):
            return move
    for move in myMoves:
        if(isOnGoodSide(move)):
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

    
def dfs_4_(board):
    myMoves, opMoves = getBothValidMoves(board)
    if len(myMoves) + len(opMoves) == 0:
        score = getScoreOfBoard(board)
        ans = (score[_BLACK_]-score[_WHITE_],(0,0))
    elif len(myMoves) == 0:
        nboard = getBoardCopy(board)
        flip(nboard)
        ans = (-dfs_4_(nboard)[0],(0,0))
    else:
        tans=(66,(0,0))
        for move in myMoves:
            nboard = getBoardCopy(board)
            if makeMove(nboard, _BLACK_, move[0], move[1]) == False:
                print 'bad program'
                break
            flip(nboard)
            res = dfs_4_(nboard)
            if res[0] < tans[0]:
                tans = (res[0],move)
                #find win cut
                if tans[0] < 0 :
                    break
        ans = (-tans[0],tans[1])
    return ans

def dfs_4(board,myTile):
    nboard = getBoardCopy(board)
    if myTile == _WHITE_:
        flip(nboard)
    return dfs_4_(nboard)

def getComputer4Move(board, myTile):
    cnt = 0
    for xy in range(64):
        cnt+= ( board[xy>>3][xy&7] == _NONE_ )
    if cnt<=8:
        res = dfs_4(board,myTile)
        return res[1]
    if cnt<=12:
        getComputer5Move(board, myTile)
    return getComputer3Move(board, myTile)


def dfs_6(board, myTile, depth):
    if depth>=10:
        print 'dfs_6 too deep'
        return (-7122)
    opTile = myTile^1
    if myTile == _BLACK_:
        myMoves, opMoves = getBothValidMoves(board)
    else:
        opMoves, myMoves = getBothValidMoves(board)
    if len(myMoves) + len(opMoves) == 0 or depth == 0:
        tmp = getScoreOfBoard(board)
        score = tmp[myTile]-tmp[opTile]
        for x,y in [(0,0),(0,7),(7,0),(7,7)]:
            score+= (board[x][y]!=2)*(1-2*(board[x][y]^myTile))<<10
            score-= (board[x][y]==2)*((board[x^0][y^1]==myTile) or (board[x^1][y^0]==myTile) or (board[x^1][y^1]==myTile))<<8
        for x in [0,7]:
            for y in [2,3,4,5]:
                score+= (board[x][y]!=2)*(1-2*(board[x][y]^myTile))<<2
                score+= (board[y][x]!=2)*(1-2*(board[y][x]^myTile))<<2
        return (score,0)
    elif len(myMoves) == 0:
        return (-dfs_6(board, opTile, depth-1)[0],0)
    tans=[(1<<30,0),(1<<30,0)]
    for move in myMoves:
        tilesToFlip = isValidMove(board, myTile, move[0], move[1])
        if tilesToFlip == False:
            print 'bad program'
            break
        board[move[0]][move[1]] = myTile
        for x ,y in tilesToFlip:
            board[x][y]^=1
        res = dfs_6(board, opTile, depth-1)
        board[move[0]][move[1]] = _NONE_
        for x ,y in tilesToFlip:
            board[x][y]^=1
        if res[0] < tans[0][0]:
            tans[1] = tans[0]
            tans[0] = (res[0],move)
        elif res[0] < tans[1][0]:
            tans[1] = (res[0],move)
    if tans[1][0]>=tans[0][0]+1024:
        r = 0
    else:
        r = random.randint(0, 1)
    return (-tans[r][0],tans[r][1])


def getComputer6Move(board, myTile):
    cnt = 0
    for xy in range(64):
        cnt+= ( board[xy>>3][xy&7] == _NONE_ )
    if cnt<=8:
        res = dfs_4(board,myTile)
        return res[1]
    tmp = getComputer3Move(board, myTile)
    if isOnCorner(tmp):
        return tmp
    if cnt<=64:
        nboard = getBoardCopy(board)
        res = dfs_6(nboard,myTile, 2)
        return res[1]
    return tmp


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
HumanMoveIsGet = False
ShowFlag = True
#'H'    = human
#'C1'   = random
#'C2'   = corner first
#'C3'   = corner first side second
#'C4'   = MIX of C3 and C5 + end game diff maximized
#'C5'   = corner first side second big diff third(one level)
PLAYEROPT = ['H','C6']
PLAYERWINS = [0,0]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if gameOver == True:
                resetBoard(mainBoard)
                turn = 0
                gameOver = False
                HumanMoveIsGet = False
                break
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
        elif(PLAYEROPT[turn] == 'C6'):
            x, y = getComputer6Move(mainBoard, turn)
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
            if res[_BLACK_]<res[_WHITE_]:
                PLAYERWINS[1]+=1
            if res[_BLACK_]>res[_WHITE_]:
                PLAYERWINS[0]+=1
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


