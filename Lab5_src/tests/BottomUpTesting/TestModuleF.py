import unittest
from unittest.mock import patch
from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleF(unittest.TestCase):
    def setUp(self):
        self.module_f = ModuleF()

    @patch("builtins.print")
    def test_display_normal_data(self, mock_print):
        """Test displayData with normal data."""
        data = ["John", "Doe", "Alice"]
        self.module_f.displayData(data)

        # Verify header and footer
        mock_print.assert_any_call("Current Data:")
        mock_print.assert_any_call("----------------------------------------------------------")
        mock_print.assert_any_call("1 John")
        mock_print.assert_any_call("2 Doe")
        mock_print.assert_any_call("3 Alice")

    @patch("builtins.print")
    def test_display_empty_data(self, mock_print):
        """Test displayData with an empty list."""
        data = []
        self.module_f.displayData(data)

        # Verify header and footer are printed
        mock_print.assert_any_call("Current Data:")
        mock_print.assert_any_call("----------------------------------------------------------")
        mock_print.assert_any_call("----------------------------------------------------------")

        # Verify no data entries are printed
        self.assertEqual(mock_print.call_count, 3)

    @patch("builtins.print")
    def test_display_custom_objects(self, mock_print):
        """Test displayData with objects that have custom __str__."""

        class CustomObject:
            def __str__(self):
                return "CustomObject"

        data = [CustomObject(), CustomObject()]
        self.module_f.displayData(data)

        # Verify header and footer
        mock_print.assert_any_call("Current Data:")
        mock_print.assert_any_call("----------------------------------------------------------")

        # Verify data entries with their index
        mock_print.assert_any_call("1 CustomObject")
        mock_print.assert_any_call("2 CustomObject")

    @patch("builtins.print")
    def test_display_data(self, mock_print):
        """Test displayData with Entry objects."""
        module_f = ModuleF()
        data = [
            Entry("John", "123456"),
            Entry("Doe", "789101")
        ]
        module_f.displayData(data)

        # Verify the header and footer
        mock_print.assert_any_call("Current Data:")
        mock_print.assert_any_call("----------------------------------------------------------")
        mock_print.assert_any_call("1 John, 123456")
        mock_print.assert_any_call("2 Doe, 789101")
        mock_print.assert_any_call("----------------------------------------------------------")

        # Verify the number of print calls
        self.assertEqual(mock_print.call_count, 5)

