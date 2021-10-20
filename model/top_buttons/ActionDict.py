from model.top_buttons.ActionCreate import ActionType


class ActionDict():

    _dict = dict()

    def __init__(self):
        self._dict[ActionType.MOVE] = []
        self._dict[ActionType.CREATE] = []
        self._dict[ActionType.DELETE] = []

    def add_action(self, action):
        self._dict[action.get_type()].append(action)

    def keys(self):
        return self._dict.keys()

    def get_dict(self):
        return self._dict

    def get_move(self, type):
        return self._dict[type]