import copy

from Addons import Song
from DSnest import HashMap, CircularList, ComparableValue
from DStools import UndoRedoManager


class User(ComparableValue):
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.__song_list = CircularList()
        self.__undo_redo_manager = UndoRedoManager()

    def get_song_list(self):
        return self.__song_list

    def set_song_list(self, song_list: CircularList[Song]):
        self.__song_list = song_list

    def add_song(self, song: Song):
        if self.__song_list.contains(song):
            raise AttributeError("This song is already here")
        else:
            self.__undo_redo_manager.push_state(copy.deepcopy(self.__song_list))
            self.__song_list.append(song)

    def delete_song(self, song: Song):
        if not self.__song_list.contains(song):
            raise AttributeError("Can't remove song that's not already here")
        else:
            self.__undo_redo_manager.push_state(copy.deepcopy(self.__song_list))
            self.__song_list.remove_value(song)

    def sort_song_list(self, key):
        self.__song_list.sort(key)

    def undo(self):
        state = self.__undo_redo_manager.undo(self.__song_list)
        if state:
            self.__song_list = copy.deepcopy(state)

    def redo(self):
        state = self.__undo_redo_manager.redo(self.__song_list)
        if state:
            self.__song_list = copy.deepcopy(state)

    def contains_song(self, song: Song):
        return self.__song_list.contains(song)

    def __lt__(self, other: 'User') -> bool:
        return self.username < other.username

    def __gt__(self, other: 'User') -> bool:
        return self.username > other.username

    def __eq__(self, other: 'User') -> bool:
        return self.username == other.username

    def __le__(self, other: 'User') -> bool:
        return self.username <= other.username

    def __ge__(self, other: 'User') -> bool:
        return self.username >= other.username


class Users:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = HashMap[str, User]()
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    username, password = line.strip().split(":")
                    user = User(username, password)
                    users.put_in(username, user)
        except FileNotFoundError:
            pass
        return users

    def save_users(self):
        with open(self.filename, "w") as file:
            for user in self.users:
                file.write(f"{user.username}:{user.password}\n")
                print(user.username, user.password)

    def put(self, username, user):
        self.users.put_in(username, user)
        self.save_users()

    def get(self, username):
        return self.users.get(username)

    def contains(self, username: str):
        return self.users.contains_key(username)
