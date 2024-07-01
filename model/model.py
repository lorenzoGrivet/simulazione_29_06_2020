import copy
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.maxConto=0
        self.grafo=nx.Graph()
        self.idMap={}

    def getMesi(self):
        return DAO.getMesiDAO()

    def creaGrafo(self,minuti,mese):
        nodi = DAO.getNodi(mese)
        self.grafo.add_nodes_from(nodi)
        for a in nodi:
            self.idMap[a.MatchID]=a
        archi=DAO.getArchi(mese,minuti)
        for a in archi:
            self.grafo.add_edge(self.idMap[a[0]],self.idMap[a[1]],peso=a[2])

        pass

    def connessioniMax(self,minuti,mese):
        archiList= list(self.grafo.edges(data=True))
        archiOrd= sorted(archiList,key=lambda x: x[2]["peso"],reverse=True)
        max=archiOrd[0][2]["peso"]
        c=1
        for a in archiOrd[1:]:
            if a[2]["peso"]==max:
                c+=1
            else:
                return archiOrd[:c]

        pass


    def getDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getNodi(self):
        return list(self.grafo.nodes)

    def cammino(self,m1,m2):
        parziale=[m1]
        self.ricorsione(parziale,m1,m2)
        return self.solBest, self.maxConto
        pass

    def ricorsione(self, parziale, start, m2):
        print("*")
        succ= list(self.grafo.neighbors(start))
        ammissibili=self.getAmmissibili(parziale,succ,start)
        
        if self.isTerminale(m2,parziale):
            c=self.calcola(parziale)
            if c> self.maxConto:
                self.solBest=copy.deepcopy(parziale)
                self.maxConto=c
        else:
            for a in ammissibili:
                parziale.append(a)
                self.ricorsione(parziale,a,m2)
                parziale.pop()
        
        
        pass

    def getAmmissibili(self, parziale, succ, start):
        ammissibili=[]

        for a in succ:
            b=False


            if {start.TeamHomeID,start.TeamAwayID} == {a.TeamHomeID,a.TeamAwayID}:
                b=True
            else:

                if a in parziale:
                    b=True

            if b==False:
                ammissibili.append(a)

        return ammissibili
        pass

    def isTerminale(self, m2,parziale):
        if len(parziale)==0:
            return False
        if parziale[-1] == m2:
            return True
        pass

    def calcola(self, parziale):
        somma=0
        for i in range(len(parziale)-1):
            try:
                somma += self.grafo[parziale[i]][parziale[i+1]]["peso"]
            except KeyError:
                print()
        return somma
        pass