import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # ---------- PUNTO 1a/1b ----------
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        durata = self._view._txtDurata.value
        if durata is None or durata == "":
            self._errore("Inserire una durata in minuti!")
            return
        try:
            durata = float(durata)
        except ValueError:
            self._errore("La durata deve essere un numero!")
            return
        if durata <= 0:
            self._errore("La durata deve essere maggiore di 0!")
            return

        self._model.buildGraph(durata)

        self._view.txt_result.controls.append(ft.Text(f"Grafo creato per la durata {durata}!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddAlbum.options.clear()
        self._view._ddAlbum.value = None
        for a in sorted(self._model.getNodes(), key=lambda x: x.Title):
            self._view._ddAlbum.options.append(ft.dropdown.Option(key=str(a.AlbumId), text=a.Title))
        self._view.update_page()

    # ---------- PUNTO 1c ----------
    def handleComponente(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return
        if self._view._ddAlbum.value is None:
            self._errore("Selezionare un album!")
            return

        album = self._model.idMap.get(int(self._view._ddAlbum.value))
        if album is None:
            self._errore("Album non trovato!")
            return

        componente = self._model.getComponente(album)
        durataTot = self._model.getDurata(album)

        self._view.txt_result.controls.append(
            ft.Text(f"La componente di '{album.Title}' contiene {len(componente)} album"))
        self._view.txt_result.controls.append(
            ft.Text(f"Durata complessiva: {durataTot:.2f} minuti"))
        self._view.update_page()

    # ---------- PUNTO 2 ----------
    def handleSetAlbum(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return
        if self._view._ddAlbum.value is None:
            self._errore("Selezionare un album!")
            return

        a1 = self._model.idMap.get(int(self._view._ddAlbum.value))
        if a1 is None:
            self._errore("Album non trovato!")
            return

        dTot = self._view._txtDTOT.value
        if dTot is None or dTot == "":
            self._errore("Inserire dTOT!")
            return
        try:
            dTot = float(dTot)
        except ValueError:
            self._errore("dTOT deve essere un numero!")
            return

        soluzione, durataTot = self._model.getSetAlbum(a1, dTot)
        if len(soluzione) == 0:
            self._errore(f"'{a1.Title}' da solo dura {a1.durata:.2f} minuti, più di dTOT!")
            return

        self._view.txt_result.controls.append(ft.Text("Set di album trovato:"))
        for a in soluzione:
            self._view.txt_result.controls.append(ft.Text(f"{a.Title} - {a.durata:.2f} minuti"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di album: {len(soluzione)}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata totale: {durataTot:.2f} minuti"))
        self._view.update_page()