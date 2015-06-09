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
        restnone = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
            restnone+= (board[xy>>3][xy&7]==NONE) << xy
        if cnt<=10:
            nboard = getBoardCopy(board)
            return self.dfs(nboard, Tile, restnone)[1]
        if cnt<=12:
            solver = MinMaxOneAI() 
        else:
            solver = CornerSideAI()
        return solver.getMove(board, Tile)

    def dfs(self, board, myTile, restnone):
        opTile = myTile^1
        myMoves, opMoveslen = getBothValidMoves_2(board, myTile, restnone)
        if opMoveslen ==0 and len(myMoves) == 0:
            score = getScoreOfBoard(board)
            return (score[myTile]-score[opTile],(0,0))
        elif len(myMoves) == 0:
            return (-self.dfs(board, opTile, restnone)[0],(0,0))
        tans=(1<<30,(0,0))
        for move in myMoves:
            tilesToFlip = getTileToFlip(board, myTile, move[0], move[1])
            ###################################
            mid = move[0]*8+move[1]
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone-= 1<<mid
            ###################################
            res = self.dfs(board, opTile, restnone)
            ###################################
            board[move[0]][move[1]] = NONE
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone+= 1<<mid
            ###################################
            if res[0] < tans[0]:
                tans = (res[0], move)
                #find win cut
                if tans[0] < 0 :
                    break
        return (-tans[0],tans[1])
class Dudu:
    def getGrade(self, board, myTile):
        opTile=myTile^1
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
                score+= ((board[x][y]==myTile)-(board[x][y]==opTile))<<2
                score+= ((board[y][x]==myTile)-(board[y][x]==opTile))<<2
        return score
class MuChu:
    def getGrade(self, board, myTile):
        opTile=myTile^1
        tmp = getScoreOfBoard(board)
        score = tmp[myTile]-tmp[opTile]
        for x,y in [(0,0),(0,7),(7,0),(7,7)]:
            score+= ((board[x][y]==myTile)-(board[x][y]==opTile))<<10
            score-= (board[x][y]==2 and board[x^1][y^1]==myTile)<<5
            for dx,dy in [(0,1),(1,0),(1,1)]:
                score+= (board[x][y]==myTile and board[x^dx][y^dy]==myTile)<<2
        for x in [0,7]:
            for y in [2,3,4,5]:
                score+= ((board[x][y]==myTile)-(board[x][y]==opTile))<<2
                score+= ((board[y][x]==myTile)-(board[y][x]==opTile))<<2
        return score
class LiyianAI:
    def __init__(self):
        self.grader=Dudu()
    def setgrader(self, grader_):
        self.grader=grader_
    #global span_cnt
    def getMove(self, board, myTile):
        cnt = 0
        restnone = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
            restnone+= ( board[xy>>3][xy&7] == NONE ) << xy
        nboard = getBoardCopy(board)
        if cnt<=10:
            solver = EndAllWithMinMaxAI()
            return solver.dfs(nboard, myTile, restnone)[1]
        solver = CornerSideAI()
        tmp = solver.getMove(board, myTile)
        if isOnCorner(tmp):
            return tmp
        if cnt<=64:
            global span_cnt
            span_cnt = 0
            res = self.dfs_6(nboard, myTile, restnone, 4, -(1<<30), 1<<30)
            #if span_cnt>=100:
            #    print 'span_cnt = ', span_cnt
            return res[1]
        return tmp
    def dfs_6(self, board, myTile, restnone, depth, alpha, beta):
        #global span_cnt
        #span_cnt+=1
        opTile = myTile^1
        myMoves, opMoveslen = getBothValidMoves_2(board, myTile, restnone)
        if (opMoveslen == 0 and len(myMoves) == 0) or depth == 0:
            score=self.grader.getGrade(board, myTile)
            return (score,0)
        elif len(myMoves) == 0:
            return (-self.dfs_6(board, opTile, restnone, depth-1, -beta, -alpha)[0],0)
        tans=(1<<30)
        tmov=(0,0)
        nalpha = alpha
        for move in myMoves:
            tilesToFlip = getTileToFlip(board, myTile, move[0], move[1])
            ###################################
            mid = move[0]*8+move[1]
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone-= 1 << mid
            ###################################
            res = self.dfs_6(board, opTile, restnone, depth-1, -beta, -nalpha)
            ###################################
            board[move[0]][move[1]] = NONE
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone+= 1 << mid
            ###################################
            if res[0] < tans:
                tans = res[0]
                tmov = []
                tmov.append(move)
            elif res[0] == tans:
                tmov.append(move)
            nalpha = max(nalpha, -res[0])
            if nalpha >= beta:
                break
        return (-tans,random.choice(tmov))
