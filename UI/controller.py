import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        loc = self._view.dd_localization.value
        if loc is None or loc == "":
            self._view.txt_result.controls.append(ft.Text("Selezionare una localizzazione", color="red"))
            self._view.update_page()
            return
        archi = self._model.crea_grafo(loc)
        n, m = self._model.dim_grafo()
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {n} nodi e {m} archi", color="green"))

        for a in archi:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} <-> {a[1]}: peso {a[2]}"))
        self._view.btn_path.disabled=False
        self._view.update_page()

    def analyze_graph(self, e):
        comp = self._model.comp_connesse()
        self._view.txt_result.controls.append(ft.Text("Le componeti connesse sono:", color = "green"))

        for c in comp:
            if len(c) > 1:
                res = ""
                for el in c:
                    res += f"{el}, "
                res += f"| dimensione componente = {len(c)}"
                self._view.txt_result.controls.append(ft.Text(res))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result.controls.clear()

        percorso = self._model.cerca_percorso()

        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{n} -> {n.Essential}", color="green"))

        self._view.update_page()

    def fill_localizations(self):
        loc = self._model.get_localizations()
        for l in loc:
            self._view.dd_localization.options.append(ft.dropdown.Option(l))

