import unittest


from model.top_buttons.History import History, ActionType
from tests.frameworks.Generator import Generator


class HistoryTest(unittest.TestCase):

    def test_get_action(self):
        action1 = Generator.random_action_dict()
        h = History()
        h.add_action(action1)
        h.add_action(Generator.random_action_dict())
        h.add_action(Generator.random_action_dict())
        self._check_action(action1, h.get_action_array(0))

    def test_get_last_action(self):
        action1 = Generator.random_action_dict()
        h = History()
        h.add_action(Generator.random_action_dict())
        h.add_action(Generator.random_action_dict())
        h.add_action(action1)
        self._check_action(action1, h.get_last_action_array())

    def test_remove_last_action(self):
        action1 = Generator.random_action_dict()
        h = History()
        h.add_action(Generator.random_action_dict())
        h.add_action(Generator.random_action_dict())
        h.add_action(action1)
        self.assertTrue(action1 in h.get_array())
        h.remove_last_action()
        self.assertTrue(action1 not in h.get_array())

    def test_add_action(self):
        h = History()
        dict = Generator.random_action_dict()
        h.add_action(dict)
        self.check_action_dict(dict, h.get_last_action_array())
        dict2 = Generator.random_action_dict()
        h.add_action(dict2)
        self.check_action_dict(dict2, h.get_last_action_array())

    def check_action_dict(self, expected, actual):
        for key in expected.keys():
            self.assertIsNotNone(actual[key])
            e_arr = expected[key]
            arr = actual[key]
            for e in range(0,len(e_arr)):
                self.assertEqual(e_arr[e], arr[e])

    def _check_action(self, expected, actual):
        self.assertEqual(expected.keys(), actual.keys())
        for value in expected.values():
            self.assertTrue(value in actual.values())