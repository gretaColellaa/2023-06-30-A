import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        year = self._model.getYear()
        for y in year:
            self._view.ddyear.options.append(ft.dropdown.Option(f"{y}"))

    def fillShape(self, e):
        year = self._view.ddyear.value
        forme = self._model.getShape(int(year))
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f"{f}"))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        self._model.buildGraph(year, shape)
        nNodes, nEdges = self._model.getCaratteristicheGrafo()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi e {nEdges} archi"))
        dizionario = self._model.getPesoAdiacenti()
        for key, value in dizionario.items():
            self._view.txt_result.controls.append(ft.Text(f"Nodo {key} somma pesi su archi={value}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        cammino_migliore, peso_tot = self._model.getBestPath()
        self._view.txtOut2.controls.append(ft.Text(f"il cammino massimo ha peso {peso_tot}"))
        for o in range(len(cammino_migliore)-1):
           self._view.txtOut2.controls.append(ft.Text(f"{cammino_migliore[o]}--{cammino_migliore[o+1]}"))
        self._view.update_page()
