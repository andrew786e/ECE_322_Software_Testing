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


class TestModuleABCDEFG(unittest.TestCase):
    def setUp(self):
        # Initialize real modules
        self.module_f = ModuleF()
        self.module_g = ModuleG()
        self.module_b = ModuleB(self.module_f)
        self.module_c = ModuleC(self.module_f)
        self.module_d = ModuleD(self.module_f, self.module_g)
        self.module_e = ModuleE()

        # Initialize ModuleA with all real modules
        self.module_a = ModuleA(self.module_b, self.module_c, self.module_d, self.module_e)

    @patch("builtins.open", new_callable=mock_open, read_data="John Doe,12345\nJane Smith,67890\n")
    def test_run_load(self, mock_file):
        """Test 'load' command."""
        # Act
        self.module_a.run("load", "testfile.txt")

        # Assert
        self.assertIsNotNone(self.module_a.data)
        self.assertEqual(len(self.module_a.data), 2)
        mock_file.assert_called_once_with("testfile.txt")

    @patch("builtins.print")
    def test_run_load_malformed_command(self, mock_print):
        """Test 'load' command with malformed input."""
        # Act
        self.module_a.run("load")

        # Assert
        mock_print.assert_any_call("Malformed command!")

    def test_run_add(self):
        """Test 'add' command."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        self.module_a.run("add", "Jane Smith", "67890")

        # Assert
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[1].name, "Jane Smith")
        self.assertEqual(self.module_a.data[1].number, "67890")

    @patch("builtins.print")
    def test_run_add_malformed_command(self, mock_print):
        """Test 'add' command with malformed input."""
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a.run("add", "Jane Smith")  # Missing phone number
        mock_print.assert_any_call("Malformed command!")

    def test_run_update(self):
        """Test 'update' command."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        self.module_a.run("update", 1, "Jane Smith", "67890")

        # Assert
        self.assertEqual(self.module_a.data[0].name, "Jane Smith")
        self.assertEqual(self.module_a.data[0].number, "67890")

    @patch("builtins.print")
    def test_run_update_malformed_command(self, mock_print):
        """Test 'update' command with malformed input."""
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a.run("update", 1, "Jane Smith")  # Missing phone number
        mock_print.assert_any_call("Malformed command!")

    def test_run_delete(self):
        """Test 'delete' command."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        self.module_a.run("delete", 1)

        # Assert
        self.assertEqual(len(self.module_a.data), 1)
        self.assertEqual(self.module_a.data[0].name, "Jane Smith")

    @patch("builtins.print")
    def test_run_delete_malformed_command(self, mock_print):
        self.module_a._data = [Entry("John Doe", "12345")]
        """Test 'delete' command with malformed input."""
        self.module_a.run("delete")  # Missing index
        mock_print.assert_any_call("Malformed command!")

    def test_run_sort(self):
        """Test 'sort' command."""
        # Arrange
        self.module_a._data = [Entry("Zara", "12345"), Entry("Anna", "67890")]

        # Act
        self.module_a.run("sort")

        # Assert
        self.assertEqual(self.module_a.data[0].name, "Anna")
        self.assertEqual(self.module_a.data[1].name, "Zara")

    @patch("builtins.print")
    def test_run_sort_no_data(self, mock_print):
        """Test 'sort' command with no data loaded."""
        self.module_a.data = None
        self.module_a.run("sort")
        mock_print.assert_any_call("No file loaded!")

    @patch("builtins.print")
    def test_run_help(self, mock_print):
        """Test 'help' command."""
        self.module_a.run("help")
        mock_print.assert_called_with(
            "Available Commands: \n"
            "load <filepath>\n"
            "add <name> <number>\n"
            "update <index> <name> <number>\n"
            "delete <index>\n"
            "sort\n"
            "exit"
        )

    @patch("builtins.print")
    def test_run_unknown_command(self, mock_print):
        """Test unknown command."""
        self.module_a.run("unknown")
        mock_print.assert_called_with("Unknown command, type 'help' for command list.")

    @patch("builtins.print")
    def test_run_no_command(self, mock_print):
        """Test no command passed."""
        self.module_a.run()
        mock_print.assert_called_with("No command passed!")

    @patch("builtins.print")
    def test_run_exit(self, mock_print):
        """Test 'exit' command."""
        with self.assertRaises(SystemExit):
            self.module_a.run("exit")

    @patch("builtins.print")
    def test_parseAdd_with_f_and_g(self, mock_print):
        """Test parseAdd ensuring ModuleF and ModuleG are invoked correctly."""
        # Arrange
        self.module_a._data =  [Entry("John Doe", "12345")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        result = self.module_a.parseAdd("Jane Smith", "67890")

        expected_calls = [
            unittest.mock.call("Current Data:"),
            unittest.mock.call("----------------------------------------------------------"),
            unittest.mock.call("1 John Doe, 12345"),
            unittest.mock.call("2 Jane Smith, 67890"),
            unittest.mock.call("----------------------------------------------------------"),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch("builtins.print")
    def test_parseUpdate_with_f_and_g(self, mock_print):
        """Test parseUpdate ensuring ModuleF and ModuleG are invoked correctly."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        result = self.module_a.parseUpdate(2, "Jane Doe", "54321")

        expected_calls = [
            unittest.mock.call("Current Data:"),
            unittest.mock.call("----------------------------------------------------------"),
            unittest.mock.call("1 John Doe, 12345"),
            unittest.mock.call("2 Jane Doe, 54321"),
            unittest.mock.call("----------------------------------------------------------"),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)


    @patch("builtins.print")
    def test_parseDelete_with_f_and_g(self, mock_print):
        """Test parseDelete ensuring ModuleF and ModuleG are invoked correctly."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "../TopBottomTesting/testfile.txt"

        # Act
        result = self.module_a.parseDelete(2)

        expected_calls = [
            unittest.mock.call("Current Data:"),
            unittest.mock.call("----------------------------------------------------------"),
            unittest.mock.call("1 John Doe, 12345"),
            unittest.mock.call("----------------------------------------------------------"),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch("builtins.print")
    def test_f_displayData_called_directly(self , mock_print):
        """Test that ModuleF's displayData works when called directly."""
        self.module_a._data = [Entry("John", "12345"), Entry("Doe", "67890")]
        # Act
        self.module_a._d.f.displayData(self.module_a._data)

        # Assert
        self.module_f.displayData(self.module_a._data)

        # Verify the header and footer
        mock_print.assert_any_call("Current Data:")
        mock_print.assert_any_call("----------------------------------------------------------")
        mock_print.assert_any_call("1 John, 12345")
        mock_print.assert_any_call("2 Doe, 67890")
        mock_print.assert_any_call("----------------------------------------------------------")

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_file_not_found_in_updateData(self, mock_print, mock_open):
        """Test ModuleG.updateData raises FileNotFoundError and is handled correctly."""
        self.module_a._data = [Entry("John", "12345"), Entry("Doe", "67890")]

        # Act
        result = self.module_a.parseAdd("Alice Brown", "11223")

        # Assert
        self.assertTrue(result)  # Data modification should still succeed
        self.assertEqual(len(self.module_a.data), 3)  # Ensure new entry is added
        self.assertEqual(self.module_a.data[-1].name, "Alice Brown")
        self.assertEqual(self.module_a.data[-1].number, "11223")

        # Validate the print call for the error message
        mock_print.assert_called_with("Error updating DB File.")

    def test_data_setter(self):
        # Create mock Entry data
        entry1 = Entry("John Doe", "12345")
        entry2 = Entry("Jane Smith", "67890")
        mock_data = [entry1, entry2]

        # Use the setter
        self.module_a.data = mock_data  # This will use the incorrect setter
        self.assertEqual(self.module_a._data, mock_data)

    # 16. Test the getter function for the data attribute in the function
    def test_data_getter(self):
        # Create mock Entry data
        entry1 = Entry("John Doe", "12345")
        entry2 = Entry("Jane Smith", "67890")
        self.module_a._data = [entry1, entry2]

        # Use the getter to retrieve data
        result = self.module_a.data

        # Assert that the getter returns the correct data
        self.assertEqual(result, [entry1, entry2], "Getter did not return the expected list of entries")

        # Additional checks for individual entries
        self.assertEqual(result[0].name, "John Doe", "First entry name mismatch")
        self.assertEqual(result[0].number, "12345", "First entry number mismatch")
        self.assertEqual(result[1].name, "Jane Smith", "Second entry name mismatch")
        self.assertEqual(result[1].number, "67890", "Second entry number mismatch")
