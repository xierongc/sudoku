#!/usr/bin/python
# Filename : sudoku.py
import sys
import os
import copy
import time

os.system("") # unkown reason, use this then later CSI color control can take effect in windows

# General algorithm,we need to change SIZE/GROUP_LIST/GROUP_NAME_LIST to adapt to other size of sudoku
# Current settings is 9*9
#  *************************************
#  *0   1   2  *3   4   5  *6   7   8  *
#  *9   10  11 *12  13  14 *15  16  17 *
#  *18  19  20 *21  22  23 *24  25  26 *
#  *************************************
#  *27  28  29 *30  31  32 *33  34  35 *
#  *36  37  38 *39  40  41 *42  43  44 *
#  *45  46  47 *48  49  50 *51  52  53 *
#  *************************************
#  *54  55  56 *57  58  59 *60  61  62 *
#  *63  64  65 *66  67  68 *69  70  71 *
#  *72  73  74 *75  76  77 *78  79  80 *
#  *************************************

SIZE = 9
GROUP_LIST= [
# 1, 9 Rows
[    0,  1,  2,  3,  4,  5,  6,  7,  8, ],
[    9, 10, 11, 12, 13, 14, 15, 16, 17, ],
[   18, 19, 20, 21, 22, 23, 24, 25, 26, ],
[   27, 28, 29, 30, 31, 32, 33, 34, 35, ],
[   36, 37, 38, 39, 40, 41, 42, 43, 44, ],
[   45, 46, 47, 48, 49, 50, 51, 52, 53, ],
[   54, 55, 56, 57, 58, 59, 60, 61, 62, ],
[   63, 64, 65, 66, 67, 68, 69, 70, 71, ],
[   72, 73, 74, 75, 76, 77, 78, 79, 80, ],
# 2, 9 Columns
[    0,  9, 18, 27, 36, 45, 54, 63, 72, ],
[    1, 10, 19, 28, 37, 46, 55, 64, 73, ],
[    2, 11, 20, 29, 38, 47, 56, 65, 74, ],
[    3, 12, 21, 30, 39, 48, 57, 66, 75, ],
[    4, 13, 22, 31, 40, 49, 58, 67, 76, ],
[    5, 14, 23, 32, 41, 50, 59, 68, 77, ],
[    6, 15, 24, 33, 42, 51, 60, 69, 78, ],
[    7, 16, 25, 34, 43, 52, 61, 70, 79, ],
[    8, 17, 26, 35, 44, 53, 62, 71, 80, ],
# 3, 9 blocks
[    0,  1,  2,  9, 10, 11, 18, 19, 20, ],
[    3,  4,  5, 12, 13, 14, 21, 22, 23, ],
[    6,  7,  8, 15, 16, 17, 24, 25, 26, ],
[   27, 28, 29, 36, 37, 38, 45, 46, 47, ],
[   30, 31, 32, 39, 40, 41, 48, 49, 50, ],
[   33, 34, 35, 42, 43, 44, 51, 52, 53, ],
[   54, 55, 56, 63, 64, 65, 72, 73, 74, ],
[   57, 58, 59, 66, 67, 68, 75, 76, 77, ],
[   60, 61, 62, 69, 70, 71, 78, 79, 80, ],
]
GROUP_NAME_LIST=[
'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9',
'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9',
'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9',
]
# need solved issue
'''
TABLE_LIST = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 2, 0, 0, 0, 0, 0, 8, 4,
    0, 3, 0, 0, 0, 0, 0, 7, 0,

    0, 0, 4, 0, 0, 0, 6, 0, 0,
    0, 0, 0, 2, 0, 3, 0, 0, 0,
    0, 0, 5, 0, 0, 0, 9, 0, 0,

    0, 0, 6, 0, 9, 0, 5, 0, 0,
    0, 7, 0, 0, 0, 0, 0, 2, 0,
    0, 0, 0, 0, 5, 0, 0, 0, 0,
]
'''
TABLE_LIST = [
    7, 5, 0, 0, 9, 0, 0, 4, 6,
    9, 0, 1, 0, 0, 0, 3, 0, 2,
    0, 0, 0, 0, 0, 0, 0, 0, 0,

    2, 0, 0, 6, 0, 1, 0, 0, 7,
    0, 8, 0, 0, 0, 0, 0, 2, 0,
    1, 0, 0, 3, 0, 8, 0, 0, 5,

    0, 0, 0, 0, 0, 0, 0, 0, 0,
    3, 0, 9, 0, 0, 0, 2, 0, 4,
    8, 4, 0, 0, 3, 0, 0, 7, 9,
]

class cell:
    def __init__(self):
        self.iValue = 0                                      # data
        self.possibilityList = [n for n in range(1, SIZE+1)] # possible value
        self.groupIndexList = []                             # GroupList index
        self.iTime = 0xFFFFFFFF                              # solved iTime

class group:
    def __init__(self):
        self.cellList = []   # one group is a cell list
        self.strName = ''     # group name

class solver:
    def __init__(self):
        self.strDesc = ''
        self.iTime = 0xFFFFFFFF                              # solved iTime

def initCellList(groupList):
    cellList = []
    for i in range(SIZE*SIZE):
        cellList.append(cell())

    for i in range(len(groupList)):
        for j in range(len(groupList[0].cellList)):
            index = groupList[i].cellList[j]
            cellList[index].groupIndexList.append(i)

    return cellList


def initGroupList():
    groupList = []
    for i in range(len(GROUP_LIST)):
        groupList.append(group())

    for i in range(len(groupList)):
        groupList[i].cellList = GROUP_LIST[i]
        groupList[i].strName  = GROUP_NAME_LIST[i]

    cellList = [0] * (SIZE*SIZE)

    for i in range(len(groupList)):
        for j in range(len(groupList[0].cellList)):
            index = groupList[i].cellList[j]
            cellList[index] += 1

    bCheckResult = True
    for i in range(len(cellList)):
        if (cellList[i] != 3) :
            bCheckResult = False;
            print ('%d not init correct' %(i))
    if (bCheckResult == False) :
         AssertionError()

    return groupList

def loadCellList(cellList):
    for i in range(len(cellList)):
        if(TABLE_LIST[i] != 0 ) :
            answer = TABLE_LIST[i]
            cellList[i].iValue = answer
            cellList[i].possibilityList = [answer]
            cellList[i].iTime  = 0  # 0 iTime means solved when init.

def removePossibility(cellList, groupList, solverList):
    bUpdate = False
    for i in range(len(cellList)):
        value = cellList[i].iValue
        if ( value != 0):
            for l in groupList :
                if (l.cellList.count(i) >= 1) :
                    for j in l.cellList :
                        if ((j != i) and (cellList[j].possibilityList.count(value) >=1)):
                            cellList[j].possibilityList.remove(value)
                            bUpdate = True
    return bUpdate

def markNakedSingle(cellList, groupList, solverList, iTime):
    bUpdate = False
    # When a cell is only have one possibility, then its value is done.
    for i in range(len(cellList)):
        if ((len(cellList[i].possibilityList) == 1) and (cellList[i].iValue == 0)):
            value = cellList[i].possibilityList[0]
            cellList[i].iValue = value
            cellList[i].iTime = iTime

            s = solver()
            s.iTime = iTime
            s.strDesc = 'r{0:d}c{1:d} = {2:d} as naked single'.format(int(i/SIZE)+1,int(i%SIZE)+1, value)
            solverList.append(s)

            bUpdate = True
    return bUpdate

def markHiddenSingle(cellList, groupList, solverList, iTime):
    bUpdate = False
    # For specific value, when a group only has one cell that own this value's possibility,
    # Then this cell's value is done with this specific value.
    for l in groupList :
        for v in range(1, SIZE+1):
            vCount     = 0     # vCount store value count in that group
            lastIndex  = 0     # last index store last cell index which its contain this v possibility
            for i in l.cellList:
                count = cellList[i].possibilityList.count(v)
                vCount += count
                if (count>0):
                    lastIndex = i

            if (vCount == 1 and cellList[lastIndex].iValue == 0):
                cellList[lastIndex].iValue = v
                cellList[lastIndex].iTime = iTime
                cellList[lastIndex].possibilityList = [v]

                s = solver()
                s.iTime = iTime
                s.strDesc = 'r{0:d}c{1:d} = {2:d} as hidden single of {3}'\
                            .format(int(lastIndex / SIZE) + 1, int(lastIndex % SIZE) + 1, v, l.strName)
                solverList.append(s)

                bUpdate = True

    return bUpdate

def checkSolved(cellList):
    bSolved = True
    for cell in cellList:
        if (cell.iValue == 0):
            bSolved= False
            break

    return bSolved

def checkValid(cellList):
    bValid = True
    for cell in cellList:
        if (cell.iValue == 0 and len(cell.possibilityList) == 0):
            bValid= False
            break
    return bValid

def runBackTracking(cellList, groupList, solverList, iTime, bLoopAll):
    print('Use back tracking to force search the answer.')
    baseTime = time.time()

    # Record all unsolved cell
    indexList=[]
    totalLenList=[]

    # Use ascending order to generate indexList and totalLenList
    for i in range(len(cellList)):
        if (cellList[i].iValue == 0):
            bInsert = False
            for j in range(len(totalLenList)) :
                if (len(cellList[i].possibilityList)<totalLenList[j]):
                    indexList.insert(j,i)
                    totalLenList.insert(j, len(cellList[i].possibilityList))
                    bInsert = True
                    break
            if(bInsert == False):
                indexList.append(i)
                totalLenList.append(len(cellList[i].possibilityList))

    # Prepare totalLenList for progress indicator
    l = len(totalLenList)
    for i in range(l-1,-1,-1):
        if( i < l-1):
            totalLenList[i]= totalLenList[i]*totalLenList[i+1]

    # Record current index
    currentList=[0]*len(indexList)
    currentIdx = 0

    bTraversed = False
    bContinue = False
    iAnswerNum = 0
    answerCellLists = []
    oldcellList = cellList * len(indexList)

    while (bTraversed == False):
        i = indexList[currentIdx]
        j = currentList[currentIdx]

        oldcellList[currentIdx]=copy.deepcopy(cellList)  # backup old cellList
        value = cellList[i].possibilityList[j]
        cellList[i].iValue = value
        cellList[i].iTime = iTime
        cellList[i].possibilityList = [value]

        removePossibility(cellList, groupList, solverList)
        bValid = checkValid(cellList)

        if (bValid) :
            currentIdx += 1
            if(currentIdx >= len(indexList)):
                if(iAnswerNum==0):
                    print('The 1st answer is founded.')
                answerCellLists.append(copy.deepcopy(cellList))
                iAnswerNum += 1
                if(bLoopAll != True):
                    bTraversed = True
                else:
                    bContinue = True
                    currentIdx -= 1

        if (bValid == False or bContinue):
            bContinue = False   # Reset bContinue
            bBackward = True
            while(bBackward):
                cellList = copy.deepcopy(oldcellList[currentIdx])
                i = indexList[currentIdx]
                currentList[currentIdx] += 1
                if (currentList[currentIdx] >= len(cellList[i].possibilityList)):
                    currentList[currentIdx] = 0
                    currentIdx -= 1
                    if (currentIdx<0):
                        bTraversed = True
                        break
                else:
                    bBackward = False

        currentTime = time.time()
        if (currentTime-baseTime > 0.5) :
            baseTime = currentTime
            s = 0
            for i in range(len(currentList)):
                if (i< len(currentList)-1):
                    s += currentList[i]*totalLenList[i+1]
                else:
                    s += currentList[i]
            f = float(s)/float(totalLenList[0])
            print('\rSearching status = %.0f%% ' % (f*100), end='')
    print('\rSearching status = 100% ')
    print('')
    if(bLoopAll) :
        if(iAnswerNum == 1):
            print('\rThe question is verified by backtracking all possibilities.')
        else:
            print('\rThe question is not correct, it has %d answers.' % iAnswerNum)

    return answerCellLists

MAX_TIME=0xFFFFFFFF
def printCellList(cellList, solverList, bSolved, bStep,i):
    if (bSolved):
        print('OK! It is solved. This is answer %d.' % i)
    else:
        print('Sorry, still working on it.')

    if bStep==True :
        iTime = 0
    else:
        iTime = MAX_TIME

    needPrint = True
    while ( needPrint ) :

        if bStep == True:
            needPrint = False
            print('Time = %d ' % iTime)

        for i in range(len(cellList)):
            if (cellList[i].iValue != 0):
                if (cellList[i].iTime == iTime):
                    print('\033[1;31m%d\033[0m ' % cellList[i].iValue,end='') # print value with highlight
                elif (cellList[i].iTime < iTime):
                    print('%d '% cellList[i].iValue,end='') # print value normally
                else:
                    print('0 ',end='') # no need to print at current iTime but need print in another run
                    if bStep == True:
                        needPrint = True
            else:
                print('0 ',end='')  # no need to print at current iTime

            if ((i+1) % SIZE == 0) :
                print('') # new line

        if bStep == True:
            for s in solverList:
                if (s.iTime == iTime):
                    print(s.strDesc)
            print('')
            iTime += 1
        else:
            needPrint = False

    return

def main():
    answerCellLists = []
    solverList = []
    groupList = initGroupList()
    cellList = initCellList(groupList)
    loadCellList(cellList)

    iTime = 1
    bSolved = False
    bUpdated = True
    while ((bSolved != True) and bUpdated)  :
        bUpdated = False

        # Rule 1
        bResult  = removePossibility(cellList, groupList, solverList)
        bUpdated = bUpdated or bResult

        # Rule 2
        bResult  = markNakedSingle(cellList, groupList, solverList, iTime)
        bUpdated = bUpdated or bResult

        # Rule 3, mark hidden single cell
        bResult  = markHiddenSingle(cellList, groupList, solverList, iTime)
        bUpdated = bUpdated or bResult

        bSolved = checkSolved(cellList)
        if (bUpdated) :
            iTime +=1

    if (bSolved == True) :
        answerCellLists.append(cellList)
    else:
        bLoopAll = True
        answerCellLists = runBackTracking(cellList, groupList, solverList, iTime, bLoopAll)

    bStep = True
    for i in range(len(answerCellLists)):
        bSolved = checkSolved(answerCellLists[i])
        printCellList(answerCellLists[i], solverList, bSolved, bStep, i)
    return

if __name__ == '__main__':
    sys.exit(main())