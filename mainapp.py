import os
import tkinter as tk
from tkinter import ttk
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
        self.create_widgets()

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
