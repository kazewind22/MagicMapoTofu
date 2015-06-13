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

class Kart:
    V = array('i',[
        +20, -3,+11, +8, +8,+11, -3,+20,
         -3, -7, -4, +1, +1, -4, -7, -3,
        +11, -4, +2, +2, +2, +2, -4,+11,
         +8, +1, +2, -3, -3, +2, +1, +8,
         +8, +1, +2, -3, -3, +2, +1, +8,
        +11, -4, +2, -3, -3, +2, -4,+11,
         -3, -7, -4, +1, +1, -4, -7, -3,
        +20, -3,+11, +8, +8,+11, -3,+20])
    def getGrade(self, board, myTile):
        opTile=myTile^1
        d = 0
        my_tiles = 0
        op_tiles = 0
        my_front_tiles = 0
        op_front_tiles = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == myTile:
                    d += self.V[(x<<3)+y]
                    my_tiles += 1
                    if isFrontier(board, x, y):
                        my_front_tiles += 1
                elif board[x][y] == opTile:
                    d -= self.V[(x<<3)+y]
                    op_tiles -= 1
                    if isFrontier(board, x, y):
                        op_front_tiles += 1
        p = 0
        if (my_tiles + op_tiles) != 0:
            if my_tiles > op_tiles:
                p = 100. * my_tiles / ( my_tiles + op_tiles)
            elif my_tiles < op_tiles:
                p = -100. * op_tiles / ( my_tiles + op_tiles)

        f = 0
        if (my_front_tiles + op_front_tiles) != 0:
            if my_front_tiles > op_front_tiles:
                f = -100. * my_front_tiles / (my_front_tiles + op_front_tiles)
            elif my_front_tiles < op_front_tiles:
                f = 100. * op_front_tiles / (my_front_tiles + op_front_tiles)

        c = 0
        l = 0
        for x,y in [(0,0),(0,7),(7,0),(7,7)]:
            c += 25 * ((board[x][y]==myTile)-(board[x][y]==opTile))
            if board[x][y]==2:
                for dx,dy in [(0,1),(1,0),(1,1)]:
                    l += -12.5 * ((board[x^dx][y^dy]==myTile) - (board[x^dx][y^dy]==opTile))

        Moves = getBothValidMoves(board)
        my_mob = len(Moves[myTile])
        op_mob = len(Moves[opTile])
        m = 0
        if (my_mob + op_mob) != 0:
            if my_mob > op_mob:
                m = 100. * my_mob / (my_mob + op_mob)
            elif my_mob < op_mob:
                m = -100. * op_mob / (my_mob + op_mob)

        score = 10*p + 801.724*c + 382.026*l + 78.922*m + 74.396*f + 10*d
        return score

class Dalu:
    f =  array('i',[
        +20, -3,+11, +8, +8,+11, -3,+20,
         -3, -7, -4, +1, +1, -4, -7, -3,
        +11, -4, +2, +2, +2, +2, -4,+11,
         +8, +1, +2, -3, -3, +2, +1, +8,
         +8, +1, +2, -3, -3, +2, +1, +8,
        +11, -4, +2, -3, -3, +2, -4,+11,
         -3, -7, -4, +1, +1, -4, -7, -3,
        +20, -3,+11, +8, +8,+11, -3,+20])
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
