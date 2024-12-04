import os
import tkinter as tk
from tkinter import ttk, Menu
import threading
import queue
import time

from applications.spectraapp import Spectra_View_Window


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("800x600+0+0")
        if os.name == 'nt':
            self.state('zoomed')
        elif os.name == "posix":
            self.attributes('-zoomed', True)

        self.thread_queue = queue.Queue()
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # Create the menu bar
        menu_bar = Menu(self)

        # Stars menu with submenus, separators, and hotkeys
        stars_menu = Menu(menu_bar, tearoff=0)
        stars_menu.add_command(label="&Add Star", command=self.add_star)  # Alt+A
        stars_menu.add_command(label="&Remove Star", command=self.remove_star)  # Alt+R
        stars_menu.add_separator()
        stars_menu.add_command(label="Star &Info", command=self.star_info)  # Alt+I
        menu_bar.add_cascade(label="&Stars", menu=stars_menu)  # Alt+S

        # Spectra menu with submenus and separators
        spectra_menu = Menu(menu_bar, tearoff=0)
        spectra_menu.add_command(label="&Load Spectra", command=self.load_spectra)  # Alt+L
        spectra_menu.add_command(label="&Analyze Spectra", command=self.analyze_spectra)  # Alt+A
        spectra_menu.add_separator()
        spectra_menu.add_command(label="Spectra &Settings", command=self.spectra_settings)  # Alt+S
        menu_bar.add_cascade(label="&Spectra", menu=spectra_menu)  # Alt+S

        # Photometry menu
        photometry_menu = Menu(menu_bar, tearoff=0)
        photometry_menu.add_command(label="&Load Photometry", command=self.load_photometry)  # Alt+L
        menu_bar.add_cascade(label="P&hotometry", menu=photometry_menu)  # Alt+H

        # SEDs menu
        seds_menu = Menu(menu_bar, tearoff=0)
        seds_menu.add_command(label="&Generate SEDs", command=self.generate_seds)  # Alt+G
        menu_bar.add_cascade(label="&SEDs", menu=seds_menu)  # Alt+S

        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="&About", command=self.show_about)  # Alt+A
        menu_bar.add_cascade(label="&Help", menu=help_menu)  # Alt+H

        # Set the menu bar
        self.config(menu=menu_bar)

    # Dummy methods for commands
    def add_star(self):
        print("Add Star selected")

    def remove_star(self):
        print("Remove Star selected")

    def star_info(self):
        print("Star Info selected")

    def load_spectra(self):
        print("Load Spectra selected")

    def analyze_spectra(self):
        print("Analyze Spectra selected")

    def spectra_settings(self):
        print("Spectra Settings selected")

    def load_photometry(self):
        print("Load Photometry selected")

    def generate_seds(self):
        print("Generate SEDs selected")

    def show_about(self):
        print("About selected")


    def create_widgets(self):
        # Example button to open another window
        open_button = ttk.Button(self, text="Open Window", command=self.open_window)
        open_button.pack(pady=10)

        # Example button to start a background process
        thread_button = ttk.Button(self, text="Start Process", command=self.start_thread)
        thread_button.pack(pady=10)

        # Label to update with thread result
        self.result_label = ttk.Label(self, text="Result: Waiting...")
        self.result_label.pack(pady=10)

        # Periodically check the thread queue
        self.after(100, self.process_queue)

    def open_window(self):
        new_window = Spectra_View_Window(self)
        new_window.grab_set()  # Optional: Makes the new window modal

    def start_thread(self):
        # Start a background thread
        thread = threading.Thread(target=self.background_task, args=(self.thread_queue,))
        thread.daemon = True
        thread.start()

    def background_task(self, q):
        # Simulate a long-running process
        time.sleep(5)
        q.put("Task Complete!")

    def process_queue(self):
        # Check if the thread has placed any results in the queue
        try:
            result = self.thread_queue.get_nowait()
            self.result_label.config(text=f"Result: {result}")
        except queue.Empty:
            pass

        self.after(16, self.process_queue)
