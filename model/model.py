import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._edges = []
        self._years = []
        self._teams = []
        self._grafo = nx.Graph()
        self._idMapGiocatori = {}


    def fillteam(self):
        self._teams = DAO.getTeams()
        return self._teams

    def fillyear(self, teamName):
        self._years.clear()
        self._idMapGiocatori.clear()
        years_players  = DAO.getYears(teamName)
        for y in years_players:
            if y[0] in self._idMapGiocatori.keys():
                self._idMapGiocatori[y[0]].append(y[1])
            else:
                self._idMapGiocatori[y[0]] = [y[1]]

        self._years = self._idMapGiocatori.keys()

        return self._years


    def crea_grafo(self, team):
        self._grafo.clear()
        self._edges.clear()
        self._grafo.add_nodes_from(self._years)

        for i in self._years:
            for j in self._years:
                if (i,j) not in self._edges and (j,i) not in self._edges and i!=j:

                    peso = DAO.getPesoEdges(i,j, team)
                    self._edges.append((i,j,{'weight': peso}))

        self._grafo.add_edges_from(self._edges)


    def getDettagli(self, year):
        vicini = self._grafo.neighbors(year)
        archi = []
        for v in vicini:
            archi.append((year, v, self._grafo.get_edge_data(year, v)))

        archi_ordinati = sorted(archi, key=lambda x: x[2]['weight'], reverse=True)

        return archi_ordinati
    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
