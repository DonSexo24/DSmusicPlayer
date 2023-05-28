from Addons import Artist, Song, Tag, Genre, Album
from DSnest import BinaryTree, HashMap, LinkedList
from Users import User


class Factory:
    def __init__(self):
        self.__artist = BinaryTree[Artist]()
        self.__songs = LinkedList[Song]()
        self.__users = HashMap[str, User]()
        self.__users.put_in("admin", User("admin", "$aDmiN", True))
        self.__users.put_in("test", User("test", "1234"))
        self.__genres = LinkedList[Genre]()

        """
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
        
        """

    def add_song(self, song: Song):
        if song is None:
            raise AttributeError("Song can't be None")
        if song.get_artist() is None:
            raise AttributeError("Artist can't be None")
        if not self.__artist.contains(song.get_artist()):
            raise AttributeError("Artist not found")
        else:
            song.get_artist().add_song(song)
            self.__songs.append(song)

    def add_artist(self, artist: Artist):
        self.__artist.add(artist)
        self.__artist.balance()

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

