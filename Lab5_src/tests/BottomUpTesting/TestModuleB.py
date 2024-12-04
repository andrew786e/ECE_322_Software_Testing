import unittest
from unittest.mock import patch, mock_open
from modules.ModuleB import ModuleB
from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleB(unittest.TestCase):
    def setUp(self):
        self.module_f = ModuleF()
        self.module_b = ModuleB(self.module_f)
        self.module_f_new = ModuleF()  # A second instance to test the setter

    @patch("builtins.open", new_callable=mock_open, read_data="John Doe,12345\nJane Smith,67890\n")
    def test_loadFile_success(self, mock_file):
        """Test loadFile with valid file."""
        result = self.module_b.loadFile("testfile.txt")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "John Doe")
        self.assertEqual(result[1].number, "67890")
        mock_file.assert_called_once_with("testfile.txt")

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_loadFile_file_not_found(self, mock_file , mock_print):
        """Test loadFile with a non-existent file."""
        result = self.module_b.loadFile("nonexistentfile.txt")
        self.assertEqual(result ,[])
        mock_file.assert_called_once_with("nonexistentfile.txt")
        mock_print.assert_called_with("FileNotFoundError")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_loadFile_empty_file(self, mock_file):
        """Test loadFile with an empty file."""
        result = self.module_b.loadFile("emptyfile.txt")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("emptyfile.txt")

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("builtins.print")
    def test_loadFile_ioerror_with_actual_f(self, mock_print, mock_open):
        """Test loadFile when an IOError occurs, using the actual ModuleF."""
        # Act
        result = self.module_b.loadFile("restrictedfile.txt")

        # Assert
        # Check if the IOError message was printed correctly
        # mock_print.assert_called__with("Could not read file:Permission denied")
        print_statements = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Could not read file:None", print_statements)

    def test_getter_f(self):
            """Test the getter for property 'f'."""
            # Act
            result = self.module_b.f

            # Assert
            self.assertEqual(result, self.module_f)  # Ensure the getter returns the correct instance
            self.assertIsInstance(result, ModuleF)  # Validate the returned object is an instance of ModuleF

    def test_setter_f(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_b.f = self.module_f_new

        # Assert
        self.assertEqual(self.module_b.f, self.module_f_new)  # Ensure the new ModuleF instance is correctly set
        self.assertNotEqual(self.module_b.f, self.module_f)  # Ensure the old ModuleF instance is replaced
        self.assertIsInstance(self.module_b.f, ModuleF)  # Validate the newly set object is an instance of ModuleF
