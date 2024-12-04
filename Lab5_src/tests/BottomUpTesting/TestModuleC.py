import unittest
from modules.ModuleC import ModuleC
from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleC(unittest.TestCase):
    def setUp(self):
        self.module_f = ModuleF()
        self.module_f_new = ModuleF()
        self.module_c = ModuleC(self.module_f)

    def test_sortData_success(self):
        """Test sortData with unsorted data."""
        data = [
            Entry("Zara", "12345"),
            Entry("Anna", "67890"),
            Entry("John", "54321"),
        ]
        result = self.module_c.sortData(data)
        self.assertEqual(result[0].name, "Anna")
        self.assertEqual(result[1].name, "John")
        self.assertEqual(result[2].name, "Zara")

    def test_sortData_empty(self):
        """Test sortData with empty data."""
        data = []
        result = self.module_c.sortData(data)
        self.assertEqual(result, [])

    def test_getter_f_module_c(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_c.f

        # Assert
        self.assertEqual(result, self.module_f)

    def test_setter_f_module_c(self):
        """Test the setter for property 'f'."""
        # Act
        self.module_c.f = self.module_f_new

        # Assert
        self.assertEqual(self.module_c.f, self.module_f_new)
        self.assertNotEqual(self.module_c.f, self.module_f)

