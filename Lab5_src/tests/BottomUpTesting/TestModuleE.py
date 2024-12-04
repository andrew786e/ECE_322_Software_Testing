import unittest
from unittest.mock import patch
from modules.ModuleE import ModuleE


class TestModuleE(unittest.TestCase):
    @patch("sys.exit")  # Mock sys.exit to prevent the program from exiting
    @patch("builtins.print")  # Mock print to capture the print statement
    def test_exitProgram(self, mock_print, mock_exit):
        """Test that exitProgram prints the exit message and calls sys.exit."""
        module_e = ModuleE()

        # Call the method
        module_e.exitProgram()

        # Assert that the print function was called with the correct message
        mock_print.assert_called_once_with("Program Exit !")

        # Assert that sys.exit was called once
        mock_exit.assert_called_once()


