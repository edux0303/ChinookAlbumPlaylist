import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TdP - Album e playlist"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self.txt_result = None

    def load_interface(self):
        self._page.controls.append(
            ft.Text("TdP - Chinook: album e playlist", color="blue", size=24))

        # ---------- RIGA 1: durata + crea grafo (1a, 1b) ----------
        self._txtDurata = ft.TextField(label="Durata (minuti)", width=250)
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo, width=250)
        row1 = ft.Row([self._txtDurata, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ---------- RIGA 2: album + analisi componente (1c) ----------
        self._ddAlbum = ft.Dropdown(label="Album", width=250)
        self._btnComponente = ft.ElevatedButton(text="Analisi componente",
                                                on_click=self._controller.handleComponente, width=250)
        row2 = ft.Row([self._ddAlbum, self._btnComponente],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ---------- RIGA 3: durata massima + set di album (2) ----------
        self._txtDTOT = ft.TextField(label="dTOT (minuti)", width=250)
        self._btnSetAlbum = ft.ElevatedButton(text="Set di album",
                                              on_click=self._controller.handleSetAlbum, width=250)
        row3 = ft.Row([self._txtDTOT, self._btnSetAlbum],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)

        # ---------- area risultati ----------
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()