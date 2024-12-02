import tkinter as tk
from tkinter import ttk
import threading
import queue
import time


class Spectra_View_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Secondary Window")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="This is a secondary window").pack(pady=10)
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10)
