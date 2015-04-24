from __future__ import division
import sys,getopt
import db
import sqlite3
import copy

class Vertex:

    def __init__(self,name,catList):
        self.name = name
        self.connection = []
        self.category = catList[:]
        self.priorProb = {}
        for cat in self.category:
            self.priorProb[cat] = 0.0
        self.pcategory = {}
        self.sink = True
        self.conditionP = {}

    def addConnection(self,node):
        if self.sink:
            self.sink = False
        pcat = node.getCategory()
        self.pcategory[node.getName()] = pcat[:]
        self.connection.append(node)
        self.conditionP[node.getName()] = {}
        for item1 in pcat:
            for item2 in self.category:
                self.conditionP[node.getName()][(item1,item2)] = 0.0

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getParentCategory(self):
        return self.pcategory

    def getConnection(self):
        return self.connection

    def isEdge(self,node):
        for n in self.connection:
            assert isinstance(n,Vertex)
            if n.getName() == node.getName():
                return True
            else:
                continue
        return False

    def isSink(self):
        return self.sink

    def setPriorProb(self,key,value):
        self.priorProb[key] = value

    def setConditionP(self,pname,key,value):
        self.conditionP[pname][key]=value

class Graph:

    def __init__(self):
        self.vertex = {}

    def addVertex(self,node):
        if isinstance(node,Vertex):
            name = node.getName()
            self.vertex[name] = node
        else:
            print "parameter must be instance of Vertex"

    def addEdge(self,nodef,nodet):
        assert isinstance(nodef,str) and isinstance(nodet,str)
        if nodef in self.vertex and nodet in self.vertex:
            nf = self.vertex[nodef]
            nt = self.vertex[nodet]
            assert isinstance(nf,Vertex) and isinstance(nt,Vertex)
            nf.addConnection(nt)

    def isEdge(self,nodef,nodet):
        assert isinstance(nodef,str) and isinstance(nodet,str)
        if nodef in self.vertex and nodet in self.vertex:
            nf = self.vertex[nodef]
            nt = self.vertex[nodet]
            assert isinstance(nf,Vertex) and isinstance(nt,Vertex)
            return nf.isEdge(nt)
        else:
            return False

    def getVertex(self):
        return self.vertex


def initGraph():
    dag = Graph()
    nodes = []
    defaultList = ['no','yes']
    #topological sort
    nodes.append(Vertex('diabetes',defaultList))
    nodes.append(Vertex('stroke',defaultList))
    nodes.append(Vertex('attack',defaultList))
    nodes.append(Vertex('angina',defaultList))
    nodes.append(Vertex('bmi',['underweight','normal','overweight','obese']))
    nodes.append(Vertex('bp',defaultList))
    nodes.append(Vertex('cholesterol',defaultList))
    nodes.append(Vertex('exercise',defaultList))
    nodes.append(Vertex('smoke',defaultList))
    nodes.append(Vertex('income',['25000','25001-50000','50001-75000','75000']))
    nodes[0].addConnection(nodes[4])
    nodes[1].addConnection(nodes[4])
    nodes[2].addConnection(nodes[4])
    nodes[3].addConnection(nodes[4])
    nodes[1].addConnection(nodes[5])
    nodes[2].addConnection(nodes[5])
    nodes[3].addConnection(nodes[5])
    nodes[1].addConnection(nodes[6])
    nodes[2].addConnection(nodes[6])
    nodes[3].addConnection(nodes[6])
    nodes[4].addConnection(nodes[7])
    nodes[5].addConnection(nodes[7])
    nodes[6].addConnection(nodes[7])
    nodes[5].addConnection(nodes[8])
    nodes[6].addConnection(nodes[8])
    nodes[4].addConnection(nodes[9])
    nodes[5].addConnection(nodes[9])
    nodes[6].addConnection(nodes[9])
    nodes[7].addConnection(nodes[9])
    nodes[8].addConnection(nodes[9])

    for node in nodes:
        dag.addVertex(node)

    return dag

def initCPT(graph,cursor,tableName):
    assert isinstance(graph,Graph)
    assert isinstance(cursor,sqlite3.Cursor)
    vertex = graph.getVertex()
    #get the total number of record in the database
    cursor.execute('SELECT * FROM {0}'.format(tableName))
    recordTotal = len(cursor.fetchall())
    for key in vertex:
        v = vertex[key]
        assert isinstance(v,Vertex)
        if v.isSink():
            category = v.getCategory()
            for cate in category:
                command = 'SELECT * FROM {0} WHERE {1}=\'{2}\''.format(tableName,v.getName(),cate)
                cursor.execute(command)
                p = len(cursor.fetchall())/recordTotal
                v.setPriorProb(cate,p)
        else:
            category = v.getCategory()
            pcategory = v.getParentCategory()
            for pn in pcategory:
                ccategory = pcategory[pn]
                for key1 in ccategory:
                    cursor.execute('SELECT * FROM {0} WHERE {1}=\'{2}\''.format(tableName,pn,key1))
                    recordT = len(cursor.fetchall())
                    for key2 in category:
                        cursor.execute('SELECT * FROM {0} WHERE {1}=\'{2}\' AND {3}=\'{4}\''.format(tableName,pn,key1,v.getName(),key2))
                        recordC = len(cursor.fetchall())
                        p = recordC/recordT
                        v.setConditionP(pn,(key1,key2),p)

def estProbQuery(query):


def main(argv):
    inputFile = ""
    dataFile = ""
    dbFile = "riskData.db"
    outputFile = "riskFactor_output.txt"
    tableName = "risks"
    try:
        opts,args = getopt.getopt(argv,"i:d:",["ifile=","dfile="])
    except getopt.GetoptError:
        print "python bayes.py -i <inputfile> -d <datafile>"
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-i":
            inputFile = arg
        elif opt == "-d":
            dataFile = arg

    fin = open(inputFile,"r")
    fout = open(outputFile,"w")

    graph = initGraph()
    db.initDB(dataFile,dbFile)
    conn = db.getConnection(dbFile)
    cursor = db.getCursor(conn)
    initCPT(graph,cursor,tableName)

    lines = fin.readlines()
    testCaseNum = (int)(lines[0])
    for i in range(1,testCaseNum+1):
        query = eval(lines[i])


    db.endConnection(conn)
    fin.close()
    fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])