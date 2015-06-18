import time, sys, random
from constants import *
from operations import *
from grader import *
from advisor import *

class SetPlayer:
    def __init__(self, Type):
        self.player = self.setSolver(Type)
        self.playerType = Type
    def setSolver(self, Type):
        return {
            'random':RandomAI(),
            'corner':CornerAI(),
            'cornerside':CornerSideAI(),
            'mix':EndAllWithMinMaxAI(),
            'sauce':LiyianAI(),
        }.get(Type, RandomAI())
    def getMove(self, board, Tile):
        return self.player.getMove(board, Tile)   

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
        cnt = [0,0,0]
        restnone = 0
        for xy in range(64):
            cnt[board[xy>>3][xy&7]]+= 1
            restnone+= (board[xy>>3][xy&7]==NONE) << xy
        if cnt[2]<=10:
            nboard = getBoardCopy(board)
            return self.dfs(nboard, Tile, restnone, cnt)[1]
        if cnt[2]<=12:
            solver = MinMaxOneAI() 
        else:
            solver = CornerSideAI()
        return solver.getMove(board, Tile)

    def dfs(self, board, myTile, restnone, cnt):
        if cnt[NONE] == 0:
            return (cnt[myTile]-cnt[myTile^1],(0,0))
        opTile = myTile^1
        myMoves, opMoveslen = getBothValidMoves_2(board, myTile, restnone)
        if opMoveslen ==0 and len(myMoves) == 0:
            return (cnt[myTile]-cnt[opTile],(0,0))
        elif len(myMoves) == 0:
            return (-self.dfs(board, opTile, restnone, cnt)[0],(0,0))
        tans=(1<<30,(0,0))
        for move in myMoves:
            tilesToFlip = getTileToFlip(board, myTile, move[0], move[1])
            ###################################
            mid = move[0]*8+move[1]
            tfn = len(tilesToFlip)
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone-= 1<<mid
            cnt[ NONE ]-= 1
            cnt[opTile]-=tfn
            cnt[myTile]+=tfn+1
            ###################################
            res = self.dfs(board, opTile, restnone, cnt)
            ###################################
            board[move[0]][move[1]] = NONE
            for x ,y in tilesToFlip:
                board[x][y]^=1
            restnone+= 1<<mid
            cnt[ NONE ]+= 1
            cnt[opTile]+=tfn
            cnt[myTile]-=tfn+1
            ###################################
            if res[0] < tans[0]:
                tans = (res[0], move)
                #find win cut
                if tans[0] < 0 :
                    break
        return (-tans[0],tans[1])

class LiyianAI:
    def __init__(self):
        self.grader = Yuehs()
        self.fBound = 0
        self.advise = [Fisrt8AI(None),Fisrt8AI(None)]
        self.sBound = 10
        self.xLevel = 4
    def setgrader(self, grader_):
        self.grader = grader_
    def setfBound(self, fBound_):
        self.fBound = fBound_
    def setadvise(self, advise_, myTile):
        self.advise[myTile]=advise_
    def setsBound(self, sBound_):
        self.sBound = sBound_
    def setxLevel(self, xLevel_):
        self.xLevel = xLevel_
    def getMove(self, board, myTile):
        cnt = [0,0,0]
        restnone = 0
        for xy in range(64):
            cnt[board[xy>>3][xy&7]]+= 1
            restnone+= ( board[xy>>3][xy&7] == NONE ) << xy
        nboard = getBoardCopy(board)
        if 60-cnt[NONE]<=self.fBound and self.advise[myTile].isMove(nboard, myTile):
            return self.advise[myTile].getMove(nboard, myTile)
        elif cnt[NONE]<=self.sBound:
            return EndAllWithMinMaxAI().dfs(nboard, myTile, restnone, cnt)[1]
        res = self.dfs_6(nboard, myTile, restnone, self.xLevel, -(1<<30), 1<<30)
        return res[1]
    def dfs_6(self, board, myTile, restnone, depth, alpha, beta):
        if depth == 0:
            return (self.grader.getGrade(board, myTile),0)
        opTile = myTile^1
        myMoves, opMoveslen = getBothValidMoves_2(board, myTile, restnone)
        if opMoveslen == 0 and len(myMoves) == 0:
            return (self.grader.getGrade(board, myTile),0)
        elif len(myMoves) == 0:
            return (-self.dfs_6(board, opTile, restnone, depth-1, -beta, -alpha)[0],0)
        tans=(1<<30)
        tmov=[]
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
