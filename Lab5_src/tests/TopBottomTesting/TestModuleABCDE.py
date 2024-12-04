import unittest
from unittest.mock import Mock
from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE
from unittest.mock import Mock, patch , mock_open
from data.Entry import Entry

class TestModuleABCDE(unittest.TestCase):
    def setUp(self):
        # Mocks for ModuleF and ModuleG
        self.mock_f = Mock()
        self.mock_g = Mock()
        self.mock_f_new = Mock()
        self.mock_g_new = Mock()

        # Real implementations of Modules B, C, D, E
        self.module_b = ModuleB(self.mock_f)
        self.module_c = ModuleC(self.mock_f)
        self.module_d = ModuleD(self.mock_f, self.mock_g)
        self.module_e = ModuleE()

        # Initialize ModuleA with mixed dependencies
        self.module_a = ModuleA(self.module_b, self.module_c, self.module_d, self.module_e)

    @patch("builtins.open", new_callable=mock_open, read_data="John Doe,12345\nJane Smith,67890\n")
    def test_parseLoad_success_module_b(self, mock_file):
        """Test parseLoad with a valid file and actual ModuleB."""
        # Act
        result = self.module_a.parseLoad("testfile.txt")

        # Assert
        self.assertTrue(result)
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[0].name, "John Doe")
        self.assertEqual(self.module_a.data[1].number, "67890")
        mock_file.assert_called_once_with("testfile.txt")
        self.mock_f.displayData.assert_called_once_with(self.module_a.data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_parseLoad_failure_module_b(self, mock_file , mock_print):
        """Test parseLoad with a non-existent file and actual ModuleB."""
        # Act
        result = self.module_a.parseLoad("nonexistentfile.txt")

        # Assert
        self.assertTrue(result)
        self.assertEqual(self.module_a.data , [])
        mock_file.assert_called_once_with("nonexistentfile.txt")
        mock_print.assert_called_once_with("FileNotFoundError")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_parseLoad_empty_file_module_b(self, mock_file):
        """Test parseLoad with an empty file and actual ModuleB."""
        # Act
        result = self.module_a.parseLoad("emptyfile.txt")

        # Assert
        self.assertTrue(result)
        self.assertEqual(self.module_a.data, [])
        mock_file.assert_called_once_with("emptyfile.txt")
        self.mock_f.displayData.assert_called_once_with([])

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("builtins.print")
    def test_parseLoad_ioerror_module_b(self, mock_print, mock_file):
        """Test parseLoad with a file that causes IOError and validate the print message."""
        # Act
        result = self.module_a.parseLoad("restrictedfile.txt")

        # Assert
        self.assertTrue(result)
        self.assertEqual(self.module_a.data, [])
        mock_file.assert_called_once_with("restrictedfile.txt")

        # Validate that an appropriate message is printed
        mock_print.assert_called_once_with("Could not read file:{0.filename}".format(IOError("Permission denied")))

    @patch("builtins.open", new_callable=mock_open, read_data="John Doe,12345\nInvalidDataLine\nJane Smith,67890\n")
    @patch("builtins.print")
    def test_parseLoad_invalid_data_format_module_b(self, mock_print, mock_file):
        """Test parseLoad with a file containing invalid data format."""
        # Act
        result = self.module_a.parseLoad("testfile.txt")

        # Assert
        self.assertTrue(result)  # Ensure the method returns True (partially successful load)
        self.assertEqual(len(self.module_a.data), 2)  # Only valid entries should be loaded
        self.assertEqual(self.module_a.data[0].name, "John Doe")
        self.assertEqual(self.module_a.data[1].name, "Jane Smith")
        mock_file.assert_called_once_with("testfile.txt")

    def test_getter_f_module_b(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_b.f

        # Assert
        self.assertEqual(result, self.mock_f)
        self.assertIsInstance(result, Mock)
        self.assertTrue(hasattr(result, "displayData"))  # Ensure it has the expected method

    def test_setter_f_module_b(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_b.f = self.mock_f_new

        # Assert
        self.assertEqual(self.module_b.f, self.mock_f_new)
        self.assertNotEqual(self.module_b.f, self.mock_f)
        self.assertIsInstance(self.module_b.f, Mock)


    def test_runSort_success_module_c(self):
        """Test runSort with valid data and real ModuleC."""
        # Arrange
        self.module_a._data = [
            Entry("Zara", "45678"),
            Entry("Anna", "12345"),
            Entry("John", "67890"),
        ]

        # Act
        result = self.module_a.runSort()

        # Assert
        self.assertTrue(result)
        self.assertEqual(len(self.module_a.data), 3)
        self.assertEqual(self.module_a.data[0].name, "Anna")
        self.assertEqual(self.module_a.data[1].name, "John")
        self.assertEqual(self.module_a.data[2].name, "Zara")
        self.mock_f.displayData.assert_called_once_with(self.module_a.data)

    def test_runSort_empty_data_module_c(self):
        """Test runSort with empty data."""
        # Arrange
        self.module_a._data = []

        # Act
        result = self.module_a.runSort()

        # Assert
        self.assertTrue(result)  # Should still return True for empty data
        self.assertEqual(self.module_a.data, [])
        self.mock_f.displayData.assert_called_once_with([])

    def test_getter_f_module_c(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_c.f

        # Assert
        self.assertEqual(result, self.mock_f)
        self.assertIsInstance(result, Mock)
        self.assertTrue(hasattr(result, "displayData"))  # Ensure it has the expected method

    def test_setter_f_module_c(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_c.f = self.mock_f_new

        # Assert
        self.assertEqual(self.module_c.f, self.mock_f_new)
        self.assertNotEqual(self.module_c.f, self.mock_f)
        self.assertIsInstance(self.module_c.f, Mock)

    def test_parseAdd_success_module_d(self):
        """Test parseAdd with valid name and number."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"

        # Act
        result = self.module_a.parseAdd("Jane Smith", "67890")

        # Assert
        self.assertTrue(result)
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[1].name, "Jane Smith")
        self.assertEqual(self.module_a.data[1].number, "67890")
        self.mock_f.displayData.assert_called_once()
        self.mock_g.updateData.assert_called_once()

    def test_parseUpdate_success_module_d(self):
        """Test parseUpdate with a valid index, name, and number."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "testfile.txt"

        # Act
        result = self.module_a.parseUpdate(2, "Jane Doe", "54321")

        # Assert
        self.assertTrue(result)
        self.assertEqual(len(self.module_a.data), 2)
        self.assertEqual(self.module_a.data[1].name, "Jane Doe")
        self.assertEqual(self.module_a.data[1].number, "54321")
        self.mock_f.displayData.assert_called_once_with(self.module_a.data)
        self.mock_g.updateData.assert_called_once_with("testfile.txt", self.module_a.data)

    def test_parseDelete_success_module_d(self):
        """Test parseDelete with a valid index."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        self.module_a._filename = "testfile.txt"

        # Act
        result = self.module_a.parseDelete(2)

        # Assert
        self.assertTrue(result)
        self.assertEqual(len(self.module_a.data), 1)
        self.assertEqual(self.module_a.data[0].name, "John Doe")
        self.mock_f.displayData.assert_called_once_with(self.module_a.data)
        self.mock_g.updateData.assert_called_once_with("testfile.txt", self.module_a.data)

    def test_parseDelete_invalid_index_module_d(self):
        """Test parseDelete with an invalid index."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"

        # Act
        with self.assertRaises(IndexError):
            self.module_a.parseDelete(5)  # Invalid index

    def test_parseUpdate_invalid_index_module_d(self):
        """Test parseUpdate with an invalid index."""
        # Arrange
        self.module_a._data = [Entry("John Doe", "12345")]
        self.module_a._filename = "testfile.txt"

        # Act
        with self.assertRaises(IndexError):
            self.module_a.parseUpdate(5, "Jane Doe", "54321")

    def test_getter_f_module_d(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_d.f

        # Assert
        self.assertEqual(result, self.mock_f)
        self.assertIsInstance(result, Mock)

    def test_setter_f_module_d(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_d.f = self.mock_f_new

        # Assert
        self.assertEqual(self.module_d.f, self.mock_f_new)
        self.assertNotEqual(self.module_d.f, self.mock_f)
        self.assertIsInstance(self.module_d.f, Mock)

    def test_getter_g_module_d(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_d._g

        # Assert
        self.assertEqual(result, self.mock_g)
        self.assertIsInstance(result, Mock)

    def test_setter_g_module_d(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_d.g = self.mock_g_new

        # Assert
        self.assertEqual(self.module_d.g , self.mock_g_new)
        self.assertNotEqual(self.module_d.g, self.mock_g)
        self.assertIsInstance(self.module_d.g, Mock)

    @patch("sys.exit")  # Mock sys.exit to prevent the program from exiting
    @patch("builtins.print")  # Mock print to capture the print statement
    def test_exitProgram_module_e(self, mock_print, mock_exit):
        """Test that exitProgram prints the exit message and calls sys.exit."""
        self.module_a.runExit()

        # Assert that the print function was called with the correct message
        mock_print.assert_called_once_with("Program Exit !")

        # Assert that sys.exit was called once
        mock_exit.assert_called_once()

    @patch("sys.exit")  # Mock sys.exit to prevent the program from exiting
    @patch("builtins.print")  # Mock print to capture the print statement
    def test_exitProgram_module_e_individual(self, mock_print, mock_exit):
        """Test that exitProgram prints the exit message and calls sys.exit."""
        self.module_e.exitProgram()

        # Assert that the print function was called with the correct message
        mock_print.assert_called_once_with("Program Exit !")

        # Assert that sys.exit was called once
        mock_exit.assert_called_once()
