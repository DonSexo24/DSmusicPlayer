import glob
import os
import shutil
import subprocess
import urllib
from tkinter import filedialog

from pytube import YouTube
import youtube_dl
from DSnest import ComparableValue, LinkedList, DoubleLinkedList, BinaryTree


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Album loader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#
class Album(ComparableValue):
    def __init__(self, name: str, year: str):
        self.name = name
        self.year = year
        self.songs = LinkedList[Song]()

    def song_exists(self, song_code: str):
        for song in self.songs:
            if song.get_id() == song_code:
                return True
        return False

    def get_song_codes(self):
        codes = []
        for song in self.songs:
            codes.append(song.get_id())
        return codes

    def get_song(self, song_code: str):
        for song in self.songs:
            if song.get_id() == song_code:
                return song

    def add_song(self, song: 'Song'):
        self.songs.append(song)

    def __lt__(self, other: 'Album') -> bool:
        return self.name.upper() < other.name.upper()

    def __gt__(self, other: 'Album') -> bool:
        return self.name.upper() > other.name.upper()

    def __eq__(self, other: 'Album') -> bool:
        return self.name.upper() == other.name.upper()

    def __le__(self, other: 'Album') -> bool:
        return self.name.upper() <= other.name.upper()

    def __ge__(self, other: 'Album') -> bool:
        return self.name.upper() >= other.name.upper()


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #tag loader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class Tag(ComparableValue):
    def __init__(self, attribute: str):
        self.__attribute = attribute

    def get_attribute(self):
        return self.__attribute

    def __lt__(self, other: 'Tag') -> bool:
        return self.__attribute < other.get_attribute()

    def __gt__(self, other: 'Tag') -> bool:
        return self.__attribute > other.get_attribute()

    def __eq__(self, other: 'Tag') -> bool:
        return self.__attribute == other.get_attribute()

    def __le__(self, other: 'Tag') -> bool:
        return self.__attribute <= other.get_attribute()

    def __ge__(self, other: 'Tag') -> bool:
        return self.__attribute >= other.get_attribute()

    def get_compatibility(self, tag2: 'Tag') -> bool:
        if not self or not tag2:
            raise ValueError("String can't be null")
        if len(self.__attribute) == 0 or len(tag2.get_attribute()) == 0:
            return False

        string1 = self.__attribute.lower()
        string2 = tag2.get_attribute().lower()

        if string1 == string2:
            return True

        if string1 in string2 or string2 in string1:
            return True

        return False


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #song loader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


class Song(ComparableValue):

    def __init__(self, name: str, code: str, album: Album, artist: 'Artist', year: str, duration: int,
                 genre: 'Genre', url: str):

        self.__name = name
        self.__id = code
        self.__album = album
        album.songs.append(self)
        self.__artist = artist
        self.__year = year
        self.__duration = duration
        self.__genre = genre
        genre.add_song(self)
        self.__url = url
        self.__tags = BinaryTree[Tag]()
        self.__tags.add(Tag(name))
        self.__tags.add(Tag(year))
        self.__tags.add(Tag(self.__genre.get_name()))
        self.__tags.add(Tag(self.__artist.get_name()))
        print(self.__artist.get_name(), "name")
        self.__tags.add(Tag(album.name))
        self.__tags.balance()

    def get_name(self):
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_id(self):
        return self.__id

    def set_id(self, code: str):
        self.__id = code

    def get_album(self):
        return self.__album

    def set_album(self, album: Album):
        self.__album = album

    def get_artist(self):
        return self.__artist

    def set_artist(self, artist):
        self.__artist = artist

    def get_year(self):
        return self.__year

    def set_year(self, year: str):
        self.__year = year

    def get_duration(self):
        return self.__duration

    def set_duration(self, duration: int):
        self.__duration = duration

    def get_genre(self):
        return self.__genre

    def get_genre_name(self):
        return self.__genre.get_name()

    def set_genre(self, genre: 'Genre'):
        self.__tags.remove(Tag(self.__genre.get_name()))
        self.__genre = genre
        self.__tags.add(Tag(self.__genre.get_name()))

    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_cover_path(self):
        path = os.path.join(os.getcwd(), "Files")
        return retrieve_image_path(self.__id, self.__url, path)

    def get_audio_path(self):
        return retrieve_audio_path(self.__id, self.__url, os.getcwd())

    def get_all_tags(self) -> []:
        return self.__tags.in_order_traversal()

    def get_filtered_tags(self, tag: Tag) -> []:
        values = []
        for aux_tag in self.get_all_tags():
            if tag.get_compatibility(aux_tag):
                values.append(aux_tag)
        return values

    def add_tag(self, tag: Tag):
        if self.__tags.contains(tag):
            raise AttributeError("Song already has this tag")
        else:
            self.__tags.add(tag)
            self.__tags.balance()

    def remove_tag(self, tag: Tag):
        self.__tags.remove(tag)

    def contains_true_tag(self, tag: Tag) -> bool:
        return self.__tags.contains(tag)

    def contains_partial_tag(self, tag: Tag) -> bool:
        for aux_tag in self.get_all_tags():
            if tag.get_compatibility(aux_tag):
                return True
        return False

    def __lt__(self, other: 'Song') -> bool:
        return self.__id < other.get_id()

    def __gt__(self, other: 'Song') -> bool:
        return self.__id > other.get_id()

    def __eq__(self, other: 'Song') -> bool:
        return self.__id == other.get_id()

    def __le__(self, other: 'Song') -> bool:
        return self.__id <= other.get_id()

    def __ge__(self, other: 'Song') -> bool:
        return self.__id >= other.get_id()


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Artist loader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


class Artist(ComparableValue):

    def __init__(self, code: str, name: str, country: str, is_group: bool):
        self.__code = code
        self.__name = name
        self.__country = country
        self.__is_group = is_group
        self.__song_list = DoubleLinkedList()
        self.__albums = LinkedList[Album]()
        self.__albums.append(Album("Singles", ""))

    def add_song(self, song: Song):
        if self.__song_list.contains(song):
            raise AttributeError("Song already added")
        if not self.__albums.contains(song.get_album()):
            raise AttributeError("Album not found")
        else:
            self.__song_list.append(song)

    def add_album(self, album: Album):
        if self.__albums.contains(album):
            raise AttributeError("Album already added")
        else:
            self.__albums.append(album)

    def get_code(self):
        return self.__code

    def set_code(self, code):
        self.__code = code

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_country(self) -> str:
        return self.__country

    def set_country(self, country: str):
        self.__country = country

    def get_is_group(self) -> bool:
        return self.__is_group

    def set_is_group(self, is_group: bool):
        self.__is_group = is_group

    def get_song_list(self) -> DoubleLinkedList[Song]:
        return self.__song_list

    def set_song_list(self, song_list: DoubleLinkedList[Song]):
        self.__song_list = song_list

    # Getter and setter for albums
    def get_albums(self) -> LinkedList[Album]:
        return self.__albums

    def get_albums_names(self):
        names = []
        for album in self.__albums:
            names.append(album.name)
        return names

    def set_albums(self, albums: LinkedList[Album]):
        self.__albums = albums

    def get_album_by_name(self, album_name: str):
        for album in self.__albums:
            if album.name == album_name:
                return album
        return None

    def delete_album_by_name(self, album_name: str):
        self.__albums.remove_by_value(Album(album_name, "NA"))

    def remove_song(self, song):
        for album in self.__albums:
            album.songs.remove_by_value(song)
        self.__song_list.remove_value(song)

    def __lt__(self, other: 'Artist') -> bool:
        return self.__code < other.get_code()

    def __gt__(self, other: 'Artist') -> bool:
        return self.__code > other.get_code()

    def __eq__(self, other: 'Artist') -> bool:
        return self.__code == other.get_code()

    def __le__(self, other: 'Artist') -> bool:
        return self.__code <= other.get_code()

    def __ge__(self, other: 'Artist') -> bool:
        return self.__code >= other.get_code()


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Genre loader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


class Genre(ComparableValue):

    def __init__(self, name: str):
        self.__name = name
        self.__songs = LinkedList[Song]()

    def get_name(self) -> str:
        return self.__name

    def get_songs(self) -> LinkedList[Song]:
        return self.__songs

    def number_songs(self) -> int:
        return self.__songs.size()

    def add_song(self, song: Song):
        if self.__songs.contains(song):
            raise AttributeError("Song already here")
        else:
            self.__songs.append(song)

    def remove_song(self, song: Song):
        if not self.__songs.contains(song):
            raise AttributeError("Song not present")
        else:
            self.__songs.remove_by_value(song)

    def __lt__(self, other: 'Genre') -> bool:
        return self.__name < other.get_name()

    def __gt__(self, other: 'Genre') -> bool:
        return self.__name > other.get_name()

    def __eq__(self, other: 'Genre') -> bool:
        return self.__name == other.get_name()

    def __le__(self, other: 'Genre') -> bool:
        return self.__name <= other.get_name()

    def __ge__(self, other: 'Genre') -> bool:
        return self.__name >= other.get_name()


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Song Filter by 'AND' search with Tag compatibility
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


def get_all_filtered_songs(tags: LinkedList[Tag], songs: LinkedList[Song]):
    aux_songs = LinkedList[Song]()
    for song in songs:
        flag = True
        for tag_to_evaluate in tags:
            if not song.contains_partial_tag(tag_to_evaluate):
                flag = False
        if flag.__eq__(True):
            aux_songs.append(song)

    return aux_songs

def get_any_filtered_songs(tags: LinkedList[Tag], songs: LinkedList[Song]):
    aux_songs = LinkedList[Song]()
    for song in songs:
        flag = False
        for tag_to_evaluate in tags:
            if song.contains_partial_tag(tag_to_evaluate):
                flag = True
                break
        if flag.__eq__(True):
            aux_songs.append(song)

    return aux_songs


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Filter Genres by the one (or group of) with most songs
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

def genre_with_most_songs(genres: LinkedList[Genre]) -> LinkedList[Genre]:
    aux_genres = LinkedList[Genre]()
    max_size = 0
    for genre in genres:
        genre_song_size = genre.number_songs()
        if genre_song_size >= max_size:
            if genre_song_size > max_size:
                max_size = genre_song_size
                aux_genres.clear()
            aux_genres.append(genre)

    return aux_genres


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Audio & Image format retrieving
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

def retrieve_audio_path(song_id: str, url, root_path: str) -> str:
    folder_path = os.path.join(root_path, "Files", song_id)
    audio_path = os.path.join(folder_path, song_id + ".mp3")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    if not os.path.exists(audio_path):
        raise AttributeError("Audio file not found")
    return audio_path


def retrieve_image_path(song_id: str, url: str, root_path: str) -> str:
    folder_path = os.path.join(root_path, song_id)
    image_path = os.path.join(folder_path, song_id + ".jpg")
    if not os.path.exists(image_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        try:
            __download_image(song_id, url, folder_path)
        except FileNotFoundError:
            print("Error while downloading img")
    return image_path



def __download_image(song_id: str, url, folder_path: str):
    image_path = os.path.join(folder_path, song_id + ".jpg")
    youtube_stream = YouTube(str(url))
    image_url = youtube_stream.thumbnail_url
    urllib.request.urlretrieve(image_url, image_path)
    print(image_path.title(), "downloaded at", folder_path.title())
