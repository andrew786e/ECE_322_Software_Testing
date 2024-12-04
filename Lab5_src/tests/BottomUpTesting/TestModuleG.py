import unittest
from unittest.mock import mock_open, patch

from data.Entry import Entry
from modules.ModuleG import ModuleG


class TestModuleG(unittest.TestCase):
    # Sets up initial values for different types of data to be tested
    def setUp(self):
        self.module_g = ModuleG()
        self.valid_data = [
            Entry('John' , '123456'),
            Entry('Doe' , '789101')
        ]
        self.empty_data = []
        self.invalid_data = [
            type('Data', (object,), {'name': 'John'}),
            type('Data', (object,), {'number': '789101'})
        ]

    @patch("builtins.open", new_callable=mock_open)
    def test_successful_update(self, mock_file):
        self.module_g.updateData("testfile.txt", self.valid_data)
        mock_file.assert_called_once_with("testfile.txt", "w")
        mock_file().write.assert_any_call("John,123456\n")
        mock_file().write.assert_any_call("Doe,789101\n")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.module_g.updateData("invalid_path.txt", self.valid_data)
            mock_print.assert_called_once_with("Error updating DB File.")

    @patch("builtins.open", new_callable=mock_open)
    def test_empty_data(self, mock_file):
        self.module_g.updateData("testfile.txt", self.empty_data)
        mock_file.assert_called_once_with("testfile.txt", "w")
        mock_file().write.assert_not_called()

    def test_invalid_data_objects(self):
        with self.assertRaises(AttributeError):
            self.module_g.updateData("testfile.txt", self.invalid_data)

