from __future__ import division
import sys, getopt
import copy

#disLib = [['diabetes',0.3,[](finding),[](pd),[](pnd)]...]
#patLib = [[[](test on disease-1),[](test on disease-2]...]

def roundTo4digit(p):
    return '{:.4f}'.format(round(p,4))

def estPatProb(disLib,patLib,pIndex,dIndex):
    joint = disLib[dIndex][1]
    marginalF = 1 - disLib[dIndex][1]
    for k in range(0,len(patLib[pIndex][dIndex])):
        if patLib[pIndex][dIndex][k] == 'T':
            joint = joint * disLib[dIndex][3][k]
            marginalF = marginalF * disLib[dIndex][4][k]
        elif patLib[pIndex][dIndex][k] == 'F':
            joint = joint * (1 - disLib[dIndex][3][k])
            marginalF = marginalF * (1-disLib[dIndex][4][k])
    p = joint / (marginalF + joint)
    return p


def estProb(disLib,patLib):
    result = {}
    for i in range(0,len(patLib)):
        pn = "Patient-"+(str)(i+1)
        result[pn] = {}
        for j in range(0,len(patLib[i])):
            p = estPatProb(disLib,patLib,i,j)
            result[pn][disLib[j][0]] = roundTo4digit(p)
    return result

def testBit(num,offset):
    mask = 1 << offset
    return (num & mask)

def maxMinProb(disLib,patLib):
    nDisLib = copy.deepcopy(disLib)
    nPatLib = copy.deepcopy(patLib)
    result = {}
    for i in range(0,len(nPatLib)):
        pn = "Patient-"+(str)(i+1)
        result[pn] = {}
        for j in range(0,len(nPatLib[i])):
            minProb = 2.0
            maxProb = -1.0
            unknownList = []
            for k in range(0,len(nPatLib[i][j])):
                if nPatLib[i][j][k] == 'U':
                    unknownList.append(k)
            #no unknown test result
            if len(unknownList) == 0:
                p = estPatProb(nDisLib,nPatLib,i,j)
                result[pn][nDisLib[j][0]] = []
                result[pn][nDisLib[j][0]].append(roundTo4digit(p))
                result[pn][nDisLib[j][0]].append(roundTo4digit(p))
                continue
            maxIteration = 2 << (len(unknownList)-1)
            for k in range(0,maxIteration):
                index = -1
                for l in range(0,len(unknownList)):
                    if testBit(k,l):
                        nPatLib[i][j][unknownList[index]] = 'T'
                    else:
                        nPatLib[i][j][unknownList[index]] = 'F'
                    index = index - 1
                p = estPatProb(nDisLib,nPatLib,i,j)
                if p < minProb:
                    minProb = p
                if p > maxProb:
                    maxProb = p
            result[pn][nDisLib[j][0]] = []
            result[pn][nDisLib[j][0]].append(roundTo4digit(minProb))
            result[pn][nDisLib[j][0]].append(roundTo4digit(maxProb))
    return result

def nextTest(odisLib,opatLib):
    disLib = copy.deepcopy(odisLib)
    patLib = copy.deepcopy(opatLib)
    result = {}
    for i in range(0,len(patLib)):
        pn = "Patient-"+(str)(i+1)
        result[pn] = {}
        for j in range(0,len(patLib[i])):
            origP = estPatProb(disLib,patLib,i,j)
            result[pn][disLib[j][0]] = []
            unknownList = []
            maxIncFind = []
            maxDecFind = []
            maxInc = -1.0
            maxDec = -1.0
            for k in range(0,len(patLib[i][j])):
                if patLib[i][j][k] == 'U':
                    unknownList.append(k)
            for index in unknownList:
                #test True state
                patLib[i][j][index] = 'T'
                np = estPatProb(disLib,patLib,i,j)
                if np > origP:
                    inc = np - origP
                    if inc > maxInc:
                        maxInc = inc
                        if len(maxIncFind)==0:
                            maxIncFind.append(disLib[j][2][index])
                            maxIncFind.append('T')
                        else:
                            maxIncFind[0] = disLib[j][2][index]
                            maxIncFind[1] = 'T'
                elif np < origP:
                    dec = origP - np
                    if dec > maxDec:
                        maxDec = dec
                        if len(maxDecFind) == 0:
                            maxDecFind.append(disLib[j][2][index])
                            maxDecFind.append('T')
                        else:
                            maxDecFind[0] = disLib[j][2][index]
                            maxDecFind[1] = 'T'
                #test False state
                patLib[i][j][index] = 'F'
                np = estPatProb(disLib,patLib,i,j)
                if np > origP:
                    inc = np - origP
                    if inc > maxInc:
                        maxInc = inc
                        if len(maxIncFind) == 0:
                            maxIncFind.append(disLib[j][2][index])
                            maxIncFind.append('F')
                        else:
                            maxIncFind[0] = disLib[j][2][index]
                            maxIncFind[1] = 'F'
                elif np < origP:
                    dec = origP - np
                    if dec > maxDec:
                        maxDec = dec
                        if len(maxDecFind) == 0:
                            maxDecFind.append(disLib[j][2][index])
                            maxDecFind.append('F')
                        else:
                            maxDecFind[0] = disLib[j][2][index]
                            maxDecFind[1] = 'F'
                patLib[i][j][index] = 'U'
            if maxInc == -1.0:
                result[pn][disLib[j][0]].append('none')
                result[pn][disLib[j][0]].append('N')
            else:
                find = maxIncFind[0]
                res = maxIncFind[1]
                result[pn][disLib[j][0]].append(find)
                result[pn][disLib[j][0]].append(res)
            if maxDec == -1.0:
                result[pn][disLib[j][0]].append('none')
                result[pn][disLib[j][0]].append('N')
            else:
                find = maxDecFind[0]
                res = maxDecFind[1]
                result[pn][disLib[j][0]].append(find)
                result[pn][disLib[j][0]].append(res)
    return result




def main(argv):
    inputFile = ""
    outputFile = ""
    try:
        opts,args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print "python bayes.py -i <inputfile>"
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-i":
            inputFile = arg

    index = inputFile.rfind('/')
    dotIndex = inputFile.rfind('.')
    if index != -1:
        libPath = inputFile[:index]
        if dotIndex != -1:
            fileName = inputFile[index+1:dotIndex]
            outputFile = libPath + '/' + fileName + '_inference' + inputFile[dotIndex:]
        else:
            fileName = inputFile[index+1:]
            outputFile = libPath + '/' + fileName + '_inference'
    else:
        if dotIndex != -1:
            fileName = inputFile[:dotIndex]
            outputFile = fileName + '_inference' + inputFile[dotIndex:]
        else:
            outputFile = inputFile + '_inference'
    fin = open(inputFile,"r")
    fout = open(outputFile,"w")
    line = fin.readline()
    para = line.split(' ')
    nDise = (int)(para[0])
    disLib = []
    patLib = []
    nPat = (int)(para[1])
    for i in range(0,nDise):
        line = fin.readline()
        lines = line.split(' ')
        name = lines[0]
        p = (float)(lines[2])
        disLib.append([])
        disLib[i].append(name)
        disLib[i].append(p)
        line = fin.readline()
        disLib[i].append(eval(line))
        line = fin.readline()
        disLib[i].append(eval(line))
        line = fin.readline()
        disLib[i].append(eval(line))
    for i in range(0, nPat):
        patLib.append([])
        for j in range(0,nDise):
            line = fin.readline()
            patLib[i].append(eval(line))
    q1result = estProb(disLib,patLib)
    q2result = maxMinProb(disLib,patLib)
    q3result = nextTest(disLib,patLib)
    for i in range(0,nPat):
        item = "Patient-"+(str)(i+1)
        fout.write(item+':\n')
        fout.write(str(q1result[item])+'\n')
        fout.write(str(q2result[item])+'\n')
        fout.write(str(q3result[item])+'\n')
    fin.close()
    fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])