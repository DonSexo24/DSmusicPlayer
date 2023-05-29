import os
import random
import string
from tkinter import messagebox
from typing import IO

from Addons import Artist, Song, Tag, Genre, Album
from DSnest import BinaryTree, HashMap, LinkedList
from Users import User


class Factory:
    def __init__(self):
        self.__artists = BinaryTree[Artist]()
        self.__songs = LinkedList[Song]()
        self.__users = HashMap[str, User]()
        self.__users.put_in("admin", User("admin", "$aDmiN", True))
        self.__users.put_in("test", User("test", "1234"))
        self.__genres = LinkedList[Genre]()


        user1 = User("Carla", "torta2")
        user2 = User("Tomas", "torta2")
        user3 = User("Cecilia", "torta2")
        user4 = User("Diego", "torta2")
        self.add_user(user1)
        self.add_user(user2)
        self.add_user(user3)
        self.add_user(user4)

        pop = Genre("pop".upper())
        rock = Genre("rock".upper())
        metal = Genre("metal".upper())
        lofi = Genre("lofi".upper())
        self.add_genre(pop)
        self.add_genre(rock)
        self.add_genre(metal)
        self.add_genre(lofi)

        a1 = Artist("001", "Kali", "USA", False)
        al1 = Album("Weather", "2017")
        a1.add_album(al1)
        self.add_artist(a1)
        s1 = Song("Hazel", "sh7agA", al1, a1, al1.year, 115, pop, "https://www.youtube.com/watch?v=lp7SDPPbx-s")
        self.add_song(s1)

        a2 = Artist("002", "Mirella", "COL", False)
        al2 = Album("Lucero", "2018")
        a2.add_album(al2)
        self.add_artist(a2)
        s2 = Song("CruzDeSol", "a8a9HA", al2, a2, al2.year, 101, lofi, "https://www.youtube.com/watch?v=lp7SDPPbx-s")
        self.add_song(s2)

        a3 = Artist("003", "Aztecombo", "MX", True)
        al3 = Album("SandiaWine", "2015")
        a3.add_album(al3)
        self.add_artist(a3)
        s3 = Song("Ganzua", "0A89lg", al3, a3, al3.year, 110, rock, "https://www.youtube.com/watch?v=vKgqf1Bo_UI")
        self.add_song(s3)

        a4 = Artist("004", "Angy-G", "MX", False)
        al4 = Album("Alors", "2013")
        a4.add_album(al4)
        self.add_artist(a4)
        s4_1 = Song("Voux", "H97gAa", al4, a4, al4.year, 50, pop, "https://www.youtube.com/watch?v=PrURjtcpBgU")
        s4_2 = Song("Trem", "ah76oP", al4, a4, al4.year, 56, rock, "https://www.youtube.com/watch?v=PrURjtcpBgU")
        s4_3 = Song("Claim", "h7Gaf1", al4, a4, al4.year, 53, pop, "https://www.youtube.com/watch?v=PrURjtcpBgU")
        s4_4 = Song("Solitude", "aj89aG", al4, a4, al4.year, 56, rock, "https://www.youtube.com/watch?v=PrURjtcpBgU")
        self.add_song(s4_1)
        self.add_song(s4_2)
        self.add_song(s4_3)
        self.add_song(s4_4)

        a5 = Artist("005", "Howler", "CDA", False)
        al5 = Album("Luxury", "2021")
        a5.add_album(al5)
        self.add_artist(a5)

        s5 = Song("Beach", "1la0AG", al5, a5, al5.year, 49, pop, "https://www.youtube.com/watch?v=WSukD4Y_QY0")
        s5.add_tag(Tag("Trending"))
        s5.add_tag(Tag("Alelux"))
        s5.add_tag(Tag("Partrend"))
        s5.add_tag(Tag("Atrendding"))
        self.add_song(s5)

        self.add_user_song(user1, s2)
        self.add_user_song(user1, s5)
        self.add_user_song(user1, s4_4)
        self.add_user_song(user1, s1)
        self.add_user_song(user1, s4_1)
        


    def add_song(self, song: Song):
        if song is None:
            raise AttributeError("Song can't be None")
        if song.get_artist() is None:
            raise AttributeError("Artist can't be None")
        if not self.__artists.contains(song.get_artist()):
            raise AttributeError("Artist not found")
        else:
            song.get_artist().add_song(song)
            self.__songs.append(song)

    def add_artist(self, artist: Artist):
        self.__artists.add(artist)
        self.__artists.balance()

    def add_user(self, user: User):
        self.__users.put_in(user.username, user)

    def add_song_tag(self, song: Song, tag: Tag):
        if song.contains_true_tag(tag):
            raise AttributeError("Tag already assigned here")
        else:
            song.add_tag(tag)

    def remove_song_tag(self, song: Song, tag: Tag):
        if not song.contains_true_tag(tag):
            raise AttributeError("Unable to delete tab not assigned")
        else:
            song.remove_tag(tag)

    def get_songs(self):
        return self.__songs

    def add_user_song(self, user: User, song: Song):
        if not self.__songs.contains(song):
            raise AttributeError("Song not founded")
        if not self.__users.contains_value(user):
            raise AttributeError("User not founded")
        user.add_song(song)

    def remove_user_song(self, user: User, song: Song):
        if not self.__songs.contains(song):
            raise AttributeError("Song not founded")
        if not self.__users.contains_value(user):
            raise AttributeError("User not founded")
        user.delete_song(song)

    def get_users(self):
        return self.__users

    def contains_user(self, username: str):
        return self.__users.contains_key(username)

    def get_user(self, username: str):
        return self.__users.get(username)

    def get_genres(self) -> LinkedList[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_artists(self) -> BinaryTree[Artist]:
        return self.__artists

    def get_artist_by_code(self, code: str) -> Artist:
        for artist in self.__artists.in_order_traversal():
            if artist.get_code() == code:
                return artist

    def contains_artist(self, artist: Artist) -> bool:
        return self.__artists.contains(artist)

    def get_artist_codes(self) -> LinkedList[str]:
        codes = LinkedList[str]()
        for artist in self.__artists.in_order_traversal():
            codes.append(artist.get_code())
        return codes

    def delete_artist(self, artist_code):
        artist = self.get_artist_by_code(artist_code)
        if artist:
            for song in artist.get_song_list():
                for user in self.__users:
                    try:
                        user.delete_song(song)
                    except AttributeError:
                        pass
                for genre in self.__genres:
                    try:
                        genre.remove_song(song)
                    except AttributeError:
                        pass
                try:
                    self.__songs.remove(song)
                except AttributeError:
                    pass
            self.__artists.remove(artist)

    def get_genres_names(self):
        names = []
        for genre in self.__genres:
            names.append(genre.get_name())
        return names

    def generate_song_code(self):
        code_length = 6
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(code_length))

        while self.song_code_exists(code):
            code = ''.join(random.choice(characters) for _ in range(code_length))

        return code

    def song_code_exists(self, code):
        for artist in self.__artists.in_order_traversal():
            for album in artist.get_albums():
                if album.song_exists(code):
                    return True
        return False

    def get_song_codes(self):
        codes = []
        for song in self.__songs:
            codes.append(song.get_id())
        return codes

    def get_genre_by_name(self, name: str):
        for genre in self.__genres:
            if genre.get_name() == name:
                return genre

    def delete_song(self, song_code):
        song = self.get_song_by_code(song_code)
        for user in self.__users:
            try:
                user.delete_song(song)
            except AttributeError:
                pass
        for genre in self.__genres:
            try:
                genre.remove_song(song)
            except AttributeError:
                pass
        for artist in self.__artists.in_order_traversal():
            try:
                artist.remove_song(song)
            except AttributeError:
                pass
        self.__songs.remove_by_value(song)

    def get_song_by_code(self, song_code):
        for song in self.__songs:
            if song.get_id() == song_code:
                return song

    def add_data_from_file(self, archivo: IO):
        songs = self.__songs
        artists = self.__artists
        genres = self.__genres

        try:
            lines = archivo.readlines()
            for line in lines:
                arguments = LinkedList[str]()
                for element in line.strip().split(":"):
                    arguments.append(element)

                if arguments.size() == 4:
                    try:
                        artists.add(Artist(str(arguments.get(0)).upper(),
                                           str(arguments.get(1)).upper(),
                                           str(arguments.get(2)).upper(),
                                           arguments.get(3)))
                        print("Artist added successfully")
                    except AttributeError:
                        print("Artist already exists")

                elif arguments.size() == 7:
                    aux_artist = Artist("", "", "", False)
                    aux_album = Album("", "")
                    aux_genre = Genre("")

                    for artist in artists.in_order_traversal():
                        if artist.get_name() == str(arguments.get(0)).upper():
                            aux_artist = artist
                            break

                    for album in aux_artist.get_albums():
                        if album.get_name() == arguments.get(2):
                            aux_album = album
                            break

                    for genre in genres:
                        if genre.get_name() == arguments.get(5):
                            aux_genre = genre
                            break

                    if aux_artist.get_name() == "":
                        if aux_genre.name == "":
                            self.add_genre(Genre(str(arguments.get(5)).upper()))

                        if aux_album.name == "":
                            aux_album = Album(arguments.get(2), arguments.get(3))

                        song = Song(arguments.get(1), self.generate_song_code(), aux_album,
                                    aux_artist, arguments.get(3), int(arguments.get(4)),
                                    aux_genre, arguments.get(6))

                        try:
                            song.get_audio_path()
                        except AttributeError:
                            self.audio_listener(song)

                        try:
                            song.get_cover_path()
                        except AttributeError:
                            self.image_listener(song)

                        try:
                            aux_artist.add_song(song)
                            aux_genre.add_song(song)
                            songs.append(song)
                            print("Song added successfully")
                        except AttributeError:
                            print("Song already exists")
                    else:
                        print("Artist not found")
        except FileNotFoundError:
            print("File not found")

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
