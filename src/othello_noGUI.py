import time, sys, random
from constants import *
from operations import *
from players_noGUI import *

mainBoard = getNewBoard()
player1 = SetPlayer('sauce')
player1.player.setgrader(Yuehs())
player1.player.setfBound(0)
player1.player.setsBound(13)
player1.player.setxLevel(2)

player2 = SetPlayer('sauce')
player2.player.setgrader(Yuehs())
player2.player.setfBound(8)
player2.player.setsBound(13)
player2.player.setxLevel(2)

players = [player1, player2]
playersTile = [BLACK, WHITE]
playersWins = [0, 0]
#random.seed(7122)

ALLstarttime = time.clock()
f1=open('./count_win.txt', 'a')
round = 10000
while round!=0:
    round-=1
    starttime = time.clock()
    playersTime = [0, 0]
    resetBoard(mainBoard)
    now = 0
    ALLBoardID = [getBoardID(mainBoard)]
    moveCN = 0
    while isGameOver(mainBoard) == False:
        ts = time.clock()
        x, y = players[now].getMove(mainBoard, playersTile[now])
        playersTime[now]+= time.clock() - ts
        if makeMove(mainBoard, now, x, y) == False and players[now] != player0:
            print 'bad AI ' + playersTile[now] + ' made a invalid move!'
            gameOver = True
        if moveCN < 9:
            ALLBoardID.append(getBoardID(mainBoard))
            moveCN+= 1
        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
    score = getScoreOfBoard(mainBoard)
    if score[0] != score[1]:
        playersWins[score[0]<score[1]]+=1
    flag=7122
    if score[0]<score[1]:
        flag = 1
    elif score[0]>score[1]:
        flag = -1
    else:
        flag = 0
    if moveCN == 9:
        s = ''
        for cb in ALLBoardID:
            s+=str(cb[0])+' '
            s+=str(cb[1])+' '
            s+=str(cb[2])+' '
        s+=str(flag)+' '+str(1)
        print >>f1, s
    if round == 9999:
        print 'win count:  ', playersWins[0], playersWins[1]
        print 'spent time: ', playersTime[0], playersTime[1]
        print 'total time: ', time.clock()-starttime
print 'ALLtotal time: ', time.clock() - ALLstarttime
