import os
import pickle

from Addons import Artist, Album, Song
from DSFactory import Factory
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk


class AdminView:
    def __init__(self, factory: Factory):
        self.factory = factory
        self.window = tk.Tk()
        self.window.title("Admin View")

        # Artist section
        artist_frame = tk.Frame(self.window)
        artist_frame.pack(pady=10)

        tk.Label(artist_frame, text="Select Artist:").grid(row=0, column=0, sticky=tk.W)
        self.artist_spinner = ttk.Combobox(artist_frame, values=list(self.factory.get_artist_codes()), width=10)
        self.artist_spinner.bind("<<ComboboxSelected>>", self.update_artist_info)
        self.artist_spinner.grid(row=0, column=1)

        tk.Button(artist_frame, text="Clear Selection", command=self.clear_artist_selection).grid(row=0, column=2)

        tk.Label(artist_frame, text="Name:").grid(row=1, column=0, sticky=tk.W)
        self.artist_name_label = tk.Label(artist_frame, text="")
        self.artist_name_label.grid(row=1, column=1, sticky=tk.W)

        tk.Label(artist_frame, text="Country:").grid(row=2, column=0, sticky=tk.W)
        self.artist_country_label = tk.Label(artist_frame, text="")
        self.artist_country_label.grid(row=2, column=1, sticky=tk.W)

        tk.Label(artist_frame, text="Is Group:").grid(row=3, column=0, sticky=tk.W)
        self.artist_is_group_label = tk.Label(artist_frame, text="")
        self.artist_is_group_label.grid(row=3, column=1, sticky=tk.W)

        tk.Button(artist_frame, text="Add Artist", command=self.add_artist_popup).grid(row=4, column=0)
        tk.Button(artist_frame, text="Update Artist", command=self.update_artist_popup).grid(row=4, column=1)
        tk.Button(artist_frame, text="Delete Artist", command=self.delete_artist).grid(row=4, column=2)

        # Album section
        album_frame = tk.Frame(self.window)
        album_frame.pack(pady=10)

        tk.Label(album_frame, text="Select Album:").grid(row=0, column=0, sticky=tk.W)
        self.album_spinner = ttk.Combobox(album_frame, values=[], width=20)
        self.album_spinner.bind("<<ComboboxSelected>>", self.update_album_info)
        self.album_spinner.grid(row=0, column=1)

        tk.Button(album_frame, text="Add Album", command=self.add_album_popup).grid(row=1, column=0)
        tk.Button(album_frame, text="Update Album", command=self.update_album_popup).grid(row=1, column=1)
        tk.Button(album_frame, text="Delete Album", command=self.delete_album).grid(row=1, column=2)

        # Song section
        song_frame = tk.Frame(self.window)
        song_frame.pack(pady=10)

        tk.Label(song_frame, text="Select Song:").grid(row=0, column=0, sticky=tk.W)
        self.song_spinner = ttk.Combobox(song_frame, values=[], width=20)
        self.song_spinner.grid(row=0, column=1)

        tk.Button(song_frame, text="Add Song", command=self.add_song_popup).grid(row=1, column=0)
        tk.Button(song_frame, text="Update Song", command=self.update_song_popup).grid(row=1, column=1)
        tk.Button(song_frame, text="Delete Song", command=self.delete_song).grid(row=1, column=2)

        self.file_button = tk.Button(self.window, text="Load from File", command=self.open_file)
        self.file_button.pack(pady=10)

        self.window.mainloop()

    def update_artist_info(self, event):
        selected_artist = self.artist_spinner.get()
        artist = self.factory.get_artist_by_code(selected_artist)
        self.artist_name_label.config(text=artist.get_name())
        self.artist_country_label.config(text=artist.get_country())
        self.artist_is_group_label.config(text=str(artist.get_is_group()))
        self.album_spinner.config(values=list(artist.get_albums_names()))
        self.song_spinner['values'] = []

    def update_album_info(self, event):
        selected_artist = self.artist_spinner.get()
        artist = self.factory.get_artist_by_code(selected_artist)
        selected_album = self.album_spinner.get()
        album = artist.get_album_by_name(selected_album)
        self.song_spinner.config(values=list(album.get_song_codes()))

    def clear_artist_selection(self):
        self.artist_spinner.set("")
        self.artist_name_label.config(text="")
        self.artist_country_label.config(text="")
        self.artist_is_group_label.config(text="")
        self.album_spinner['values'] = []
        self.song_spinner['values'] = []

    def add_artist_popup(self):
        self.artist_popup = tk.Toplevel()
        self.artist_popup.title("Add Artist")

        tk.Label(self.artist_popup, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.artist_name_entry = tk.Entry(self.artist_popup)
        self.artist_name_entry.grid(row=0, column=1)

        tk.Label(self.artist_popup, text="Code:").grid(row=1, column=0, sticky=tk.W)
        self.artist_code_entry = tk.Entry(self.artist_popup)
        self.artist_code_entry.grid(row=1, column=1)

        tk.Label(self.artist_popup, text="Country:").grid(row=2, column=0, sticky=tk.W)
        self.artist_country_entry = tk.Entry(self.artist_popup)
        self.artist_country_entry.grid(row=2, column=1)

        tk.Label(self.artist_popup, text="Is Group:").grid(row=3, column=0, sticky=tk.W)
        self.artist_is_group_entry = tk.Entry(self.artist_popup)
        self.artist_is_group_entry.grid(row=3, column=1)

        tk.Button(self.artist_popup, text="Save", command=self.save_artist).grid(row=4, columnspan=2)

        self.artist_popup.protocol("WM_DELETE_WINDOW", self.on_artist_popup_close)

    def update_artist_popup(self):
        artist_code = self.artist_spinner.get()
        if artist_code:
            artist = self.factory.get_artist_by_code(artist_code)
            if artist:
                self.artist_popup = tk.Toplevel()
                self.artist_popup.title("Update Artist")

                tk.Label(self.artist_popup, text="Name:").grid(row=0, column=0, sticky=tk.W)
                self.artist_name_entry = tk.Entry(self.artist_popup)
                self.artist_name_entry.insert(tk.END, artist.get_name())
                self.artist_name_entry.grid(row=0, column=1)

                tk.Label(self.artist_popup, text="Code:").grid(row=1, column=0, sticky=tk.W)
                self.artist_code_entry = tk.Entry(self.artist_popup)
                self.artist_code_entry.insert(tk.END, artist.get_code())
                self.artist_code_entry.config(state=tk.DISABLED)
                self.artist_code_entry.grid(row=1, column=1)

                tk.Label(self.artist_popup, text="Country:").grid(row=2, column=0, sticky=tk.W)
                self.artist_country_entry = tk.Entry(self.artist_popup)
                self.artist_country_entry.insert(tk.END, artist.get_country())
                self.artist_country_entry.grid(row=2, column=1)

                tk.Label(self.artist_popup, text="Is Group:").grid(row=3, column=0, sticky=tk.W)
                self.artist_is_group_entry = tk.Entry(self.artist_popup)
                self.artist_is_group_entry.insert(tk.END, str(artist.get_is_group()))
                self.artist_is_group_entry.grid(row=3, column=1)

                tk.Button(self.artist_popup, text="Save", command=self.save_artist).grid(row=4, columnspan=2)

                self.artist_popup.protocol("WM_DELETE_WINDOW", self.on_artist_popup_close)
            else:
                messagebox.showerror("Error", "Invalid artist selected.")
        else:
            messagebox.showerror("Error", "No artist selected.")

    def on_artist_popup_close(self):
        if messagebox.askyesno("Confirmation", "Any unsaved/added artist information will be lost. Continue?"):
            self.artist_popup.destroy()

    def save_artist(self):
        name = self.artist_name_entry.get()
        code = self.artist_code_entry.get()
        country = self.artist_country_entry.get()
        is_group = self.artist_is_group_entry.get()

        if not (name and country and is_group):
            messagebox.showerror("Error", "Please enter all the required fields.")
            return

        if code in self.factory.get_artist_codes() and code != self.artist_spinner.get():
            messagebox.showerror("Error", f"Code '{code}' already exists.")
            return

        if self.artist_spinner.get():
            artist = self.factory.get_artist_by_code(self.artist_spinner.get())
            artist.set_name(name)
            artist.set_country(country)
            artist.set_is_group(eval(is_group))
            messagebox.showinfo("Success", "Artist updated successfully!")
            self.save_factory()
        else:
            artist = Artist(code=code, name=name, country=country, is_group=eval(is_group))
            self.factory.add_artist(artist)
            messagebox.showinfo("Success", "Artist added successfully!")
            self.save_factory()

        self.artist_spinner['values'] = list(self.factory.get_artist_codes())
        self.clear_artist_selection()
        self.artist_popup.destroy()

    def delete_artist(self):
        artist_code = self.artist_spinner.get()
        if artist_code:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete the artist?"):
                self.factory.delete_artist(artist_code)
                self.artist_spinner.set("")
                self.artist_spinner['values'] = list(self.factory.get_artist_codes())
                self.clear_artist_selection()
                self.save_factory()
        else:
            messagebox.showerror("Error", "No artist selected.")

    def add_album_popup(self):
        artist_code = self.artist_spinner.get()
        if artist_code:
            self.album_popup = tk.Toplevel()
            self.album_popup.title("Add Album")

            tk.Label(self.album_popup, text="Name:").grid(row=0, column=0, sticky=tk.W)
            self.album_name_entry = tk.Entry(self.album_popup)
            self.album_name_entry.grid(row=0, column=1)

            tk.Label(self.album_popup, text="Year:").grid(row=1, column=0, sticky=tk.W)
            self.album_year_entry = tk.Entry(self.album_popup)
            self.album_year_entry.grid(row=1, column=1)

            tk.Button(self.album_popup, text="Save", command=self.save_album).grid(row=2, columnspan=2)

            self.album_popup.protocol("WM_DELETE_WINDOW", self.on_album_popup_close)
        else:
            messagebox.showerror("Error", "No artist selected.")

    def update_album_popup(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        if artist_code and album_name:
            album = self.factory.get_artist_by_code(artist_code).get_album_by_name(album_name)
            if album:
                self.album_popup = tk.Toplevel()
                self.album_popup.title("Update Album")

                tk.Label(self.album_popup, text="Name:").grid(row=0, column=0, sticky=tk.W)
                self.album_name_entry = tk.Entry(self.album_popup)
                self.album_name_entry.insert(tk.END, album.name)
                self.album_name_entry.grid(row=0, column=1)

                tk.Label(self.album_popup, text="Year:").grid(row=1, column=0, sticky=tk.W)
                self.album_year_entry = tk.Entry(self.album_popup)
                self.album_year_entry.insert(tk.END, album.year)
                self.album_year_entry.grid(row=1, column=1)

                tk.Button(self.album_popup, text="Save", command=self.save_album).grid(row=2, columnspan=2)

                self.album_popup.protocol("WM_DELETE_WINDOW", self.on_album_popup_close)
            else:
                messagebox.showerror("Error", "Invalid album selected.")
        else:
            messagebox.showerror("Error", "No artist or album selected.")

    def on_album_popup_close(self):
        if messagebox.askyesno("Confirmation", "Any unsaved/added album information will be lost. Continue?"):
            self.album_popup.destroy()

    def save_album(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_name_entry.get()
        album_year = self.album_year_entry.get()

        if not (album_name and album_year):
            messagebox.showerror("Error", "Please enter all the required fields.")
            return

        if artist_code:
            artist = self.factory.get_artist_by_code(artist_code)
            if self.album_spinner.get():
                album = artist.get_album_by_name(self.album_spinner.get())
                album.set_name(album_name)
                album.set_year(album_year)
                messagebox.showinfo("Success", "Album updated successfully!")
            else:
                album = Album(name=album_name, year=album_year)
                artist.add_album(album)
                messagebox.showinfo("Success", "Album added successfully!")
            self.album_spinner['values'] = artist.get_albums_names()
            self.album_popup.destroy()
            self.save_factory()
        else:
            messagebox.showerror("Error", "No artist selected.")

    def delete_album(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        if artist_code and album_name:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete the album?"):
                self.factory.get_artist_by_code(artist_code).delete_album_by_name(album_name)
                self.album_spinner.set("")
                self.album_spinner['values'] = self.factory.get_artist_by_code(artist_code).get_albums_names()
                self.save_factory()
        else:
            messagebox.showerror("Error", "No artist or album selected.")

    def add_song_popup(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        if artist_code and album_name:
            self.song_popup = tk.Toplevel()
            self.song_popup.title("Add Song")

            tk.Label(self.song_popup, text="Code:").grid(row=0, column=0, sticky=tk.W)
            self.song_code_entry = tk.Entry(self.song_popup)
            self.song_code_entry.grid(row=0, column=1)

            tk.Button(self.song_popup, text="Generate New Code", command=self.generate_song_code).grid(row=0, column=2)

            tk.Label(self.song_popup, text="Artist Code:").grid(row=1, column=0, sticky=tk.W)
            self.song_artist_code_entry = tk.Entry(self.song_popup)
            self.song_artist_code_entry.insert(tk.END, artist_code)
            self.song_artist_code_entry.config(state=tk.DISABLED)
            self.song_artist_code_entry.grid(row=1, column=1)

            tk.Label(self.song_popup, text="Name:").grid(row=2, column=0, sticky=tk.W)
            self.song_name_entry = tk.Entry(self.song_popup)
            self.song_name_entry.grid(row=2, column=1)

            tk.Label(self.song_popup, text="Album:").grid(row=3, column=0, sticky=tk.W)
            self.song_album_spinner = ttk.Combobox(self.song_popup, values=album_name, width=20)
            self.song_album_spinner.grid(row=3, column=1)

            tk.Label(self.song_popup, text="Year:").grid(row=4, column=0, sticky=tk.W)
            self.song_year_entry = tk.Entry(self.song_popup)
            self.song_year_entry.grid(row=4, column=1)

            tk.Label(self.song_popup, text="Duration (seconds):").grid(row=5, column=0, sticky=tk.W)
            self.song_duration_entry = tk.Entry(self.song_popup)
            self.song_duration_entry.grid(row=5, column=1)

            tk.Label(self.song_popup, text="Genre:").grid(row=6, column=0, sticky=tk.W)
            self.song_genre_spinner = ttk.Combobox(self.song_popup, values=self.factory.get_genres_names(), width=20)
            self.song_genre_spinner.grid(row=6, column=1)

            tk.Label(self.song_popup, text="URL:").grid(row=7, column=0, sticky=tk.W)
            self.song_url_entry = tk.Entry(self.song_popup)
            self.song_url_entry.grid(row=7, column=1)

            tk.Button(self.song_popup, text="Save", command=self.save_song).grid(row=8, columnspan=2)

            self.song_popup.protocol("WM_DELETE_WINDOW", self.on_song_popup_close)
        else:
            messagebox.showerror("Error", "No artist or album selected.")

    def update_song_popup(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        song_code = self.song_spinner.get()
        if artist_code and album_name and song_code:
            song = self.factory.get_artist_by_code(artist_code).get_album_by_name(album_name).get_song(song_code)

            if song:
                self.song_popup = tk.Toplevel()
                self.song_popup.title("Update Song")

                tk.Label(self.song_popup, text="Code:").grid(row=0, column=0, sticky=tk.W)
                self.song_code_entry = tk.Entry(self.song_popup)
                self.song_code_entry.insert(tk.END, song.get_id())
                self.song_code_entry.config(state=tk.DISABLED)
                self.song_code_entry.grid(row=0, column=1)

                tk.Label(self.song_popup, text="Artist Code:").grid(row=1, column=0, sticky=tk.W)
                self.song_artist_code_entry = tk.Entry(self.song_popup)
                self.song_artist_code_entry.insert(tk.END, artist_code)
                self.song_artist_code_entry.config(state=tk.DISABLED)
                self.song_artist_code_entry.grid(row=1, column=1)

                tk.Label(self.song_popup, text="Name:").grid(row=2, column=0, sticky=tk.W)
                self.song_name_entry = tk.Entry(self.song_popup)
                self.song_name_entry.insert(tk.END, song.get_name())
                self.song_name_entry.grid(row=2, column=1)

                tk.Label(self.song_popup, text="Album:").grid(row=3, column=0, sticky=tk.W)
                self.song_album_spinner = ttk.Combobox(self.song_popup, values=[], width=20)
                self.song_album_spinner.insert(tk.END, album_name)
                self.song_album_spinner.config(state=tk.DISABLED)
                self.song_album_spinner.grid(row=3, column=1)

                tk.Label(self.song_popup, text="Year:").grid(row=4, column=0, sticky=tk.W)
                self.song_year_entry = tk.Entry(self.song_popup)
                self.song_year_entry.insert(tk.END, song.get_year())
                self.song_year_entry.grid(row=4, column=1)

                tk.Label(self.song_popup, text="Duration (seconds):").grid(row=5, column=0, sticky=tk.W)
                self.song_duration_entry = tk.Entry(self.song_popup)
                self.song_duration_entry.insert(tk.END, song.get_duration())
                self.song_duration_entry.grid(row=5, column=1)

                tk.Label(self.song_popup, text="Genre:").grid(row=6, column=0, sticky=tk.W)
                self.song_genre_spinner = ttk.Combobox(self.song_popup, values=self.factory.get_genres_names(), width=20)
                self.song_genre_spinner.insert(tk.END, song.get_genre().get_name())
                self.song_genre_spinner.grid(row=6, column=1)

                tk.Label(self.song_popup, text="URL:").grid(row=7, column=0, sticky=tk.W)
                self.song_url_entry = tk.Entry(self.song_popup)
                self.song_url_entry.insert(tk.END, song.get_url())
                self.song_url_entry.grid(row=7, column=1)

                tk.Button(self.song_popup, text="Save", command=self.save_song).grid(row=8, columnspan=2)

                self.song_popup.protocol("WM_DELETE_WINDOW", self.on_song_popup_close)
            else:
                messagebox.showerror("Error", "Invalid song selected.")
        else:
            messagebox.showerror("Error", "No artist, album, or song selected.")

    def on_song_popup_close(self):
        if messagebox.askyesno("Confirmation", "Any unsaved/added song information will be lost. Continue?"):
            self.song_popup.destroy()

    def generate_song_code(self):
        self.song_code_entry.delete(0, tk.END)
        code = self.factory.generate_song_code()
        self.song_code_entry.insert(tk.END, code)

    def save_song(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        song_code = self.song_code_entry.get()
        song_artist_code = self.song_artist_code_entry.get()
        song_name = self.song_name_entry.get()
        song_album = self.song_album_spinner.get()
        song_year = self.song_year_entry.get()
        song_duration = self.song_duration_entry.get()
        song_genre = self.song_genre_spinner.get()
        song_url = self.song_url_entry.get()

        if not (
                song_code and song_artist_code and song_name and song_album and song_year and song_duration and song_genre and song_url):
            messagebox.showerror("Error", "Please enter all the required fields.")
            return

        if song_code in self.factory.get_song_codes() and song_code != self.song_spinner.get():
            messagebox.showerror("Error", f"Code '{song_code}' already exists.")
            return

        artist = self.factory.get_artist_by_code(artist_code)
        album = artist.get_album_by_name(album_name)
        if artist and album:
            if self.song_spinner.get():
                song = album.get_song(self.song_spinner.get())
                song.set_name(song_name)
                song.set_album(song_album)
                song.set_year(song_year)
                song.set_duration(song_duration)
                song.set_genre(song_genre)
                song.set_url(song_url)
                messagebox.showinfo("Success", "Song updated successfully!")
            else:
                song = Song(code=song_code, artist=artist, name=song_name, album=artist.get_album_by_name(song_album),
                            year=song_year, duration=int(song_duration),
                            genre=self.factory.get_genre_by_name(song_genre), url=song_url)
                try:
                    song.get_audio_path()
                except AttributeError:
                    self.audio_listener(song)

                try:
                    song.image_audio_path()
                except AttributeError:
                    self.image_listener(song)

                self.factory.add_song(song)
                messagebox.showinfo("Success", "Song added successfully!")

            self.song_spinner['values'] = album.get_song_codes()
            self.song_popup.destroy()
            self.save_factory()
        else:
            messagebox.showerror("Error", "No artist, album, or song selected.")

    def delete_song(self):
        artist_code = self.artist_spinner.get()
        album_name = self.album_spinner.get()
        song_code = self.song_spinner.get()
        if artist_code and album_name and song_code:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete the song?"):
                self.factory.delete_song(song_code)
                self.song_spinner.set("")
                self.song_spinner['values'] = self.factory.get_artist_by_code(artist_code).get_album_by_name(
                    album_name).get_song_codes()
                self.save_factory()
        else:
            messagebox.showerror("Error", "No artist, album, or song selected.")

    def open_file(self):
        archivo = filedialog.askopenfile(filetypes=[("Archivos de texto", "*.txt")])

        if archivo is not None:
            if messagebox.askyesno("Confirmation", "Want to add Artists and Songs from File?"):
                self.factory.add_data_from_file(archivo)
                self.save_factory()

    def save_factory(self):
        factory_aux = pickle.dumps(self.factory)
        with open(os.path.join(os.getcwd(), "factory.pkl"), "wb") as archivo:
            archivo.write(factory_aux)

    def audio_listener(self, song):
        path = os.path.join(os.getcwd(), "Files", song.get_id())
        audio_name = song.get_id() + ".mp3"
        audio = os.path.join(path, audio_name)

        if os.path.exists(audio):
            messagebox.showinfo("Success", "Audio located!")
        else:
            messagebox.showwarning("Warning",
                                   "Can't proceed until   " + audio_name + "   is located in:\n" + path)
            self.audio_listener(song)

    def image_listener(self, song):
        path = os.path.join(os.getcwd(), "Files", song.get_id())
        image_name = song.get_id() + ".png"
        image = os.path.join(path, image_name)

        if os.path.exists(image):
            messagebox.showinfo("Success", "Image located!")
        else:
            messagebox.showwarning("Warning",
                                   "Can't proceed until   " + image_name + "   is located in:\n" + path)
            self.audio_listener(song)

