import unittest
from unittest.mock import Mock, patch
from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE
from data.Entry import Entry  # Assuming Entry is located in the `modules` package.

class TestModuleA(unittest.TestCase):
    def setUp(self):
        self.mock_b = Mock()
        self.mock_c = Mock()
        self.mock_d = Mock()
        self.mock_e = Mock()
        self.module_a = ModuleA(self.mock_b, self.mock_c, self.mock_d, self.mock_e)

    # 2. Test parseDelete when the index is within the given range and data has been loaded
    def test_parseDelete_success(self):
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "textfile.txt"
        self.mock_d.deleteData.return_value = [Entry("John Doe", "12345")]
        result = self.module_a.parseDelete(2)
        self.mock_d.deleteData.assert_called_once_with(
            [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")], 1,"textfile.txt"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.module_a._data), 1)
        self.assertEqual(self.module_a._data[0].name, "John Doe")

    # 3. Test the parse delete function when the index is outside the valid range and data has been loaded
    def test_parseDelete_failure_index(self):
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "textfile.txt"
        self.mock_d.deleteData.return_value = None
        result = self.module_a.parseDelete(5)
        self.mock_d.deleteData.assert_called_once_with(
            [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")], 4,"textfile.txt"
        )
        self.assertFalse(result)

    # 4.Test the parse delete function when no data has been loaded
    def test_parseDelete_failure_no_data(self):
        self.module_a._filename = "test.txt"
        self.mock_d.deleteData.return_value = None
        result = self.module_a.parseDelete(4)
        self.mock_d.deleteData.assert_called_once_with(
            None, 3,"test.txt"
        )
        self.assertFalse(result)
        self.assertEqual(self.module_a._data, None)

    #5. Test the displayHelp function to show the commands that are available
    @patch('builtins.print')
    def test_displayHelp(self, mocked_print):
        # Call the displayHelp method
        return_value = self.module_a.displayHelp()

        # Assertions
        mocked_print.assert_called_once_with(
            "Available Commands: \n"
            "load <filepath>\n"
            "add <name> <number>\n"
            "update <index> <name> <number>\n"
            "delete <index>\n"
            "sort\n"
            "exit"
        )
        self.assertTrue(return_value)  # Assert the method returns True

    #6. Test the parseLoad function when a valid file path has been given
    def test_parseLoad_success_valid_file_path(self):
        # Mock the return value with a list of Entry objects
        self.mock_b.loadFile.return_value = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        result = self.module_a.parseLoad("testfile.txt")
        self.mock_b.loadFile.assert_called_once_with("testfile.txt")
        self.assertTrue(result)
        self.assertEqual(len(self.module_a._data), 2)
        self.assertEqual(self.module_a._data[0].name, "John Doe")
        self.assertEqual(self.module_a._data[0].number, "12345")

    #7. Test the parseLoad function when an invalid file path has been given
    def test_parseLoad_success_invalid_file_path(self):
        # Mock the return value with a list of Entry objects
        self.mock_b.loadFile.return_value = None
        result = self.module_a.parseLoad("testfile.txt")
        self.mock_b.loadFile.assert_called_once_with("testfile.txt")
        self.assertFalse(result)
        self.assertEqual(self.module_a._data, None)

    #8. Test the parseAdd function with a valid name and number
    def test_parseAdd_success(self):
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "textfile.txt"
        self.mock_d.insertData.return_value = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        result = self.module_a.parseAdd("Jane Smith", "67890")
        self.mock_d.insertData.assert_called_once_with(
            [Entry("John Doe", "12345")], "Jane Smith", "67890","textfile.txt"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.module_a._data), 2)
        self.assertEqual(self.module_a._data[1].name, "Jane Smith")

    #9. Test the parseAdd  function with an invalid name or number
    def test_parseAdd_failure_invalid_name_number(self):
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "textfile.txt"
        self.mock_d.insertData.return_value = None
        result = self.module_a.parseAdd("Jane Smith", "67890")
        self.mock_d.insertData.assert_called_once_with(
            [Entry("John Doe", "12345")], "Jane Smith", "67890","textfile.txt"
        )
        self.assertFalse(result)
        self.assertEqual(self.module_a._data , None)

    #10. Test the sort data function when data has been loaded
    def test_runSort_success(self):
        self.module_a._data = [Entry("John", "12345") , Entry("Jane", "67890")]
        self.mock_c.sortData.return_value = [Entry("Jane", "67890") , Entry("John", "12345")]
        result = self.module_a.runSort()
        self.mock_c.sortData.assert_called_once_with(
            [Entry("John", "12345") , Entry("Jane", "67890")]
        )
        self.assertTrue(result)
        self.assertEqual(self.module_a._data[0].name, "Jane")

    # 11. Test the sort data function when data has been loaded
    def test_runSort_failure(self):
        self.module_a._data = None
        self.mock_c.sortData.return_value = None
        result = self.module_a.runSort()
        self.mock_c.sortData.assert_called_once_with(
            None
        )
        self.assertFalse(result)
        self.assertEqual(self.module_a._data, None)

    # 12. Test parseUpdate with a valid index, name, and number for a successful update.
    def test_parseUpdate_success(self):
        self.module_a._filename = "testing.txt"
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.mock_d.updateData.return_value = [Entry("John Doe", "12345"), Entry("Jane Doe", "54321")]
        result = self.module_a.parseUpdate(2, "Jane Doe", "54321")
        self.mock_d.updateData.assert_called_once_with(
            [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")], 0, "Jane Doe", "54321", "testing.txt"
        )
        self.assertTrue(result)
        self.assertEqual(self.module_a._data[1].name, "Jane Doe")
        self.assertEqual(self.module_a._data[1].number, "54321")

    # 13. Test parseUpdate with an invalid index and no data
    def test_parse_update_failure_invalid_index(self):
        self.module_a._filename = "testing.txt"
        self.module_a._data = None
        self.mock_d.updateData.return_value = None
        result = self.module_a.parseUpdate(9, "Jane Doe", "54321")
        self.mock_d.updateData.assert_called_once_with(
            None, 7, "Jane Doe", "54321", "testing.txt"
        )
        self.assertFalse(result)
        self.assertEqual(self.module_a._data, None)

    #14. Test the runExit function
    def test_runExit(self):
        self.module_a.runExit()
        self.mock_e.exitProgam.assert_called_once()

    #15. Test the setter function for the data attribute in the function
    def test_data_setter(self):
        # Create mock Entry data
        entry1 = Entry("John Doe", "12345")
        entry2 = Entry("Jane Smith", "67890")
        mock_data = [entry1, entry2]

        # Use the setter
        self.module_a.data = mock_data  # This will use the incorrect setter
        self.assertEqual(self.module_a._data, mock_data)

    #16. Test the getter function for the data attribute in the function
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

    #17. Test the run function with all the commands “help” , “load” , “add” , “sort” , “update” , “delete” , “exit”
    @patch('builtins.print')
    def test_run_help(self, mocked_print):
        self.module_a.run("help")
        mocked_print.assert_called_with(
            "Available Commands: \n"
            "load <filepath>\n"
            "add <name> <number>\n"
            "update <index> <name> <number>\n"
            "delete <index>\n"
            "sort\n"
            "exit"
        )

    def test_run_load(self):
        # Mock loadFile
        self.mock_b.loadFile.return_value = [Entry("John Doe", "12345")]

        # Test "load" command
        self.module_a.run("load", "testfile.txt")

        self.mock_b.loadFile.assert_called_once_with("testfile.txt")
        self.assertEqual(self.module_a.data, [Entry("John Doe", "12345")])
        self.assertEqual(self.module_a._filename, "testfile.txt")

    @patch('builtins.print')
    def test_run_load_index_error(self, mocked_print):
        # Call the run method with "load" but without a filename
        self.module_a.run("load")

        # Assert that the correct error message was printed
        mocked_print.assert_any_call("Malformed command!")

    def test_run_add(self):
        # Set initial data and filename
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"
        self.mock_d.insertData.return_value = [
            Entry("John Doe", "12345"),
            Entry("Jane Smith", "67890"),
        ]

        # Test "add" command
        self.module_a.run("add", "Jane Smith", "67890")

        self.mock_d.insertData.assert_called_once_with(
            [Entry("John Doe", "12345")], "Jane Smith", "67890", "testfile.txt"
        )
        self.assertEqual(len(self.module_a.data), 2)

    @patch('builtins.print')
    def test_run_add_index_error(self, mocked_print):
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"
        # Call the run method with "add" but without sufficient arguments
        self.module_a.run("add", "Jane Smith")  # Missing the second argument (number)

        # Assert that the correct error message was printed
        mocked_print.assert_any_call("Malformed command!")

    @patch('builtins.print')
    def test_run_add_no_data_loaded(self , mocked_print):
        # Set initial data and filename
        self.module_a._data = None
        self.module_a._filename = "testfile.txt"
        self.mock_d.insertData.return_value = [
            Entry("John Doe", "12345"),
            Entry("Jane Smith", "67890"),
        ]

        # Test "add" command
        self.module_a.run("add", "Jane Smith", "67890")

        mocked_print.assert_any_call("No file loaded!")


    def test_run_sort(self):
        # Set initial data
        self.module_a._data = [Entry("Jane Smith", "67890"), Entry("John Doe", "12345")]
        self.mock_c.sortData.return_value = [
            Entry("John Doe", "12345"),
            Entry("Jane Smith", "67890"),
        ]

        # Test "sort" command
        self.module_a.run("sort")

        self.mock_c.sortData.assert_called_once_with(
            [Entry("Jane Smith", "67890"), Entry("John Doe", "12345")]
        )
        self.assertEqual(self.module_a.data[0].name, "John Doe")

    @patch('builtins.print')
    def test_run_sort_no_file_loaded(self , mocked_print):
        # Set initial data
        self.module_a._data = None
        self.mock_c.sortData.return_value = [
            Entry("John Doe", "12345"),
            Entry("Jane Smith", "67890"),
        ]

        # Test "sort" command
        self.module_a.run("sort")

        mocked_print.assert_any_call("No file loaded!")



    def test_run_update(self):
        # Set initial data and filename
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"
        self.mock_d.updateData.return_value = [Entry("John Doe", "67890")]

        # Test "update" command
        self.module_a.run("update", 1, "John Doe", "67890")

        self.mock_d.updateData.assert_called_once_with(
            [Entry("John Doe", "12345")], -1, "John Doe", "67890", "testfile.txt"
        )
        self.assertEqual(self.module_a.data[0].number, "67890")

    @patch('builtins.print')
    def test_run_update_index_error(self, mocked_print):
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"

        self.module_a.run("update", 1, "John Doe")

        # Assert that the correct error message was printed
        mocked_print.assert_any_call("Malformed command!")

    @patch('builtins.print')
    def test_run_update_no_data_loaded(self , mocked_print):
        self.module_a._data = None
        self.module_a._filename = "testfile.txt"
        self.mock_d.updateData.return_value = [Entry("John Doe", "67890")]

        # Test "update" command
        self.module_a.run("update", 1, "John Doe", "67890")
        mocked_print.assert_any_call("No file loaded!")

    def test_run_delete(self):
        # Set initial data and filename
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "testfile.txt"
        self.mock_d.deleteData.return_value = [Entry("Jane Smith", "67890")]

        # Test "delete" command
        self.module_a.run("delete", 1)

        self.mock_d.deleteData.assert_called_once_with(
            [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")], 0, "testfile.txt"
        )
        self.assertEqual(len(self.module_a.data), 1)
        self.assertEqual(self.module_a.data[0].name, "Jane Smith")

    @patch('builtins.print')
    def test_run_delete_index_error(self, mocked_print):
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"

        self.module_a.run("delete")

        # Assert that the correct error message was printed
        mocked_print.assert_any_call("Malformed command!")

    @patch('builtins.print')
    def test_run_delete_no_file_loaded(self , mocked_print):
        # Set initial data and filename
        self.module_a._data = None
        self.module_a._filename = "testfile.txt"
        self.mock_d.deleteData.return_value = [Entry("Jane Smith", "67890")]

        # Test "delete" command
        self.module_a.run("delete", 1)

        mocked_print.assert_any_call("No file loaded!")

    def test_run_exit_program(self):
        # Test "exit" command
        self.module_a.run("exit")
        self.mock_e.exitProgam.assert_called_once()


    #18 Test case with invalid command
    @patch('builtins.print')
    def test_run_wrong_command(self, mocked_print):
        self.module_a.run("wrongcommand")
        mocked_print.assert_called_with(
            "Unknown command, type 'help' for command list."
        )

    #19 Test case with no command
    @patch('builtins.print')
    def test_run_zero_command(self, mocked_print):
        self.module_a.run()
        mocked_print.assert_called_with(
            "No command passed!"
        )
