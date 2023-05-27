import tkinter as tk
from tkinter import ttk

from Addons import Song
import pygame
from PIL import Image, ImageTk
from DSFactory import Factory
from DSnest import LinkedList
from Users import User


class HomePlayer:
    def __init__(self, factory: Factory, user: User):
        self.window = tk.Tk()
        self.window.title("Home Player")

        self.factory = factory
        self.user = user

        # Initialize Widgets
        self.search_bar = SearchBar(self.window)
        self.search_bar.pack(pady=5)

        self.song_row_scroller = VerticalScrollPane(self.window, 300, 400, )
        for i in range(0, 5):
            aux = HorizontalScrollPane(self.song_row_scroller, self.song_row_scroller.winfo_width()-10, 60)
            aux.pack(padx=5, pady=10)
        self.song_row_scroller.pack()

        self.control_bar = ControlBar(self.window, user.get_song_list())
        self.control_bar.pack(pady=5)

        self.window.mainloop()


class SongDisplay(tk.Frame):
    def __init__(self, song: Song, master):
        super().__init__(master)
        self.song = song
        self.__open_image()

    def __open_image(self):
        self.image = Image.open(self.song.get_cover_path())
        self.image_label = tk.Label(self)
        self.image_label.pack()
        tk_image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image


class HorizontalScrollPane(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.frame.bind("<Configure>", self._configure_canvas)

        # Disable resizing of scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _configure_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class VerticalScrollPane(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.frame.bind("<Configure>", self._configure_canvas)

        # Disable resizing of scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _configure_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class SearchBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.search_type_checkbox = tk.Checkbutton(self, text="AND Search")
        self.search_type_checkbox.grid(row=0, column=0, padx=10, pady=2)
        self.search_bar_entry = tk.Entry(self)
        self.search_bar_entry.grid(row=0, column=1, padx=10, pady=2)
        self.search_button = tk.Button(self, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2, padx=10, pady=2)

    def search(self):
        print('searching:', self.search_bar_entry.get())


class ControlBar(tk.Frame):
    def __init__(self, master, mix):
        super().__init__(master)
        # Initialize Widgets
        self.play_button = tk.Button(self, text="Prev", command=self.prev_song)
        self.play_button.grid(row=1, column=0, pady=5, padx=10)

        self.play_button = tk.Button(self, text="Play", command=self.toggle_playback)
        self.play_button.grid(row=1, column=1, pady=5, padx=10)

        self.play_button = tk.Button(self, text="Next", command=self.next_song)
        self.play_button.grid(row=1, column=2, pady=5, padx=10)

        self.progress_bar = ProgressBar(self, 200, 20, 0)
        self.progress_bar.grid(row=0, columnspan=3, pady=5, padx=10)

        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_mix = mix
        self.current_song = None
        self.paused = False
        self.playing = False

        # Initialize variables
        if not self.current_mix.is_empty():
            self.current_song = self.current_mix.get(0)

    def toggle_playback(self):
        if self.current_song:
            if not self.playing:
                pygame.mixer.music.load(self.current_song.get_audio_path())
                pygame.mixer.music.play()
                self.playing = True
                self.paused = False
                self.play_button.configure(text="Pause")
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.play_button.configure(text="Pause")
            else:
                pygame.mixer.music.pause()
                self.paused = True
                self.play_button.configure(text="Play")

    def play_from_timestamp(self, timestamp):
        if self.current_song:
            pygame.mixer.music.load(self.current_song.get_audio_path())
            pygame.mixer.music.play(start=timestamp)
            self.playing = True
            self.paused = False

    def next_song(self):
        try:
            index = self.current_mix.index_of(self.current_song)
            if self.current_mix.valid_index(index + 1):
                self.current_song = self.current_mix.get(index + 1)
            else:
                self.current_song = self.current_mix.get(0)
            self.playing = True
            self.paused = False
            self.toggle_playback()
        except IndexError:
            print("No next song found")

    def prev_song(self):
        try:
            index = self.current_mix.index_of(self.current_song)
            if self.current_mix.valid_index(index - 1):
                self.current_song = self.current_mix.get(index - 1)
            else:
                self.current_song = self.current_mix.get(self.current_mix.size() - 1)
            self.playing = True
            self.paused = False
            self.toggle_playback()
        except IndexError:
            print("No prev song found")


class ProgressBar(tk.Canvas):
    def __init__(self, parent, width, height, progress=0):
        super().__init__(parent, width=width, height=height, bg='white', relief='sunken', bd=1)

        self.progress = progress
        self.dragging = False

        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag_progress)
        self.bind("<ButtonRelease-1>", self.end_drag)

        self.update_progress()

    def start_drag(self, event):
        self.dragging = True
        self.drag_progress(event)

    def drag_progress(self, event):
        if self.dragging:
            x = event.x / self.winfo_width()
            self.progress = max(0, min(1, x))
            self.update_progress()

    def end_drag(self, event):
        self.dragging = False
        print(self.progress)

    def update_progress(self):
        self.delete('progress')
        width = self.winfo_width() * self.progress
        self.create_rectangle(0, 0, width, self.winfo_height(), fill='blue', tags='progress')


    def get_progress(self):
        return self.progress
