import networkx as nx
import random
from database.DAO import DAO


class Model:
    def __init__(self):
        self._year = None
        self._edges = []
        self._years = []
        self._teams = []
        self._grafo = nx.Graph()
        self._idMapGiocatori = {}
        self._idMapTifosi = {}


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
        self._year = year
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

    def simula(self, T):

        anni = []
        for a in self._years:
            if a > self._year:
                anni.append(a)

        t = 1
        while t in range(1, T):
            for g in self._idMapGiocatori[self._year]:
                if g in self._idMapTifosi.keys():
                    self._idMapTifosi[f"t{t}"].append(g)
                else:
                    self._idMapTifosi[f"t{t}"] = [g]
                t += 1

        self.ricorsione(anni, self._idMapTifosi.keys())

        return self._idMapTifosi




    def ricorsione(self, parziale, fans):
        if len(parziale) == 1:
            return


        else:
            for g in self._idMapGiocatori[parziale[1]]:
                tifosi = []
                #tifosi_casuali = []
                for f in fans:
                    if g in self._idMapTifosi[f]:
                        tifosi.append(f)
                if tifosi != [] :
                    if g in  self._idMapGiocatori[parziale[1]] and g in self._idMapGiocatori[parziale[0]]:
                        change = int(len(tifosi) * 10 / 100)
                        tifosi_casuali = random.sample(tifosi, change)
                        for t in tifosi_casuali:
                            giocatore = random.sample(self._idMapGiocatori[parziale[1]].items(), 1)
                            while giocatore == g:
                                giocatore = random.sample(self._idMapGiocatori[parziale[1]].items(), 1)
                            self._idMapTifosi[t] = giocatore

                    else:
                        change = int(len(tifosi) * 90 / 100)
                        tifosi_casuali = random.sample(tifosi, change)
                        for t in tifosi_casuali:
                            giocatore = random.sample(self._idMapGiocatori[parziale[1]].items(), 1)
                            while giocatore == g:
                                giocatore = random.sample(self._idMapGiocatori[parziale[1]].items(), 1)
                            self._idMapTifosi[t] = giocatore

                        for t in tifosi:
                            if t not in tifosi_casuali:
                                list(fans).remove(t)

            self.ricorsione(parziale[1::],fans)





