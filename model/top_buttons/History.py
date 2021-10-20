from enum import Enum

from model.top_buttons.ActionCreate import *

class History():


    def __init__(self):
        self.matrix = []
        self.current_array = []

    def add_action(self, action):
        self.current_array.append(action)

    """
    Appends the current array to the matrix and resets the current array
    """
    def next_index(self):
        self.matrix.append(self.current_array)
        self.current_array = []

    def get_action_array(self, index):
        return self.matrix[index]

    def get_last_action_array(self):
        return self.matrix[-1]

    def remove_last_action_array(self):
        self.matrix.remove(self.get_last_action_array())

    def size(self):
        return len(self.matrix)

    def get_array(self, index):
        return self.matrix[index]

    def is_empty(self):
        return self.size() == 0

    def not_empty(self):
        return not self.is_empty()

    def set_matrix(self, matrix):
        self.matrix = matrix
