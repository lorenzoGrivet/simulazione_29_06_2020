import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.m2 = None
        self.m1 = None
        self.selectedMese = None
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model


    def fillDD(self):
        mesi=self.model.getMesi()
        mesiDD=list(map(lambda x: ft.dropdown.Option(key=x,on_click=self.getSelectedMese),mesi))
        self.view.ddMese.options=mesiDD
        self.view.update_page()

    def fillDDRicorsione(self):
        nodi=self.model.getNodi()
        nodiDD1= list(map(lambda x: ft.dropdown.Option(key=x,data=x,on_click=self.getSelectedMatch1),nodi))
        nodiDD2=list(map(lambda x: ft.dropdown.Option(key=x,data=x,on_click=self.getSelectedMatch2),nodi))
        self.view.ddM1.options=nodiDD1
        self.view.ddM2.options=nodiDD2
        self.view.update_page()



    def handleCreaGrafo(self, e):

        if self.view.txtMinuti=="":
            self.view.create_alert("Inserire minuti")
        if self.selectedMese is None:
            self.view.create_alert("Inserire mese")

        try:
            intMinuti=int(self.view.txtMinuti.value)
        except ValueError:
            self.view.create_alert("inserire numero")
            return

        self.model.creaGrafo(intMinuti,self.selectedMese)
        n,a = self.model.getDetails()
        self.view.txtGrafo.controls.append(ft.Text(f"Nodi: {n}. Archi: {a}"))
        self.view.update_page()
        self.fillDDRicorsione()
        pass


    def handleConnessioneMax(self, e):
        if self.view.txtMinuti=="":
            self.view.create_alert("Inserire minuti")

        try:
            intMinuti=int(self.view.txtMinuti.value)
        except ValueError:
            self.view.create_alert("inserire numero")
            return

        res=self.model.connessioniMax(intMinuti,self.selectedMese)
        for a in res:
            self.view.txtConnessione.controls.append(ft.Text(f"{a[0]} -- {a[1]}, peso: {a[2]["peso"]}"))
        self.view.update_page()

        pass

    def handleCollegamento(self, e):
        if self.m1 is None or self.m2 is None:
            self.view.create_alert("Inserire match")
        res, peso=self.model.cammino(self.m1,self.m2)
        self.view.txtCollegamento.controls.append(ft.Text(f"Peso: {peso}"))
        for a in res:
            self.view.txtCollegamento.controls.append(ft.Text(f"{a}"))
        self.view.update_page()
        pass
    
    
    def getSelectedMese(self,e):
        if e.control.key is None:
            pass
        else:
            self.selectedMese=e.control.key

    def getSelectedMatch1(self,e):
        if e.control.data is None:
            pass
        else:
            self.m1=e.control.data

    def getSelectedMatch2(self,e):
        if e.control.data is None:
            pass
        else:
            self.m2=e.control.data


           