import copy
import os.path
import urllib
from typing import IO

import pygame
from Addons import Artist, Song, Genre, Album
from DSnest import Stack, LinkedList, BinaryTree


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


