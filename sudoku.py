#!/usr/bin/python
# Filename : sudoku.py
# TODO need read from file and try to finish all current 100 cases

import sys
import os
import getopt
import copy
import time
from enum import Enum

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
'''
TABLE_LIST = [
    0, 0, 5, 3, 0, 0, 0, 0, 0,
    8, 0, 0, 0, 0, 0, 0, 2, 0,
    0, 7, 0, 0, 1, 0, 5, 0, 0,

    4, 0, 0, 0, 0, 5, 3, 0, 0,
    0, 1, 0, 0, 7, 0, 0, 0, 6,
    0, 0, 3, 2, 0, 0, 0, 8, 0,

    0, 6, 0, 5, 0, 0, 0, 0, 9,
    0, 0, 4, 0, 0, 0, 0, 3, 0,
    0, 0, 0, 0, 0, 9, 7, 0, 0,
]
'''
class STATE(Enum):
    NONE      = 0   # not sure
    DEDUCTION = 1   # pure deduction
    GUESS     = 2   # pure guess
    MIXED     = 3   # it is deduction itself but previous result is based on guess

class PARSE(Enum):
    NAME      = 0   # parsing name
    CELL      = 1   # parsing cells

class cell:
    def __init__(self):
        self.iValue = 0                                      # data
        self.possibilityList = [n for n in range(1, SIZE+1)] # possible value
        self.groupIndexList = []                             # GroupList index
        self.iTime = 0xFFFFFFFF                              # solved iTime
        self.state = STATE.NONE                              # initial state
        self.strSolve = ''                                   # solve description

class group:
    def __init__(self):
        self.cellList = []   # one group is a cell list
        self.strName = ''    # group name

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

def loadCellList(cellList, tableList):
    for i in range(len(cellList)):
        if(tableList[i] != 0 ) :
            answer = tableList[i]
            cellList[i].iValue = answer
            cellList[i].possibilityList = [answer]
            cellList[i].iTime  = 0  # 0 iTime means solved when init.

def removePossibility(cellList, groupList):
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

def markNakedSingle(cellList, groupList, iTime, bPureDeduction):
    bUpdate = False
    # When a cell is only have one possibility, then its value is done.
    for i in range(len(cellList)):
        if ((len(cellList[i].possibilityList) == 1) and (cellList[i].iValue == 0)):
            value = cellList[i].possibilityList[0]
            cellList[i].iValue = value
            cellList[i].iTime = iTime
            cellList[i].state = STATE.DEDUCTION if (bPureDeduction == True) else STATE.MIXED
            cellList[i].strSolve ='r{0:d}c{1:d} = {2:d} as naked single'.format(int(i/SIZE)+1,int(i%SIZE)+1, value)

            # Since it is based on guess, we need update possibilities every time to find no answer immediately
            if (bPureDeduction == False):
                removePossibility(cellList, groupList)

            bUpdate = True
    return bUpdate

def markHiddenSingle(cellList, groupList, iTime, bPureDeduction):
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
                cellList[lastIndex].state = STATE.DEDUCTION if (bPureDeduction == True) else STATE.MIXED
                cellList[lastIndex].strSolve = 'r{0:d}c{1:d} = {2:d} as hidden single of {3}' \
                                              .format(int(lastIndex / SIZE) + 1, int(lastIndex % SIZE) + 1, v, l.strName)
                # Since it is based on guess, we need update possibilities every time to find no answer immediately
                if (bPureDeduction == False):
                    removePossibility(cellList, groupList)

                bUpdate = True

    return bUpdate

def checkSolved(cellList):
    bSolved = True
    for cell in cellList:
        if (cell.iValue == 0):
            bSolved= False
            break

    return bSolved

def checkValid(cellList, groupList):
    bValid = True
    for cell in cellList:
        if (cell.iValue == 0 and len(cell.possibilityList) == 0):
            bValid= False
            break
    return bValid

def checkNoDuplicate(cellList, groupList ):
    strError=''
    bNoDuplicate = True

    for group in groupList:
        countList = [0] * (SIZE+1)
        for i in group.cellList:
            if (cellList[i].iValue !=0):
                j = cellList[i].iValue
                countList[j] += 1
                if(countList[j]>1):
                    strError = 'Invalid case! Group {0} has multiple value {1:d} '.format(group.strName, j)
                    bNoDuplicate = False
                    break
        if (bNoDuplicate == False):
            break

    return strError

def solveByBackTraking(cellList, groupList, iTime, bLoopAll):
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
    oldtimeList = [0] * len(indexList)

    # backup first old cellList
    oldcellList[0] = copy.deepcopy(cellList)
    oldtimeList[0] = iTime

    while (bTraversed == False):
        i = indexList[currentIdx]
        j = currentList[currentIdx]

        value = cellList[i].possibilityList[j]
        cellList[i].iValue = value
        cellList[i].iTime = iTime
        cellList[i].possibilityList = [value]
        cellList[i].strSolve = 'r{0:d}c{1:d} = {2:d} by\033[1;31m guess\033[0m '\
                                .format(int(i / SIZE) + 1, int(i % SIZE) + 1, value)
        removePossibility(cellList, groupList)

        bUpdated = True
        while (bUpdated) :
            bUpdated = solveByDeduction(cellList, groupList, iTime, False)

        bValid = checkValid(cellList, groupList)

        if (bValid) :
            iTime += 1
            while True :
                currentIdx += 1
                if(currentIdx >= len(indexList)):
                    break

                # backup old cellList
                oldcellList[currentIdx] = copy.deepcopy(cellList)
                oldtimeList[currentIdx] = iTime

                i = indexList[currentIdx]
                if (cellList[i].iValue == 0):
                    cellList[i].state = STATE.GUESS
                    break

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
                # restore old cellList
                cellList = copy.deepcopy(oldcellList[currentIdx])
                iTime = oldtimeList[currentIdx]

                i = indexList[currentIdx]
                currentList[currentIdx] += 1
                # when try next possibility, if meet any of following 2 conditions,
                # we need reset its state and go back further.
                # 1, Have tried all possibilities of that cell.
                # 2, This cell state is based on deduction, but one of its dependant cell state is by guess.
                if (currentList[currentIdx] >= len(cellList[i].possibilityList) or cellList[i].state == STATE.MIXED):
                    cellList[i].state = STATE.NONE
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
def printCellList(cellList, bSolved, bStep,i):
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
            print('Time = %d ' % iTime)

        needPrint = False
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
            for i in range(len(cellList)):
                if (cellList[i].iTime == iTime and cellList[i].strSolve !=''):
                    print(cellList[i].strSolve)
            print('')
            iTime += 1

    return

def solveByDeduction(cellList, groupList, iTime, bPureDeduction):
    bUpdated = False
    # Rule 1
    bResult = removePossibility(cellList, groupList)
    bUpdated = bUpdated or bResult

    # Rule 2
    bResult = markNakedSingle(cellList, groupList, iTime, bPureDeduction)
    bUpdated = bUpdated or bResult

    # Rule 3, mark hidden single cell
    bResult = markHiddenSingle(cellList, groupList, iTime, bPureDeduction)
    bUpdated = bUpdated or bResult

    return bUpdated

def solveOneCellList(numList, strname, bStep):
    answerCellLists = []
    groupList = initGroupList()
    cellList = initCellList(groupList)
    loadCellList(cellList, numList)

    strError = checkNoDuplicate(cellList, groupList)
    if(strError!=''):
        print('['+strname+']'+strError)
    else :
        print('['+strname+'] is solving')
        iTime = 1
        bSolved = False
        bUpdated = True
        while ((bSolved != True) and bUpdated)  :

            bUpdated = solveByDeduction(cellList, groupList, iTime, True)

            bSolved = checkSolved(cellList)
            if (bUpdated) :
                iTime +=1

        if (bSolved == True) :
            answerCellLists.append(cellList)
        else :
            bLoopAll = True
            answerCellLists = solveByBackTraking(cellList, groupList, iTime, bLoopAll)

        for i in range(len(answerCellLists)):
            bSolved = checkSolved(answerCellLists[i])
            printCellList(answerCellLists[i], bSolved, bStep, i)
    return

def readCellLists(input_file, tableLists, strnames):
    file_object = open(input_file, 'r')
    state = PARSE.NAME
    try:
        for line in file_object:
            if (state == PARSE.NAME):
                s = line.find('[')
                e = line.find(']', s)
                if (s != -1 and e != -1):
                    strnames.append(copy.deepcopy(line[s+1:e]))
                    state = PARSE.CELL
                    tableList = []
            elif (state == PARSE.CELL):
                new_str = ''
                for ch in line:
                    if ch.isdigit():
                        new_str += ch
                    else:
                        new_str += " "
                sub_list = new_str.split()
                for sub_str in sub_list:
                    tableList.append(eval(sub_str))
                if (len(tableList)>= SIZE*SIZE):
                    state = PARSE.NAME
                    tableLists.append(copy.deepcopy(tableList[:SIZE*SIZE]))
                    if (len(tableList)> SIZE*SIZE):
                        print('{0} input number is {1:d} > {2:d}'\
                              .format(strnames[-1], len(tableList), SIZE*SIZE))
    finally:
        if (len(strnames) > len(tableLists)):
            strnames = strnames[:len(tableLists)]
        elif (len(strnames) < len(tableLists)):
            tableLists = tableLists[:len(strnames)]

        file_object.close()
    return

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'i:v:')
    input_file = ''

    bStep = True
    for op, value in opts:
        if op == '-i':
            input_file = value
        elif op == '-v':
            bStep = (int(value)!=0)

    if (input_file == ''):
        tableList = TABLE_LIST
        strname   = "Default"
        solveOneCellList(tableList, strname, bStep)
    else :
        tableLists = []
        strnames = []
        readCellLists(input_file, tableLists, strnames)
        for i in range(len(tableLists)):
            solveOneCellList(tableLists[i], strnames[i], bStep)

    return
if __name__ == '__main__':
    sys.exit(main())