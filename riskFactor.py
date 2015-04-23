from __future__ import division
import sys,getopt
import db
import copy

class Vertex:

    def __init__(self,name):
        self.name = name
        self.connection = []

    def addConnection(self,node):
        self.connection.append(node)

    def removeConnection(self,node):
        self.connection.remove(node)

    def getName(self):
        return self.name

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


def initGraph():
    dag = Graph()
    nodes = []
    #topological sort
    nodes.append(Vertex('diabetes'))
    nodes.append(Vertex('stroke'))
    nodes.append(Vertex('attack'))
    nodes.append(Vertex('angina'))
    nodes.append(Vertex('bmi'))
    nodes.append(Vertex('bp'))
    nodes.append(Vertex('cholesterol'))
    nodes.append(Vertex('exercise'))
    nodes.append(Vertex('smoke'))
    nodes.append(Vertex('income'))
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

def main(argv):
    inputFile = ""
    dataFile = ""
    dbFile = "riskData.db"
    outputFile = "riskFactor_output.txt"

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


    fin.close()
    fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])