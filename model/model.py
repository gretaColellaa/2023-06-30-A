import geopy.distance
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.shapes = set()
        self._grafo = nx.Graph()
        self.nodes = []
        self.dizionarioAdiacenti={}
        self._bestObjVal = 0

    def buildGraph(self, year, shape):
        self._grafo.clear()
        self.nodes = DAO.getAllNodes()
        for n in self.nodes:
            self._grafo.add_node(n)
        self.addEdgesPesati(year, shape)

    def addEdgesPesati(self, year, shape):
        archi = DAO.getArchi()
        for n1, n2 in archi:
            if self._grafo.has_edge(n1, n2) is False:
                peso = DAO.getPesoArchi(n1, n2, year, shape)
                self._grafo.add_edge(n1, n2, weight=peso[0])

    def getPesoAdiacenti(self):
        self.dizionarioAdiacenti={}
        for a in self._grafo.nodes:
            peso = 0
            vicini = self._grafo.neighbors(a)
            for v in vicini:
                peso += self._grafo[a][v]['weight']
            self.dizionarioAdiacenti[a] = peso
        return self.dizionarioAdiacenti

    def getDistance(self, a, b):
        return self.getDistanceBetweenPointsNew(a.Lat, a.Lng, b.Lat, b.Lng)

    def searchPath(self):

        for nodo in self._grafo.nodes:
            parziale = []
            self.ricorsione(nodo, parziale)
        return self._bestPath, self._bestObjVal

    def ricorsione(self, n, parziale):
        archiViciniAmmissibili = self.getArchiViciniAmm(n, parziale)

        if len(archiViciniAmmissibili) == 0:
            if self._getMaxDistance(parziale) > self._bestObjVal:
                self._bestPath = copy.deepcopy(parziale)
                self._bestObjVal = self._getMaxDistance(parziale)

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsione(a[1], parziale)
            parziale.pop()

    def getArchiViciniAmm(self, nodoLast, parziale):
        archiVicini = self._grafo.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:

            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):
        if len(parziale) == 0:
            return True
        return e[2]["weight"] > parziale[-1][2]["weight"]

    def isNovel(self, e, parziale):
        if len(parziale) == 0:
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)

    def _getMaxDistance(self, listOfNodes):

        if len(listOfNodes) == 1:
            return 0

        maxDistance = 0
        for i in range(0, len(listOfNodes)):
            maxDistance += self.getDistance(listOfNodes[i][0], listOfNodes[i][1])
        return maxDistance

    def getDistanceBetweenPointsNew(self, latitude1, longitude1, latitude2, longitude2):
        punto1 = (latitude1, longitude1)
        punto2 = (latitude2, longitude2)
        distanza = geopy.distance.distance(punto1, punto2).km
        return distanza

    def getYear(self):
        anni = DAO.getYear()
        ins_anni = set()
        for a in anni:
            ins_anni.add(a)
        return ins_anni

    def getShape(self, year):
        self.shapes = set()
        forme = DAO.getAllShape(year)
        for s in forme:
            self.shapes.add(s)
        return self.shapes

    def getCaratteristicheGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
