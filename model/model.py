import copy
import networkx as nx
from networkx.classes import Graph

from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.classifications = []
        self.idClassifications = {}
        self.percorso = []
        self.elementi = 0

    def get_localizations(self):
        return DAO.get_localizations()

    def crea_grafo(self, loc):
        self._grafo.clear()
        self.classifications = DAO.get_classifications(loc)
        for c in self.classifications:
            self.idClassifications[c.GeneID] = c
        self._grafo.add_nodes_from(self.classifications)

        edges = DAO.get_interactions(self.idClassifications, loc)
        self._grafo.add_edges_from(edges)

        cromosomi = DAO.get_chromosomes()

        archi = []

        for e in self._grafo.edges:
            c0 = cromosomi[e[0].GeneID]
            c1 = cromosomi[e[1].GeneID]
            w = 0
            if c0 == c1:
                w = c0
            else:
                w = c0 + c1

            self._grafo[e[0]][e[1]]["weight"] = w
            archi.append((e[0], e[1], w))

        archi.sort(key = lambda x:x[2])
        return archi

    def comp_connesse(self):
        comp = list(nx.connected_components(self._grafo))
        print(comp)
        return sorted(comp, key=lambda x:len(x), reverse=True)

    def cerca_percorso(self):
        self.percorso = []
        self.elementi = 0

        essential = [n for n in self._grafo.nodes if n.Essential == "Essential"]
        non_essential = [n for n in self._grafo.nodes if n.Essential == "Non-Essential"]

        self.ricorsione([], essential)
        self.ricorsione([], non_essential)


        return sorted(self.percorso, key=lambda x:x.GeneID)


    def ricorsione(self, parziale, lista):
        if len(parziale) > self.elementi:
            self.elementi = len(parziale)
            self.percorso = copy.deepcopy(parziale)
        elif len(parziale) == self.elementi:
            sottografo_parziale = self._grafo.subgraph(parziale)
            sottografo = self._grafo.subgraph(self.percorso)
            if nx.number_connected_components(sottografo_parziale) < nx.number_connected_components(sottografo):
                self.elementi = len(parziale)
                self.percorso = copy.deepcopy(parziale)

        for n in lista:
            if len(parziale) == 0 or n.GeneID > parziale[-1].GeneID:
                parziale.append(n)
                self.ricorsione(parziale, lista)
                parziale.pop()



    def dim_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)