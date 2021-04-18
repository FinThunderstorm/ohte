from tkinter import ttk


class MemoView:
    def __init__(self, window, handles):
        self.__window = window
        self.__handles = handles
        self.__frame = None

    def _initialize(self):
        self._frame = ttk.Frame(master=self.__window)
