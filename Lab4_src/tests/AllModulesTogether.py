import unittest
from unittest.mock import MagicMock, mock_open, patch
from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE
from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG
from data.Entry import Entry


class TestAllModulesTogether(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.module_f = ModuleF()
        self.module_g = ModuleG()
        self.module_b = ModuleB(f=self.module_f)
        self.module_c = ModuleC(f=self.module_f)
        self.module_d = ModuleD(f=self.module_f, g=self.module_g)
        self.module_e = ModuleE()
        self.module_a = ModuleA(b=self.module_b, c=self.module_c, d=self.module_d, e=self.module_e)

    @patch("builtins.open", new_callable=mock_open, read_data="Alice,123\nBob,456\n")
    def test_file_loading_and_display(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[0].name, "Alice")
        mock_file.assert_called_once_with("mock_file.txt")

    @patch("builtins.open", new_callable=mock_open, read_data="Alice,123\nBob,456\n")
    def test_data_addition_and_display(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        self.module_d.insertData = MagicMock(return_value=[Entry("Alice", "123"), Entry("Bob", "456"), Entry("Charlie", "789")])
        self.module_a.parseAdd("Charlie", "789")
        self.assertEqual(len(self.module_a.data), 3)
        self.assertEqual(self.module_a.data[2].name, "Charlie")

    @patch("builtins.open", new_callable=mock_open, read_data="Alice,123\nBob,456\nCharlie,789\n")
    def test_data_update(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        self.module_d.updateData = MagicMock(return_value=[Entry("Alice", "123"), Entry("Bob", "456"), Entry("Charlie", "890")])
        self.module_a.parseUpdate(3, "Charlie", "890")
        self.assertEqual(self.module_a.data[2].number, "890")

    @patch("builtins.open", new_callable=mock_open, read_data="Bob,456\nAlice,123\nCharlie,890\n")
    def test_data_sorting_and_display(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        self.module_c.sortData = MagicMock(return_value=[Entry("Alice", "123"), Entry("Bob", "456"), Entry("Charlie", "890")])
        self.module_a.runSort()
        self.assertEqual(self.module_a.data[0].name, "Alice")
        self.assertEqual(self.module_a.data[1].name, "Bob")

    @patch("builtins.open", new_callable=mock_open, read_data="Alice,123\nBob,456\nCharlie,890\n")
    def test_data_delete_and_display(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        self.module_d.deleteData = MagicMock(return_value=[Entry("Alice", "123"), Entry("Charlie", "890")])
        self.module_a.parseDelete(2)
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[1].name, "Charlie")

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            self.module_a.runExit()

    def test_invalid_commands(self):
        with patch("builtins.print") as mock_print:
            self.module_a.run("unknown_command")
            mock_print.assert_called_with("Unknown command, type 'help' for command list.")

    def test_nonexistent_file(self):
        with patch("builtins.print") as mock_print:
            self.module_a.parseLoad("nonexistent_file.txt")
            mock_print.assert_called_with("FileNotFoundError")

    @patch("builtins.open", new_callable=mock_open, read_data="Alice,123\nBob,456\nCharlie,890\n")
    def test_invalid_index_in_update_and_delete(self, mock_file):
        self.module_a.parseLoad("mock_file.txt")
        with patch("builtins.print") as mock_print:
            # Test invalid index for update
            self.module_a.parseUpdate(10, "NewName", "NewNumber")
            mock_print.assert_called_with("Malformed command!")

            # Test invalid index for delete
            self.module_a.parseDelete(10)
            mock_print.assert_called_with("Malformed command!")


