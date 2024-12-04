import unittest
from unittest.mock import Mock
from modules.ModuleD import ModuleD
from data.Entry import Entry

class TestModuleDWithMocks(unittest.TestCase):
    def setUp(self):
        # Use mocks instead of stubs
        self.mock_f = Mock()
        self.mock_g = Mock()
        self.module_d = ModuleD(f=self.mock_f, g=self.mock_g)

        # Example data
        self.data = [
            Entry("John", "123456"),
            Entry("Doe", "789101"),
        ]
        self.filename = "testfile.txt"

    def test_insert_data(self):
        """Test that insertData adds a new Entry."""
        # Mock the updateData method in ModuleG
        self.mock_g.updateData.return_value = None  # Simulate a successful file update

        updated_data = self.module_d.insertData(self.data, "Alice", "111222", self.filename)

        # Check that the new entry is added
        self.assertEqual(len(updated_data), 3)
        self.assertEqual(updated_data[-1].name, "Alice")
        self.assertEqual(updated_data[-1].number, "111222")

        # Verify that updateData in ModuleG is called
        self.mock_g.updateData.assert_called_once_with(self.filename, updated_data)

    def test_update_data(self):
        """Test that updateData modifies the correct Entry."""
        # Mock the updateData method in ModuleG
        self.mock_g.updateData.return_value = None  # Simulate a successful file update

        updated_data = self.module_d.updateData(self.data, 0, "Johnathan", "654321", self.filename)

        # Check that the correct entry is updated
        self.assertEqual(updated_data[0].name, "Johnathan")
        self.assertEqual(updated_data[0].number, "654321")

        # Verify that updateData in ModuleG is called
        self.mock_g.updateData.assert_called_once_with(self.filename, updated_data)

    def test_delete_data(self):
        """Test that deleteData removes the correct Entry."""
        # Mock the updateData method in ModuleG
        self.mock_g.updateData.return_value = None  # Simulate a successful file update

        updated_data = self.module_d.deleteData(self.data, 0, self.filename)

        # Check that the correct entry is deleted
        self.assertEqual(len(updated_data), 1)
        self.assertEqual(updated_data[0].name, "Doe")
        self.assertEqual(updated_data[0].number, "789101")

        # Verify that updateData in ModuleG is called
        self.mock_g.updateData.assert_called_once_with(self.filename, updated_data)

    def test_delete_data_out_of_range(self):
        """Test that deleteData handles out-of-range index gracefully."""
        updated_data = self.module_d.deleteData(self.data, 5, self.filename)

        # Check that the data remains unchanged
        self.assertEqual(updated_data, self.data)

        # Verify that updateData is not called due to the out-of-range index
        self.mock_g.updateData.assert_not_called()

    def test_get_f(self):
        """Test the getter for property 'f'."""
        self.assertEqual(self.module_d.f, self.mock_f)  # Ensure the getter returns the correct mock

    def test_set_f(self):
        """Test the setter for property 'f'."""
        new_mock_f = Mock()  # Create a new mock for ModuleF
        self.module_d.f = new_mock_f  # Set the new mock
        self.assertEqual(self.module_d.f, new_mock_f)  # Verify that the setter works

    def test_get_g(self):
        """Test the getter for property 'g'."""
        self.assertEqual(self.module_d.g, self.mock_g)  # Ensure the getter returns the correct mock

    def test_set_g(self):
        """Test the setter for property 'g'."""
        new_mock_g = Mock()  # Create a new mock for ModuleG
        self.module_d.g = new_mock_g  # Set the new mock
        self.assertEqual(self.module_d.g, new_mock_g)  # Verify that the setter works

    def test_constructor(self):
        """Test that the constructor initializes properties correctly."""
        # Verify the constructor initializes the 'f' and 'g' properties
        self.assertEqual(self.module_d.f, self.mock_f)  # Check that 'f' is set correctly
        self.assertEqual(self.module_d.g, self.mock_g)  # Check that 'g' is set correctly

