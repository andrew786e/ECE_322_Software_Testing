import unittest
from modules.ModuleB import ModuleB
from data.Entry import Entry
from unittest.mock import mock_open, patch , Mock
from modules.ModuleF import ModuleF


class TestModuleB(unittest.TestCase):
    def setUp(self):
        # Use a stub for ModuleF
        self.stub_f = Mock()
        self.module_b = ModuleB(f=self.stub_f)

    #4. Test loadFile with a valid filename containing correctly formatted data entries.
    def test_load_file_success(self):
        """Test loadFile successfully loads data from a file."""
        mock_data = "John,123456\nAlice,789101\nBob,654321\n"
        expected_data = [
            Entry("John", "123456"),
            Entry("Alice", "789101"),
            Entry("Bob", "654321"),
        ]

        # Mock the file read operation
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = self.module_b.loadFile("dummy.txt")

        # Verify the data loaded correctly
        self.assertEqual(len(result), len(expected_data))
        for r, e in zip(result, expected_data):
            self.assertEqual(r.name, e.name)
            self.assertEqual(r.number, e.number)

        # Verify that displayData was called with the loaded data
        self.stub_f.displayData.assert_called_once_with(result)

    #5. Test loadFile with a file that has incorrectly formatted lines to ensure only valid entries are loaded.
    def test_load_file_invalid_format(self):
        """Test loadFile skips invalid lines in the file."""
        mock_data = "John,123456\nInvalidLine\nAlice,789101\n"
        expected_data = [
            Entry("John", "123456"),
            Entry("Alice", "789101"),
        ]

        # Mock the file read operation
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = self.module_b.loadFile("dummy.txt")

        # Verify only valid lines are loaded
        self.assertEqual(len(result), len(expected_data))
        for r, e in zip(result, expected_data):
            self.assertEqual(r.name, e.name)
            self.assertEqual(r.number, e.number)

        # Verify that displayData was called with the loaded data
        self.stub_f.displayData.assert_called_once_with(result)

    #6. Test loadFile with a nonexistent file to check FileNotFoundError handling.
    def test_load_file_file_not_found(self):
        """Test loadFile handles FileNotFoundError."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("builtins.print") as mock_print:
                result = self.module_b.loadFile("nonexistent.txt")

        # Verify that FileNotFoundError was handled
        mock_print.assert_called_once_with("FileNotFoundError")

    #7. Test loadFile with a file that has no read permissions to check IOError handling.
    def test_load_file_io_error(self):
        """Test loadFile handles IOError."""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            with patch("builtins.print") as mock_print:
                result = self.module_b.loadFile("dummy.txt")

        # Verify that IOError was handled
        mock_print.assert_called_once_with("Could not read file:{0.filename}".format(IOError("Permission denied")))

        # Verify that an empty list is returned
        self.assertEqual(result, [])

        # Verify that displayData was not called
        self.stub_f.displayData.assert_called()

    #3. Test the getter function of Module F in Module B
    def test_getter_f(self):
        """Test the getter for property f"""
        # Mock ModuleF instance
        mock_f = Mock(spec=ModuleF)
        self.module_b._f = mock_f  # Set the mock directly

        # Retrieve the property
        result = self.module_b.f
        self.assertEqual(result, mock_f, "Getter did not return the expected ModuleF instance")

    #4. Test the setter function of Module F in Module B
    def test_setter_f(self):
        """Test the setter for property f"""
        # Mock ModuleF instance
        mock_f = Mock(spec=ModuleF)

        # Set the property
        self.module_b.f = mock_f

        # Verify that the internal attribute was updated
        self.assertEqual(self.module_b._f, mock_f, "Setter did not correctly update the ModuleF instance")
