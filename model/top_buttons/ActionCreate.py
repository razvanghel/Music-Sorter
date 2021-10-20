import os
from abc import abstractmethod
from enum import Enum
from handlers import FileHandler as f

class ActionType(Enum):
    DELETE = -1
    MOVE = 0
    CREATE = 1

class Action():
    def __init__(self, type, current_path):
        self.type = type
        self.current_path = current_path

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_current_path(self):
        return self.current_path

    def set_current_path(self, path):
        self.current_path = path

    @abstractmethod
    def reverse_action(self):
        pass

class ActionCreate(Action):

    def __init__(self, current_path):
        Action.__init__(self, ActionType.CREATE, current_path)

    def reverse_action(self):
        f.remove_directory(self.get_current_path())

class ActionDelete(Action):

    def __init__(self, current_path):
        Action.__init__(self, ActionType.CREATE, current_path)

    def reverse_action(self):
        f.create_directory(self.get_current_path())

class ActionMove(Action):

    def __init__(self, old_path, current_path):
        Action.__init__(self, ActionType.MOVE, current_path)
        self.old_path = old_path

    def get_old_path(self):
        return self.old_path

    def set_old_path(self, path):
        self.old_path = path

    def reverse_action(self):
        f.move_file(self.get_current_path(), self.get_old_path())
