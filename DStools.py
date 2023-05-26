import copy
import os.path
import urllib
import pygame
from pytube import YouTube

from Addons import Artist, Song, Genre, Album
from DSnest import Stack, LinkedList, BinaryTree


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Audio & Image format retrieving
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

def retrieve_audio(song_id: str, url, root_path: str) -> str:
    audio_path = os.path.join(root_path, song_id + ".mp3")
    if not os.path.exists(audio_path):
        __download_audio(song_id, url, root_path)
    return audio_path


def retrieve_image(song_id: str, url, root_path: str) -> Image:
    image_path = os.path.join(os.path.join(root_path, song_id), song_id + ".jpg")
    if not os.path.exists(image_path):
        __download_image(song_id, url, root_path)


def __download_audio(song_id: str, video_url, root_path: str):
    print("Not supported yet")


def __download_image(song_id: str, url, root_path: str):
    personal_path = os.path.join(root_path, song_id)

    if not os.path.exists(personal_path):
        os.mkdir(personal_path)

    youtube_stream = YouTube(str(url))
    image_file = youtube_stream.thumbnail_url
    image_path = os.path.join(personal_path, song_id + ".jpg")

    if not os.path.exists(image_path):
        urllib.request.urlretrieve(image_file, image_path)
        print(image_path.title())


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #undo & redo action
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class UndoRedoManager:
    def __init__(self):
        self.redo_stack = Stack()
        self.undo_stack = Stack()

    def push_state(self, state):
        self.undo_stack.push(state)
        self.redo_stack.clear()

    def undo(self, current):
        if not self.undo_stack.is_empty():
            print(self.undo_stack.size(), self.redo_stack.size())
            state = self.undo_stack.poll()
            self.redo_stack.push(copy.deepcopy(current))
            print(self.undo_stack.size(), self.redo_stack.size())
            return copy.deepcopy(state)
        else:
            return None

    def redo(self, current):
        if self.redo_stack.is_empty:
            print(self.undo_stack.size(), self.redo_stack.size())
            state = self.redo_stack.poll()
            self.undo_stack.push(copy.deepcopy(current))
            print(self.undo_stack.size(), self.redo_stack.size())
            return copy.deepcopy(state)
        else:
            return None

# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #File reader
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


def add_data_from_file(songs: LinkedList[Song], artists: BinaryTree[Artist], genres: LinkedList[Genre],
                       path_to_file: str):
    try:
        with open(path_to_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                aux = LinkedList[str]()
                for element in line.strip().split(":"):
                    aux.append(element)

                if aux.size() == 4:
                    try:
                        artists.add(Artist(aux.get(0), aux.get(1), aux.get(2), aux.get(3)))
                    except AttributeError:
                        print("Artist already exists")

                elif aux.size() == 7:
                    aux_artist = Artist("", "", "", False)
                    aux_album = Album("", "")
                    aux_genre = Genre("")

                    for artist in artists.in_order_traversal():
                        if artist.get_name() == aux.get(0):
                            aux_artist = artist
                            break

                    for album in aux_artist.get_albums():
                        if album.get_name() == aux.get(2):
                            aux_album = album
                            break

                    for genre in genres:
                        if genre.get_name() == aux.get(5):
                            aux_genre = genre
                            break

                    if aux_artist.get_name() == "":
                        if aux_genre.name == "":
                            if aux_album.name == "":
                                aux_album = Album(aux.get(2), aux.get(3))

                            song = Song(aux.get(1), "code_generator", aux_album,
                                        aux_artist, aux.get(3), int(aux.get(4)),
                                        aux_genre, aux.get(6))
                            try:
                                aux_artist.add_song(song)
                                aux_genre.add_song(song)
                                songs.append(song)
                            except AttributeError:
                                print("Song already exists")
                        else:
                            print("Genre not found")
                    else:
                        print("Artist not found")
    except FileNotFoundError:
        print("File not found")

# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Audio Player
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class AudioPlayer:
    def __init__(self, ruta_archivo):
        pygame.mixer.init()
        self.ruta_archivo = ruta_archivo
        self.paused = False
        self.playing = False

    def toggle_playback(self):
        if not self.playing:
            pygame.mixer.music.load(self.ruta_archivo)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def play_from_timestamp(self, timestamp):
        if not self.playing:
            pygame.mixer.music.load(self.ruta_archivo)
        pygame.mixer.music.play(start=timestamp)
        self.playing = True
        self.paused = False
