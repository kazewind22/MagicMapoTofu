import pygame, sys, random
from pygame.locals import *
from constants import *
from operations import *

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

class RandomAI:
    def getMove(self, board, Tile):
        possibleMoves = getValidMoves(board, Tile)
        random.shuffle(possibleMoves)
        return possibleMoves[0]

class CornerAI:
    def getMove(self, board, Tile):
        possibleMoves = getValidMoves(board, Tile)
        random.shuffle(possibleMoves)
        for move in possibleMoves:
            if(isOnCorner(move)):
                return move
        return possibleMoves[0]

class CornerSideAI:
    def getMove(self, board, Tile):
        possibleMoves = getValidMoves(board, Tile)
        random.shuffle(possibleMoves)
        for move in possibleMoves:
            if(isOnCorner(move)):
                return move
        for move in possibleMoves:
            if(isOnGoodSide(move)):
                return move
        return possibleMoves[0]

class MinMaxOneAI:
    def getMove(self, board, Tile):
        myMoves = getValidMoves(board, Tile)
        random.shuffle(myMoves)
        for move in myMoves:
            if(isOnCorner(move)):
                return move
        for move in myMoves:
            if(isOnGoodSide(move)):
                return move
        opTile=opponentTile(Tile)
        A=[]
        for move in myMoves:
            nboard = getBoardCopy(board)
            if makeMove(nboard, Tile, move[0], move[1]) == False:
                print 'bad program'
                break
            score = getScoreOfBoard(nboard)
            A.append((score[opTile]-score[Tile],move))
        A.sort()
        return A[0][1]

class EndAllWithMinMaxAI:
    def getMove(self, board, Tile):
        cnt = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
        if cnt<=8:
            nboard = getBoardCopy(board)
            return self.dfs(nboard, Tile)[1]
        if cnt<=12:
            solver = MinMaxOneAI() 
        else:
            solver = CornerSideAI()
        return solver.getMove(board, Tile)

    def dfs(self, board, myTile):
        opTile = myTile^1
        if myTile == BLACK:
            myMoves, opMoves = getBothValidMoves(board)
        else:
            opMoves, myMoves = getBothValidMoves(board)
        if len(myMoves) + len(opMoves) == 0:
            score = getScoreOfBoard(board)
            return (score[myTile]-score[opTile],(0,0))
        elif len(myMoves) == 0:
            return (-self.dfs(board, opTile)[0],(0,0))
        tans=(66,(0,0))
        for move in myMoves:
            tilesToFlip = isValidMove(board, myTile, move[0], move[1])
            if tilesToFlip == False:
                print 'bad program'
                break
            ###################################
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            ###################################
            res = self.dfs(board, opTile)
            ###################################
            board[move[0]][move[1]] = NONE
            for x ,y in tilesToFlip:
                board[x][y]^=1
            ###################################
            if res[0] < tans[0]:
                tans = (res[0], move)
                #find win cut
                if tans[0] < 0 :
                    break
        return (-tans[0],tans[1])

class LiyianAI:
    def getMove(self, board, myTile):
        cnt = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
        nboard = getBoardCopy(board)
        if cnt<=8:
            solver = EndAllWithMinMaxAI()
            return solver.dfs(nboard, myTile)[1]
        solver = CornerSideAI()
        tmp = solver.getMove(board, myTile)
        if isOnCorner(tmp):
            return tmp
        if cnt<=64:
            restnone=array('i',[0,0,0,0])
            for k in range(4):
                for xy in range(16):
                    if board[k*2+(xy>>3)][xy&7]==NONE:
                        restnone[k]|= 1 << xy
            res = self.dfs_6(nboard, myTile, restnone, 2)
            return res[1]
        return tmp
    def dfs_6(self, board, myTile, restnone, depth):
        opTile = myTile^1
        if myTile == BLACK:
            myMoves, opMoves = getBothValidMoves_2(board, restnone)
        else:
            opMoves, myMoves = getBothValidMoves_2(board, restnone)
        if (len(myMoves) == 0 and len(opMoves) == 0) or depth == 0:
            tmp = getScoreOfBoard(board)
            score = tmp[myTile]-tmp[opTile]
            for x,y in [(0,0),(0,7),(7,0),(7,7)]:
                score+= ((board[x][y]==myTile)-(board[x][y]==opTile))<<10
                score-= (board[x][y]==2)*((board[x^0][y^1]==myTile) or (board[x^1][y^0]==myTile) or (board[x^1][y^1]==myTile))<<8
                score-= (board[x][y]==2 and board[x^1][y^1]==myTile)<<3
                for dx,dy in [(0,1),(1,0),(1,1)]:
                    score+= (board[x][y]==myTile and board[x^dx][y^dy]==myTile)<<2
            for x in [0,7]:
                for y in [2,3,4,5]:
                    score+= (board[x][y]!=2)*(1-2*(board[x][y]^myTile))<<2
                    score+= (board[y][x]!=2)*(1-2*(board[y][x]^myTile))<<2
            return (score,0)
        elif len(myMoves) == 0:
            return (-self.dfs_6(board, opTile, restnone, depth-1)[0],0)
        tans=[(1<<30,0),(1<<30,0)]
        for move in myMoves:
            tilesToFlip = isValidMove(board, myTile, move[0], move[1])
            if tilesToFlip == False:
                print 'bad program'
                break
            ###################################
            mid = move[0]*8+move[1]
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone[mid>>4]-= 1 << (mid&15)
            ###################################
            res = self.dfs_6(board, opTile, restnone, depth-1)
            ###################################
            board[move[0]][move[1]] = NONE
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone[mid>>4]+= 1 << (mid&15)
            ###################################
            if res[0] < tans[0][0]:
                tans[1] = tans[0]
                tans[0] = (res[0],move)
            elif res[0] < tans[1][0]:
                tans[1] = (res[0],move)
        if tans[1][0]>=tans[0][0]+8:
            r = 0
        else:
            r = random.randint(0, 1)
        return (-tans[r][0],tans[r][1])
