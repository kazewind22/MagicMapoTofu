import time, sys, random
from constants import *
from operations import *
class Fisrt8AI:
    def __init__(self, file):
        self.NID={}
        self.RID=[]
        self.EDG=[]
        self.DPA=[]
        if file!=None:
            self.loadFile(file)
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

class Fisrt6AI:
    ################################build_node
    #print 'F6 start build node'
    startloadtime = time.clock()
    f1=open('cw6_node.txt','r')
    with f1:
        content = f1.readlines()
    f1.close()
    NID = {}
    for s in content:
        ss = s.split()
        ID = (int(ss[1]),int(ss[2]),int(ss[3]))
        NID[ID] = int(ss[0])
    IDT = len(NID)
    RID = [0] * IDT
    for i in NID:
        RID[NID[i]] = i
    #print 'F6 end build node: ', time.clock()-startloadtime
    ################################build_edge
    #print 'F6 start build edge'
    startloadtime = time.clock()
    f1=open('cw6_edge.txt','r')
    with f1:
        content = f1.readlines()
    f1.close()
    EDG = []
    for i in range(IDT):
        EDG.append([])
    for s in content:
        ss = s.split()
        From = int(ss[0])
        for To in range(1,len(ss),1):
            EDG[From].append(int(ss[To]))
    #print 'F6 end build edge', time.clock()-startloadtime
    ################################
    def make_DP(self, j):
        if self.DPA[j][0]!=65536:
            return None
        if len(self.EDG[j]) == 0:
            self.DPA[j]=(0,[])
            return None
        tmp = 1<<30
        tmv = []
        for k in self.EDG[j]:
            self.make_DP(k)
            if tmp > self.DPA[k][0]:
                tmp = self.DPA[k][0]
                tmv = []
                tmv.append(k)
            elif tmp == self.DPA[k][0]:
                tmv.append(k)
        self.DPA[j]=(-tmp,tmv)
        return None
    ################################
    def __init__(self, file):
        self.DPA=[]
        if file != None:
            self.loadFile(file)
    def loadFile(self, file):
        #print 'F6 start loading ', file
        starttime = time.clock()
        self.DPA = []
        for i in range(self.IDT):
            self.DPA.append((65536,[]))
        f1=open(file, 'r')
        with f1:
            content = f1.readlines()
        f1.close()
        for s in content:
            ss = s.split()
            ID = (int(ss[0]),int(ss[1]),int(ss[2]))
            if ID in self.NID:
                self.DPA[self.NID[ID]]=(float(ss[4]),[])
        for i in range(self.IDT):
            self.make_DP(i)
        #print 'F6 loadFile time: ', time.clock()-starttime
    def isMove(self, board, Tile):
        ID = getBoardID_6(board, Tile)
        return ID in self.NID and len(self.DPA[self.NID[ID]][1])>0
    def getMove(self, board, Tile):
        if self.isMove(board, Tile):
            #print 'get from fisrt6'
            ID = getBoardID_6(board, Tile)
            #print 'F6 get score ', self.DPA[self.NID[ID]][0]
            ID = self.RID[ random.choice(self.DPA[self.NID[ID]][1]) ]
            if Tile == BLACK:
                myMoves, opMoves = getBothValidMoves(board)
            else:
                opMoves, myMoves = getBothValidMoves(board)
            for move in myMoves:
                nboard = getBoardCopy(board)
                makeMove(nboard, Tile, move[0], move[1])
                if ID == getBoardID_6(nboard, Tile^1):
                    return move
            print 'fisrt6 getMove Error!'
            return (0, 0)
        else:
            return EndAllWithMinMaxAI().getMove(board, Tile)