import unittest

from model.top_buttons.ActionCreate import ActionCreate, ActionType
from tests.frameworks.Generator import Generator

expected = ActionCreate(ActionType.MOVE, Generator.random_path(), Generator.random_path())
expected2 = ActionCreate(ActionType.CREATE, Generator.random_path(), Generator.random_path())

class ActionTest(unittest.TestCase):

    def setUp(self):
        self.action = ActionCreate(expected.get_type(), expected.get_old_path(), expected.get_new_path())
        self.action2 = ActionCreate(expected2.get_type(), expected2.get_old_path(), expected2.get_new_path())

    def test_type(self):
        self.assertEqual(expected.get_type(), self.action.get_type())
        self.assertEqual(expected2.get_type(), self.action2.get_type())

    def test_new_path(self):
        self.assertEqual(expected.get_new_path(), self.action.get_new_path())
        self.assertEqual(expected2.get_new_path(), self.action2.get_new_path())

    def test_old_path(self):
        self.assertEqual(expected.get_old_path(), self.action.get_old_path())
        self.assertEqual(expected2.get_old_path(), self.action2.get_old_path())

    def test_old_path(self):
        self.assertEqual(expected.get_current_path(), self.action.get_current_path())
        self.assertEqual(expected.get_current_path(), self.action.get_new_path())
        self.assertEqual(expected2.get_current_path(), self.action2.get_current_path())
        self.assertEqual(expected2.get_current_path(), self.action2.get_old_path())