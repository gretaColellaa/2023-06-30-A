import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._teams = []
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._idMapT = {}



    def fillDD(self):
        teamsNames = []
        for t in self._model.fillteam():
            self._idMapT[t.ID] = t
            if t.name not in teamsNames:
                teamsNames.append(t.name)

        for t in sorted(teamsNames):
            self._view.ddteam.options.append(ft.dropdown.Option(t))



    def handle_graph(self, e):

        if self._view.ddteam.value:
            self._team = self._view.ddteam.value
            self._model.crea_grafo(self._team)

            #self.handle_ddyear()

        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getNumNodes()} nodi"
                                                          f" e {self._model.getNumEdges()} archi"))

        self._view.update_page()


    def handle_dettagli(self, e):
        try: int(self._view.ddyear.value)
        except: self._view.create_alert("Selezionare un anno")
        archi_ordinati = self._model.getDettagli(int(self._view.ddyear.value))
        for a in archi_ordinati:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]}<-->{a[1]} - {a[2]['weight']}"))

        self._view.update_page()



    def handle_simula(self, e):
        pass

    def handle_ddyear(self, e):

        years =self._model.fillyear(self._view.ddteam.value)

        for y in sorted(years):
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        self._view.update_page()



