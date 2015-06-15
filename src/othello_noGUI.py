import time, sys, random
from constants import *
from operations import *
from players_noGUI import *

mainBoard = getNewBoard()

player1 = SetPlayer('sauce')
player1.player.setgrader(Yuehs_271())
player1.player.setfBound(8)
player1.player.setfFiles('./count_win_Yuehs_271_BLACK.txt',BLACK)
player1.player.setfFiles('./count_win_Yuehs_271_WHITE.txt',WHITE)
player1.player.setsBound(13)
player1.player.setxLevel(2)

player2 = SetPlayer('sauce')
player2.player.setgrader(Kart())
player2.player.setfBound(8)
#player2.player.setfFiles('./count_win_Yuehs_271_BLACK.txt',BLACK)
#player2.player.setfFiles('./count_win_Yuehs_271_WHITE.txt',WHITE)
player2.player.setfFiles('./count_win_6.txt',BLACK)
player2.player.setfFiles('./count_win_6.txt',WHITE)
player2.player.setsBound(13)
player2.player.setxLevel(2)

players = [player1, player2]
playersTile = [BLACK, WHITE]
pOneIsWhite = 0
playersWins = [0, 0]
#random.seed(7122)

ALLstarttime = time.clock()
collectData = 1
showWins = 0
swapPlayers = 1
if collectData == True:
    ff=[0,0]
    ff[0]=open('./count_win_Yuehs_271_BLACK.txt', 'a')
    ff[1]=open('./count_win_Yuehs_271_WHITE.txt', 'a')
maxR = 10000
round = 0
while round < maxR:
    starttime = time.clock()
    playersTime = [0, 0]
    resetBoard(mainBoard)
    now = 0
    ALLBoardID = [getBoardID(mainBoard)]
    moveCN = 0
    while isGameOver(mainBoard) == False:
        ts = time.clock()
        x, y = players[now].getMove(mainBoard, playersTile[now])
        playersTime[now^pOneIsWhite]+= time.clock() - ts
        if makeMove(mainBoard, now, x, y) == False:
            print 'bad AI ' + playersTile[now] + ' made a invalid move!'
            break
        if moveCN < 9:
            ALLBoardID.append(getBoardID(mainBoard))
            moveCN+= 1
        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
    score = getScoreOfBoard(mainBoard)
    if score[0] != score[1]:
        playersWins[(score[0]<score[1])^pOneIsWhite]+=1
    flag=7122
    if score[0]<score[1]:
        flag = 1
    elif score[0]>score[1]:
        flag = -1
    else:
        flag = 0
    if collectData == True and moveCN == 9:
        s = ''
        for cb in ALLBoardID:
            s+=str(cb[0])+' '
            s+=str(cb[1])+' '
            s+=str(cb[2])+' '
        s+=str(flag)+' '+str(1)
        if pOneIsWhite:
            print >>ff[1], s
        else:
            print >>ff[0], s
    if showWins == True or round < 5 :
        print 'win count:  ', playersWins[0], playersWins[1]
        print 'spent time: ', playersTime[pOneIsWhite], playersTime[1^pOneIsWhite]
        print 'total time: ', time.clock()-starttime
    round+= 1
    if swapPlayers == True:
        players[0], players[1] = players[1], players[0]
        pOneIsWhite^= 1
print 'ALLtotal time: ', time.clock() - ALLstarttime
