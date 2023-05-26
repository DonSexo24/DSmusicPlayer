from Addons import Artist, Song, Tag, Genre
from DSnest import BinaryTree, HashMap, LinkedList
from Users import User


class Factory:
    def __init__(self):
        self.__artist = BinaryTree[Artist]()
        self.__songs = LinkedList[Song]()
        self.__users = HashMap[str, User]()
        self.__genres = LinkedList[Genre]()

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

    def get_filtered_songs(self, tags: LinkedList[Tag], songs: LinkedList[Song]):
        aux_songs = LinkedList[Song]()
        for song in songs:
            flag = True
            for tag_to_evaluate in tags:
                if not song.contains_partial_tag(tag_to_evaluate):
                    flag = False
            if flag.__eq__(True):
                aux_songs.append(song)

        return aux_songs
