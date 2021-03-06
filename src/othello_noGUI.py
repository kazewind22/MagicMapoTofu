import time, sys, random
from constants import *
from operations import *
from players_noGUI import *

mainBoard = getNewBoard()

player = []
def addP(AI, grader, f, ab, aw, s, x):
    tp = SetPlayer(AI)
    tp.player.setgrader(grader)
    tp.player.setfBound(f)
    tp.player.setadvise(ab,BLACK)
    tp.player.setadvise(aw,WHITE)
    tp.player.setsBound(s)
    tp.player.setxLevel(x)
    player.append(tp)
    return len(player)-1

advisor0 = Fisrt8AI(None)
advisor1 = Fisrt8AI('./count_win.txt')
advisor2 = Fisrt8AI('./count_win_Yuehs_271_BLACK.txt')
advisor3 = Fisrt8AI('./count_win_Yuehs_271_WHITE.txt')
advisor4 = Fisrt6AI('./cw6_271_BLACK.txt')
advisor5 = Fisrt6AI('./cw6_271_WHITE.txt')
advisor6 = Fisrt8AI('./count_win_anti_271_BLACK.txt')
advisor7 = Fisrt8AI('./count_win_anti_271_WHITE.txt')

player.append(0)#0
addP('sauce',Dalu()     ,8,advisor1,advisor1,13,2)#1
addP('sauce',Yuehs()    ,8,advisor1,advisor1,13,2)#2
addP('sauce',Yuehs_2()  ,8,advisor1,advisor1,13,2)#3
addP('sauce',Yuehs_27() ,8,advisor1,advisor1,13,2)#4
addP('sauce',Yuehs_271(),8,advisor2,advisor3,13,2)#5 regular
addP('sauce',Kart()     ,8,advisor1,advisor1,13,2)#6
addP('sauce',Kart_2()   ,8,advisor1,advisor1,13,2)#7
addP('sauce',Yuehs_271(),8,advisor1,advisor1,13,2)#8 anti
addP('sauce',Kart()     ,8,advisor6,advisor7,13,2)#9
addP('sauce',Kart_2()   ,8,advisor6,advisor7,13,2)#10
addP('sauce',Yuehs_271(),0,advisor0,advisor0,13,2)#11 no advisor
addP('sauce',Kart()     ,0,advisor0,advisor0,13,2)#12
addP('sauce',Kart_2()   ,0,advisor0,advisor0,13,2)#13
addP('sauce',Yuehs_271(),8,advisor2,advisor3,13,4)#14 deeper xLevel
addP('sauce',Kart()     ,8,advisor1,advisor1,13,4)#15
addP('sauce',Kart_2()   ,8,advisor1,advisor1,13,4)#16
addP('sauce',Yuehs_271(),8,advisor2,advisor3,-0,2)#17 no Endgame
addP('sauce',Kart()     ,8,advisor1,advisor1,-0,2)#18
addP('sauce',Kart_2()   ,8,advisor1,advisor1,-0,2)#19

players = [player[4], player[7]]
if len(sys.argv)>=3:
    p1 = int(sys.argv[1])
    p2 = int(sys.argv[2])
    players[0]=player[p1]
    players[1]=player[p2]
else:
    print 'usage othello_noGUI.py <player1> <player2>'
    exit(0)
playersTile = [BLACK, WHITE]
pOneIsWhite = 0
playersWins = [0, 0]
#random.seed(7122)

ALLstarttime = time.clock()
showWins = 1
swapPlayers = 1
maxR = 100

collectData_8_0 = 0
collectData_8_1 = 0
collectData_6 = 0
for i in range(3,len(sys.argv)):
    if sys.argv[i]=='-c6':
        collectData_6 = 1
    if sys.argv[i]=='-c80':
        collectData_8_0 = 1
    if sys.argv[i]=='-c81':
        collectData_8_1 = 1
    if sys.argv[i]=='-nsw':
        showWins = 0
    if sys.argv[i][0:3]=='-m=' and sys.argv[i][3:].isdigit():
        maxR = int(sys.argv[i][3:])

collectData_8 = collectData_8_0 or collectData_8_1
if collectData_6 and collectData_8:
    print 'cannot collect at the same time'
    exit(0)
ff=[0,0,0,0]
if collectData_8_0 == True:
    if p1 == 5 or p1 == 8:
        ff[0]=open('./count_win_Yuehs_271_BLACK.txt', 'a')
        ff[1]=open('./count_win_Yuehs_271_WHITE.txt', 'a')
    else:
        ff[0]=open('./count_win_anti_271_BLACK.txt', 'a')
        ff[1]=open('./count_win_anti_271_WHITE.txt', 'a')
if collectData_8_1 == True:
    if p2 == 5 or p2 == 8:
        ff[2]=open('./count_win_Yuehs_271_BLACK.txt', 'a')
        ff[3]=open('./count_win_Yuehs_271_WHITE.txt', 'a')
    else:
        ff[2]=open('./count_win_anti_271_BLACK.txt', 'a')
        ff[3]=open('./count_win_anti_271_WHITE.txt', 'a')
if collectData_6 == True:
    ff[2]=open('./cw6_271_BLACK.txt', 'a')
    ff[3]=open('./cw6_271_WHITE.txt', 'a')
round = 0
print 'start fight'
while round < maxR:
    starttime = time.clock()
    playersTime = [0, 0]
    resetBoard(mainBoard)
    now = 0
    ALLBoardID_8 = [getBoardID(mainBoard)]
    ALLBoardID_6 = [getBoardID_6(mainBoard, now)]
    moveCN = 0
    while isGameOver(mainBoard) == False:
        ts = time.clock()
        x, y = players[now].getMove(mainBoard, playersTile[now])
        playersTime[now^pOneIsWhite]+= time.clock() - ts
        if makeMove(mainBoard, now, x, y) == False:
            print 'bad AI ' + playersTile[now] + ' made a invalid move!'
            break
        if getValidMoves(mainBoard, playersTile[now^1]) != []:
            now = now^1
        if collectData_8 or collectData_6:
            ALLBoardID_8.append(getBoardID(mainBoard))
            ALLBoardID_6.append(getBoardID_6(mainBoard, now))
        moveCN+= 1
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
    if collectData_8 == True and moveCN >= 9:
        s = ''
        for i in range(10):
            s+=str(ALLBoardID_8[i][0])+' '
            s+=str(ALLBoardID_8[i][1])+' '
            s+=str(ALLBoardID_8[i][2])+' '
        s+= str(flag)+' '+str(1)
        if collectData_8_0:
            if pOneIsWhite:
                print >>ff[1], s
            else:
                print >>ff[0], s
        if collectData_8_1:
            if pOneIsWhite:
                print >>ff[3], s
            else:
                print >>ff[2], s
    if collectData_6 == True and moveCN >= 7:
        cb = ALLBoardID_6[7]
        s = str(cb[0])+' '+str(cb[1])+' '+str(cb[2])+' '+str(flag)+' '+str(1)
        if pOneIsWhite:
            print >>ff[3], s
        else:
            print >>ff[2], s
    if showWins == True or round < 3 or round == maxR - 1:
        print 'win count:  ', playersWins[0], playersWins[1]
        print 'spent time: ', playersTime[pOneIsWhite], playersTime[1^pOneIsWhite]
        print 'total time: ', time.clock()-starttime
    round+= 1
    if swapPlayers == True:
        players[0], players[1] = players[1], players[0]
        pOneIsWhite^= 1
print 'ALLtotal time: ', time.clock() - ALLstarttime
