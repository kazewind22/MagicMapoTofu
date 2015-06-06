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
            if Tile == WHITE:
                flip(nboard)
            return self.dfs(nboard)[1]
        if cnt<=12:
            solver = MinMaxOneAI() 
        else:
            solver = CornerSideAI()
        return solver.getMove(board, Tile)

    def dfs(self, board):
        myMoves, opMoves = getBothValidMoves(board)
        if len(myMoves) + len(opMoves) == 0:
            score = getScoreOfBoard(board)
            ans = (score[BLACK]-score[WHITE],(0,0))
        elif len(myMoves) == 0:
            nboard = getBoardCopy(board)
            flip(nboard)
            ans = (-self.dfs(nboard)[0],(0,0))
        else:
            tans=(66,(0,0))
            for move in myMoves:
                nboard = getBoardCopy(board)
                if makeMove(nboard, BLACK, move[0], move[1]) == False:
                    print 'bad program'
                    break
                flip(nboard)
                res = self.dfs(nboard)
                if res[0] < tans[0]:
                    tans = (res[0], move)
                    #find win cut
                    if tans[0] < 0 :
                        break
            ans = (-tans[0],tans[1])
        return ans

class LiyianAI:
    def getMove(self, board, myTile):
        cnt = 0
        for xy in range(64):
            cnt+= ( board[xy>>3][xy&7] == NONE )
        if cnt<=8:
            solver = EndAllWithMinMaxAI()
            nboard = getBoardCopy(board)
            if myTile == WHITE:
                flip(nboard)
            return solver.dfs(nboard)[1]
        solver = CornerSideAI()
        tmp = solver.getMove(board, myTile)
        if isOnCorner(tmp):
            return tmp
        if cnt<=64:
            nboard = getBoardCopy(board)
            res = self.dfs_6(nboard,myTile, 2)
            return res[1]
        return tmp
    def dfs_6(self, board, myTile, depth):
        if depth>=10:
            print 'dfs_6 too deep'
            return (-7122)
        opTile = myTile^1
        if myTile == BLACK:
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
            return (-self.dfs_6(board, opTile, depth-1)[0],0)
        tans=[(1<<30,0),(1<<30,0)]
        for move in myMoves:
            tilesToFlip = isValidMove(board, myTile, move[0], move[1])
            if tilesToFlip == False:
                print 'bad program'
                break
            board[move[0]][move[1]] = myTile
            for x ,y in tilesToFlip:
                board[x][y]^=1
            res = self.dfs_6(board, opTile, depth-1)
            board[move[0]][move[1]] = NONE
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
