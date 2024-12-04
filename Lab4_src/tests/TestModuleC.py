import unittest
from unittest.mock import Mock
from modules.ModuleC import ModuleC
from data.Entry import Entry

class TestModuleC(unittest.TestCase):
    def setUp(self):
        # Create a mock for ModuleF
        self.mock_f = Mock()
        self.module_c = ModuleC(f=self.mock_f)

        # Example data for testing
        self.data = [
            Entry("Charlie", "123456"),
            Entry("Alice", "789101"),
            Entry("Bob", "654321"),
        ]

    #2. Test whether data is sorted appropriately by name
    def test_sort_data(self):
        """Test that sortData correctly sorts data by the 'name' attribute."""
        sorted_data = self.module_c.sortData(self.data)

        # Verify the data is sorted by name
        self.assertEqual(sorted_data[0].name, "Alice")
        self.assertEqual(sorted_data[1].name, "Bob")
        self.assertEqual(sorted_data[2].name, "Charlie")

        # Verify that displayData was called with the sorted data
        self.mock_f.displayData.assert_called_once_with(sorted_data)

    #3. Test the moduleF getter
    def test_get_f(self):
        """Test the getter for property 'f'."""
        # Verify that the 'f' property returns the correct object
        self.assertEqual(self.module_c.f, self.mock_f)

    #4. Test the moduleF setter
    def test_set_f(self):
        """Test the setter for property 'f'."""
        # Create a new Mock object for ModuleF
        new_mock_f = Mock()

        # Use the setter to assign a new value to 'f'
        self.module_c.f = new_mock_f

        # Verify that the 'f' property returns the new mock object
        self.assertEqual(self.module_c.f, new_mock_f)

    # 2. Test whether data is sorted appropriately by name
    def test_sort_data_calls_display(self):
        """Test that sortData calls displayData with the sorted list."""
        # Call sortData
        sorted_data = self.module_c.sortData(self.data)

        # Verify that displayData was called with the sorted data
        self.mock_f.displayData.assert_called_once_with(sorted_data)