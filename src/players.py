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

class MinMaxOne:
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
            solver = MinMaxOne() 
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

