import sys, random
from constants import *
from operations import *

class Yuehs:
    def getGrade(self, board, myTile):
        opTile=myTile^1
        sum = [0, 0, 0]
        for x in range(8):
            for y in range(8):
                sum[board[x][y]]+=1
        score = sum[myTile]-sum[opTile]
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
class Yuehs_2:
    def getGrade(self, board, myTile):
        opTile=myTile^1
        score = Yuehs().getGrade(board, myTile)
        Moves = getBothValidMoves(board)
        score+= len(Moves[myTile])-len(Moves[opTile])
        return score
class Yuehs_27:
    def getGrade(self, board, myTile):
        opTile=myTile^1
        score = Yuehs().getGrade(board, myTile)
        Moves = getBothValidMoves(board)
        mobil = len(Moves[myTile])-len(Moves[opTile])
        for x, y in Moves[myTile]:
            mobil-= isOnCorner([x^0 ,y^1]) or isOnCorner([x^1 ,y^0]) or isOnCorner([x^1 ,y^1])
        score+= mobil<<2
        return score
class Dalu:
    f =  array('i',[
        +90,-60,+10,+10,+10,+10,-60,+90,
        -60,-80,+05,+05,+05,+05,-80,-60,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        +10,+05,+01,+01,+01,+01,+05,+10,
        -60,-80,+05,+05,+05,+05,-80,-60,
        +90,-60,+10,+10,+10,+10,-60,+90])
    def getGrade(self, board, myTile):
        opTile=myTile^1
        score = 0
        for x in range(8):
            for y in range(8):
                score+= ((board[x][y]==myTile)-(board[x][y]==opTile))*self.f[(x<<3)+y]
        for x,y in [(0,0),(0,7),(7,0),(7,7)]:
            for dx,dy in [(0,1),(1,0),(1,1)]:
                score+= (board[x][y]==myTile and board[x^dx][y^dy]==myTile)*self.f[((x^dx)<<3)+(y^dy)]
        return score