import sys, random
from constants import *
from operations import *
from grader import *

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
            'first8':Fisrt8AI()
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

class Fisrt8AI:
    def __init__(self):
        self.NID={}
        self.RID=[]
        self.EDG=[]
        self.DPA=[]
    def loadFile(self, file):
        f1=open(file, 'r')
        with f1:
            content = f1.readlines()
        f1.close()
        IDT = 0
        for s in content:
            ss = s.split()
            for i in range(10):
                ID = (int(ss[i*3+0]),int(ss[i*3+1]),int(ss[i*3+2]))
                if ID not in self.NID:
                    self.NID[ID] = IDT
                    self.RID.append(ID)
                    self.EDG.append({})
                    self.DPA.append((2.0,0))
                    IDT+= 1
                nID = self.NID[ID]
                if i!=0:
                    self.EDG[oID][nID] = 1
                oID = nID
            self.DPA[oID] = (float(ss[30]),[])
        for i in range(IDT):
            j = IDT-1-i
            if len(self.EDG[j]) == 0:
                continue
            tmp = 2.0
            tmv = []
            for k in self.EDG[j]:
                if tmp > self.DPA[k][0]:
                    tmp = self.DPA[k][0]
                    tmv = []
                    tmv.append(k)
                elif tmp == self.DPA[k][0]:
                    tmv.append(k)
            self.DPA[j]=(-tmp,tmv)
    def isMove(self, board, Tile):
        ID = getBoardID(board)
        return ID in self.NID and len(self.DPA[self.NID[ID]][1])>0
    def getMove(self, board, Tile):
        if self.isMove(board, Tile):
            #print 'get from fisrt8'
            ID = getBoardID(board)
            ID = self.RID[ random.choice(self.DPA[self.NID[ID]][1]) ]
            if Tile == BLACK:
                myMoves, opMoves = getBothValidMoves(board)
            else:
                opMoves, myMoves = getBothValidMoves(board)
            for move in myMoves:
                nboard = getBoardCopy(board)
                makeMove(nboard, Tile, move[0], move[1])
                if ID == getBoardID(nboard):
                    return move
            print 'fisrt8 getMove Error!'
            return (0, 0)
        else:
            return EndAllWithMinMaxAI().getMove(board, Tile)

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

class LiyianAI:
    def __init__(self):
        self.grader = Yuehs()
        self.fBound = 0
        self.sBound = 10
        self.xLevel = 4
        self.F8 = [Fisrt8AI(),Fisrt8AI()]
    def setgrader(self, grader_):
        self.grader = grader_
    def setfBound(self, fBound_):
        self.fBound = fBound_
    def setfFiles(self, fFiles_, myTile):
        self.F8[myTile].loadFile(fFiles_)
    def setsBound(self, sBound_):
        self.sBound = sBound_
    def setxLevel(self, xLevel_):
        self.xLevel = xLevel_
    def getMove(self, board, myTile):
        cnt = 0
        restnone = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
            restnone+= ( board[xy>>3][xy&7] == NONE ) << xy
        nboard = getBoardCopy(board)
        if 60-cnt<self.fBound and self.F8[myTile].isMove(nboard, myTile):
            return self.F8[myTile].getMove(nboard, myTile)
        if cnt<=self.sBound:
            solver = EndAllWithMinMaxAI()
            return solver.dfs(nboard, myTile, restnone)[1]
        res = self.dfs_6(nboard, myTile, restnone, self.xLevel, -(1<<30), 1<<30)
        return res[1]
    def dfs_6(self, board, myTile, restnone, depth, alpha, beta):
        opTile = myTile^1
        myMoves, opMoveslen = getBothValidMoves_2(board, myTile, restnone)
        if depth == 0 or (opMoveslen == 0 and len(myMoves) == 0):
            return (self.grader.getGrade(board, myTile),0)
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
