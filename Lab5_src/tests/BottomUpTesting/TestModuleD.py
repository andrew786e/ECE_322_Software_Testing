import unittest
from modules.ModuleD import ModuleD
from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG
from data.Entry import Entry


class TestModuleD(unittest.TestCase):
    def setUp(self):
        self.module_f = ModuleF()
        self.module_g = ModuleG()
        self.module_d = ModuleD(self.module_f, self.module_g)

    def test_insertData_success(self):
        """Test insertData with valid data."""
        data = [Entry("John Doe", "12345")]
        result = self.module_d.insertData(data, "Jane Smith", "67890", "testfile.txt")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].name, "Jane Smith")
        self.assertEqual(result[1].number, "67890")

    def test_updateData_success(self):
        """Test updateData with valid data."""
        data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        result = self.module_d.updateData(data, 0, "Jane Doe", "54321", "testfile.txt")
        self.assertEqual(result[1].name, "Jane Doe")
        self.assertEqual(result[1].number, "54321")

    def test_deleteData_success(self):
        """Test deleteData with valid data."""
        data = [Entry("John Doe", "12345"), Entry("Jane Smith", "67890")]
        result = self.module_d.deleteData(data, 1, "testfile.txt")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "John Doe")

    def test_parseDelete_invalid_index(self):
        """Test deleteData with an invalid index."""
        # Arrange
        data = [Entry("John Doe", "12345")]
        filename = "testfile.txt"

        self.module_d.deleteData(data, 5, filename)

    def test_parseUpdate_invalid_index(self):
        """Test updateData with an invalid index."""
        # Arrange
        data = [Entry("John Doe", "12345")]
        filename = "testfile.txt"
        self.module_d.updateData(data, 5, "Jane Doe", "54321", filename)

    def test_getter_f(self):
        """Test the getter for property 'f'."""
        # Act
        result = self.module_d.f

        # Assert
        self.assertEqual(result, self.module_f)
        self.assertIsInstance(result, ModuleF)

    def test_setter_f(self):
        """Test the setter for property 'f'."""
        # Arrange
        new_f = ModuleF()

        # Act
        self.module_d.f = new_f

        # Assert
        self.assertEqual(self.module_d.f, new_f)
        self.assertNotEqual(self.module_d.f, self.module_f)

    def test_getter_g(self):
        """Test the getter for property 'g'."""
        # Act
        result = self.module_d.g

        # Assert
        self.assertEqual(result, self.module_g)
        self.assertIsInstance(result, ModuleG)

    def test_setter_g(self):
        """Test the setter for property 'g'."""
        # Arrange
        new_g = ModuleG()

        # Act
        self.module_d.g = new_g

        # Assert
        self.assertEqual(self.module_d.g, new_g)
        self.assertNotEqual(self.module_d.g, self.module_g)
