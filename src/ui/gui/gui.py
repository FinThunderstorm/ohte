from tkinter import Tk, ttk
from utils.helpers import get_window_size


class GUI:
    def __init__(self, window):
        self.__window = window

    def start(self):
        label = ttk.Label(master=self.__window, text="Muistio")
        label.pack()


window = Tk()
window_size = get_window_size(window)
window.geometry(window_size)
window.title("Muistio")

gui = GUI(window)
gui.start()

window.mainloop()
