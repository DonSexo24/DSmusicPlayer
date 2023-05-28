import tkinter as tk

class AdminHome:
    def __init__(self, factory):
        self.window = tk.Tk()
        self.window.title("Admin Screen")

        self.factory = factory

        self.artist_crud_button = tk.Button(self, text="Artist", command=self.go_to_artist_crud)

    def go_to_artist_crud(self, factory):
        self.window.destroy()


class TextIn(tk.Frame):
    def __init__(self, master, key: str):
        super().__init__(master)
        self.label = tk.Label(self, text=key+": ")
        self.label.pack(side=tk.LEFT)
        self.field = tk.Entry(self)
        self.field.pack(side=tk.LEFT)