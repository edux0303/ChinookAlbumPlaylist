import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0

    # ---------- PUNTO 1 ----------
    def buildGraph(self, minuti):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi(minuti)
        for n in self._nodes:
            self.idMap[n.AlbumId] = n

        self._grafo.add_nodes_from(self._nodes)

        for s1, s2 in DAO.getEdges():
            if s1 in self.idMap and s2 in self.idMap:
                self._grafo.add_edge(self.idMap[s1], self.idMap[s2])

    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getComponente(self, album):
        return nx.node_connected_component(self._grafo, album)

    def getDurata(self, album):
        totale = 0
        for a in self.getComponente(album):
            totale += a.durata
        return totale

    # ---------- PUNTO 2 ----------
    def getSetAlbum(self, a1, dTot):
        self._solBest = []
        self._pesoBest = 0
        if a1.durata > dTot:
            return [], 0

        candidati = []
        for a in self.getComponente(a1):
            if a != a1:
                candidati.append(a)
        candidati.sort(key=lambda x: x.durata)   # dal più corto al più lungo

        self._ricorsione([a1], a1.durata, candidati, 0, dTot)
        return self._solBest, self._pesoBest

    def _ricorsione(self, parziale, durataParziale, candidati, start, dTot):
        # 1) aggiorno la soluzione migliore (più album)
        if len(parziale) > len(self._solBest):
            self._solBest = list(parziale)       # COPIA!
            self._pesoBest = durataParziale

        # 2) potatura: quanti album posso ancora aggiungere al massimo?
        possibili = 0
        somma = durataParziale
        for j in range(start, len(candidati)):
            if somma + candidati[j].durata > dTot:
                break
            somma += candidati[j].durata
            possibili += 1
        if len(parziale) + possibili <= len(self._solBest):
            return

        # 3) provo ad aggiungere i candidati dopo 'start'
        for i in range(start, len(candidati)):
            c = candidati[i]
            if durataParziale + c.durata > dTot:
                break                            # i successivi sono più lunghi
            parziale.append(c)
            self._ricorsione(parziale, durataParziale + c.durata, candidati, i + 1, dTot)
            parziale.pop()                       # backtracking