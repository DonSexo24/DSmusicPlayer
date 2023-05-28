import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from Addons import Song, get_all_filtered_songs, Tag, get_any_filtered_songs
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
        self.current_song_list = self.user.get_song_list()  # Initial song list to display

        # Initialize Widgets
        self.search_bar = SearchBar(self.window, self)
        self.search_bar.pack(pady=5)

        self.song_row_scroller = VerticalScrollPane(self.window, 300)

        # Create SongDisplay instances for the initial song list
        if not self.current_song_list.is_empty():
            for song in self.current_song_list:
                song_box = SongDisplay(self.song_row_scroller.frame, song, self.toggle_song_in_user_list)
                is_in_user_list = song in self.user.get_song_list()
                song_box.set_toggle_button_state(is_in_user_list)
                song_box.pack(pady=10)
        else:
            self.current_song_list = self.factory.get_songs()
            for song in self.current_song_list:
                song_box = SongDisplay(self.song_row_scroller.frame, song, self.toggle_song_in_user_list)
                song_box.set_toggle_button_state(False)
                song_box.pack(pady=10)

        self.song_row_scroller.pack()

        self.control_bar = ControlBar(self.window, self.user.get_song_list(), self.toggle_song_in_user_list)
        self.control_bar.pack(pady=30)

        self.search_bar.show_home_songs()

        self.window.mainloop()

    def switch_song_list(self, new_song_list):
        self.current_song_list = new_song_list
        self.song_row_scroller.frame.destroy()

        self.song_row_scroller.frame = tk.Frame(self.song_row_scroller.canvas)
        self.song_row_scroller.canvas.create_window((0, 0), window=self.song_row_scroller.frame, anchor='nw')

        # Create SongDisplay instances for the new song list
        if not self.current_song_list.is_empty():
            for song in self.current_song_list:
                song_box = SongDisplay(self.song_row_scroller.frame, song, self.toggle_song_in_user_list)
                is_in_user_list = self.user.get_song_list().contains(song)
                song_box.set_toggle_button_state(is_in_user_list)
                song_box.pack(pady=10)
        else:
            self.current_song_list = self.factory.get_songs()
            for song in self.current_song_list:
                song_box = SongDisplay(self.song_row_scroller.frame, song, self.toggle_song_in_user_list)
                song_box.set_toggle_button_state(False)
                song_box.pack(pady=10)

        self.song_row_scroller.frame.bind("<Configure>", self.song_row_scroller._configure_canvas)
        self.song_row_scroller.canvas.configure(scrollregion=self.song_row_scroller.canvas.bbox("all"))

        self.control_bar.update_song_info()
        # Update the song information in the control bar

    def toggle_song_in_user_list(self, song):
        if self.user.get_song_list().contains(song):
            self.factory.remove_user_song(self.user, song)
        else:
            self.factory.add_user_song(self.user, song)
        self.save_Factory()
        self.switch_song_list(self.current_song_list)

    def load_Factory(self):
        try:
            with open(r"C:\Users\Samuel\PycharmProjects\DSmusicPlayer\factory.pkl", "rb") as archivo:
                self.factory = pickle.load(archivo)
        except FileNotFoundError:
            print("El archivo no se encuentra.")
            self.save_Factory()
        except pickle.UnpicklingError:
            print("Error al deserializar el objeto.")
            self.save_Factory()

    def save_Factory(self):
        factory_aux = pickle.dumps(self.factory)
        with open(r"C:\Users\Samuel\PycharmProjects\DSmusicPlayer\factory.pkl", "wb") as archivo:
            archivo.write(factory_aux)


class SongDisplay(tk.Frame):
    def __init__(self, master, song: Song, toggle_callback):
        super().__init__(master)
        self.song = song
        self.configure(borderwidth=1, relief='solid')  # Add border configuration
        self.__open_image()
        self.__create_labels()
        self.__create_toggle_button(toggle_callback)

    def __open_image(self):
        image = Image.open(self.song.get_cover_path())
        width, height = image.size
        new_width = 150
        ratio = new_width / width
        new_height = int(height * ratio)

        # Resize the image while preserving the aspect ratio
        self.image = image.resize((new_width, new_height), Image.ANTIALIAS)

        self.image_label = tk.Label(self)
        self.image_label.grid(row=0, column=0, rowspan=7, padx=(10,10))
        tk_image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def __create_labels(self):
        name_label = tk.Label(self, text=self.song.get_name())
        name_label.grid(row=1, column=1, padx=10)

        artist_label = tk.Label(self, text=self.song.get_artist().get_name())
        artist_label.grid(row=2, column=1, padx=10)

        album_label = tk.Label(self, text=self.song.get_album().name)
        album_label.grid(row=3, column=1, padx=10)

        genre_label = tk.Label(self, text=self.song.get_genre_name())
        genre_label.grid(row=4, column=1, padx=10)

        date_label = tk.Label(self, text=self.song.get_year())
        date_label.grid(row=5, column=1, padx=10)

    def __create_toggle_button(self, toggle_callback):
        self.toggle_button = tk.Button(self, text="❤", command=lambda: toggle_callback(self.song))
        self.toggle_button.grid(row=1, column=2, padx=(10, 10))

    def set_toggle_button_state(self, is_in_user_list):
        if is_in_user_list:
            self.toggle_button.configure(text="❤")
        else:
            self.toggle_button.configure(text="♡")


class VerticalScrollPane(tk.Frame):
    def __init__(self, parent, height):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, height=height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.frame_window = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.frame.bind("<Configure>", self._configure_canvas)

        # Disable resizing of scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _configure_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Calculate the vertical center position
        canvas_height = self.canvas.winfo_height()
        frame_height = self.frame.winfo_reqheight()
        y_offset = max((canvas_height - frame_height) // 2, 0)

        try:
            self.canvas.itemconfigure(self.frame_window, window=self.frame, anchor='nw', y=y_offset)
        except Exception:
            pass

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class SearchBar(tk.Frame):
    def __init__(self, master, home):
        super().__init__(master)
        self.home = home
        self.selected = tk.BooleanVar()
        self.search_type_checkbox = tk.Checkbutton(self, text="AND Search", variable=self.selected)
        self.search_type_checkbox.grid(row=0, column=0, padx=10, pady=2)
        self.search_bar_entry = tk.Entry(self)
        self.search_bar_entry.grid(row=0, column=1, padx=10, pady=2)
        self.search_button = tk.Button(self, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2, padx=10, pady=2)

        self.home_button = tk.Button(self, text="Home", command=self.show_home_songs)
        self.home_button.grid(row=0, column=3, padx=10, pady=2)

        self.favorites_button = tk.Button(self, text="My Favorites", command=self.show_user_songs)
        self.favorites_button.grid(row=0, column=4, padx=10, pady=2)

        self.label_text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.label_text)
        self.label.grid(row=1, column=0, columnspan=5, padx=10, pady=2)

    def search(self):
        query = self.search_bar_entry.get()
        keys = query.split(" ")
        tags = LinkedList[Tag]()
        for word in keys:
            print(word)
            tags.append(Tag(word))
        if self.selected.get():
            self.home.switch_song_list(get_all_filtered_songs(tags, self.home.factory.get_songs()))
            search_type = "AND"
        else:
            self.home.switch_song_list(get_any_filtered_songs(tags, self.home.factory.get_songs()))
            search_type = "OR"
        self.label_text.set(f"Results of: {query} ({search_type})")

    def show_home_songs(self):
        self.home.switch_song_list(self.home.factory.get_songs())
        self.label_text.set("Songs in: Home")

    def show_user_songs(self):
        self.home.switch_song_list(self.home.user.get_song_list())
        self.label_text.set("Songs in: My Favorites")


class ControlBar(tk.Frame):
    def __init__(self, master, mix, toggle_song_callback):
        super().__init__(master)
        # Initialize Widgets
        self.song_info_label = tk.Label(self, text="", font=("Arial", 12))
        self.song_info_label.grid(row=0, columnspan=3, pady=5, padx=10)

        self.song_image_label = tk.Label(self)
        self.song_image_label.grid(row=1, columnspan=3, pady=5, padx=10)

        self.prev_button = tk.Button(self, text="Prev", command=self.prev_song)
        self.prev_button.grid(row=2, column=0, pady=5, padx=10)

        self.play_button = tk.Button(self, text="Play", command=self.toggle_playback)
        self.play_button.grid(row=2, column=1, pady=5, padx=10)

        self.next_button = tk.Button(self, text="Next", command=self.next_song)
        self.next_button.grid(row=2, column=2, pady=5, padx=10)

        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.grid(row=3, columnspan=3, pady=5, padx=10)

        self.progress = 0
        self.length = 0

        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_mix = mix
        self.current_song = None
        self.paused = False
        self.playing = False
        self.aux_pos = 0
        self.flag = False

        # Initialize variables
        if not self.current_mix.is_empty():
            self.current_song = self.current_mix.get(0)
            self.length = pygame.mixer.Sound(self.current_song.get_audio_path()).get_length()
            self.progress_bar.configure(maximum=self.length)
            self.update_progress()
        else:
            self.flag = True

        self.toggle_song_callback = toggle_song_callback

        # Initialize song image
        self.song_image = None
        self.update_song_image()
        self.update_song_info()
        self.song_list_listener()

    def song_list_listener(self):
        if self.flag and not self.current_mix.is_empty():
            self.current_song = self.current_mix.get(0)
            self.length = pygame.mixer.Sound(self.current_song.get_audio_path()).get_length()
            self.progress_bar.configure(maximum=self.length)
            self.update_progress()
            self.update_song_info()
            self.update_song_image()
            self.flag = False
        self.check_user_song_list()
        self.after(50, self.song_list_listener)

    def toggle_song_in_user_list(self, song):
        self.toggle_song_callback(song)
        self.check_user_song_list()

    def update_progress(self):
        if self.playing:
            self.progress = pygame.mixer.music.get_pos() / 1000
            if self.progress >= self.length:
                self.progress = 0
                self.next_song()
        self.progress_bar['value'] = self.progress
        self.after(50, self.update_progress)

    def update_song_info(self):
        if self.current_song:
            song_info = f"Song: {self.current_song.get_name()} | Artist: {self.current_song.get_artists().get_name()} | Album: {self.current_song.get_album().name}"
            self.song_info_label.configure(text=song_info)
        else:
            self.song_info_label.configure(text="No song selected")

    def update_song_image(self):
        if self.current_song:
            image_path = self.current_song.get_cover_path()
            if image_path:
                image = Image.open(image_path)
                width, height = image.size
                new_width = 75
                ratio = new_width / width
                new_height = int(height * ratio)

                # Resize the image while preserving the aspect ratio
                image = image.resize((new_width, new_height), Image.ANTIALIAS)
                self.song_image = ImageTk.PhotoImage(image)
                self.song_image_label.configure(image=self.song_image)
                self.song_image_label.image = self.song_image
            else:
                self.song_image_label.configure(image=None)
        else:
            self.song_image_label.configure(image=None)

    def toggle_playback(self):
        if self.current_song:
            if not self.playing:
                pygame.mixer.music.load(self.current_song.get_audio_path())
                pygame.mixer.music.play(start=self.aux_pos)
                self.playing = True
                self.paused = False
            else:
                if self.paused:
                    pygame.mixer.music.unpause()
                    self.paused = False
                else:
                    pygame.mixer.music.pause()
                    self.paused = True
        else:
            messagebox.showwarning("No Song", "No song selected.")

    def prev_song(self):
        if self.current_song:
            index = self.current_mix.index_of(self.current_song)
            if self.current_mix.valid_index(index - 1):
                self.current_song = self.current_mix.get(index - 1)
            else:
                self.current_song = self.current_mix.get(self.current_mix.size()-1)
            self.aux_pos = 0
            self.update_song_info()
            self.update_song_image()
            self.playing = False
            self.paused = False
            self.toggle_playback()
        else:
            messagebox.showwarning("No Song", "No song selected.")

    def next_song(self):
        if self.current_song:
            index = self.current_mix.index_of(self.current_song)
            if self.current_mix.valid_index(index + 1):
                self.current_song = self.current_mix.get(index + 1)
            else:
                self.current_song = self.current_mix.get(0)
            self.aux_pos = 0
            self.update_song_info()
            self.update_song_image()
            self.playing = False
            self.paused = False
            self.toggle_playback()
        else:
            messagebox.showwarning("No Song", "No song selected.")

    def check_user_song_list(self):
        if self.current_mix.is_empty():
            self.current_song = None
            self.length = 0
            self.progress_bar.configure(maximum=self.length)
            self.update_progress()
            self.update_song_info()
            self.update_song_image()
            self.playing = False
            self.paused = False
