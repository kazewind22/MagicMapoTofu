import time, sys, random
from constants import *
from operations import *
from players_noGUI import *

mainBoard = getNewBoard()
player1 = SetPlayer('sauce')
player1.player.setgrader(Yuehs())
player1.player.setsBound(10)
player1.player.setxLevel(2)

player2 = SetPlayer('sauce')
player2.player.setgrader(Dalu())
player2.player.setsBound(10)
player2.player.setxLevel(2)

players = [player1, player2]
playersTile = [BLACK, WHITE]
playersWins = [0, 0]
random.seed(7122)

while True:
    starttime = time.clock()
    playersTime = [0, 0]
    resetBoard(mainBoard)
    now = 0
    while isGameOver(mainBoard) == False:
        ts = time.clock()
        x, y = players[now].getMove(mainBoard, playersTile[now])
        playersTime[now]+= time.clock() - ts
        if makeMove(mainBoard, now, x, y) == False and players[now] != player0:
            print 'bad AI ' + playersTile[now] + ' made a invalid move!'
            gameOver = True
        
        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
    score = getScoreOfBoard(mainBoard)
    if score[0] != score[1]:
        playersWins[score[0]<score[1]]+=1
    print 'win count:  ', playersWins[0], playersWins[1]
    print 'spent time: ', playersTime[0], playersTime[1]
    print 'total time: ', time.clock()-starttime

raw_input("")
