import unittest
from unittest.mock import patch , call
from MathPackage import MathPackage

class MyTestCase(unittest.TestCase):

    # Test whether the value is within range and
    # Whether the length of the array is correct
    def test_random_func_min_max_length(self):
        result = MathPackage.random(5 , 6 , 10)
        maxValue = max(result)
        minValue = min(result)
        self.assertEqual(5 ,len(result))
        self.assertGreaterEqual(minValue , 6)
        self.assertLessEqual(maxValue, 10)

    def test_random_func_zeroLength(self):
        result = MathPackage.random(0 , 6 , 10)
        self.assertEqual(len(result), 0)
        self.assertEqual(result , [])

    def test_random_func_random_negative_value(self):
        result = MathPackage.random(7, -7,  -4)
        maxValue = max(result)
        minValue = min(result)
        self.assertGreaterEqual(minValue, -7)
        self.assertLessEqual(maxValue, -4)

    # This test case fails
    def test_random_func_random_with_boundary_switched(self):

        with self.assertRaises(ValueError) as context:
            MathPackage.random(7, 10,  6)

        self.assertEqual(str(context.exception), "Lower bound 'a' cannot be greater than upper bound 'b'")


    @patch.object(MathPackage , 'random')
    def test_random_func_mock_random(self , mock_random):
        mock_random.return_value = [3.6 , 3.8 , 5]
        result = MathPackage.random(3 , 3.5 , 5.6)

        mock_random.assert_called()
        mock_random.assert_called_once()
        mock_random.assert_called_with(3 , 3.5 , 5.6)
        mock_random.assert_called_once_with(3 , 3.5 , 5.6)
        self.assertEqual(mock_random.call_count, 1)
        self.assertEqual(mock_random.call_args,((3,3.5,5.6),))
        self.assertEqual(mock_random.call_args_list, [((3, 3.5, 5.6),)])
        self.assertEqual(result , [3.6, 3.8, 5])


    def test_max_function_emptyList(self):
        with self.assertRaises(ValueError) as context:
            result = MathPackage.max([])

        self.assertEqual(str(context.exception), "No values given in the list")

    def test_max_function_single(self):
        result = MathPackage.max([1])
        self.assertEqual(result, 1)

    def test_max_function_positive_number(self):
        result = MathPackage.max([1 ,2 ,3])
        self.assertEqual(result, 3)

    def test_max_function_positive_negative_number(self):
        result = MathPackage.max([-1, 2 , -3])
        self.assertEqual(result, 2)

    def test_max_function_negative_number(self):
        result = MathPackage.max([-1 ,-2 ,-3])
        self.assertEqual(-1 , result)

    def test_max_function_zero(self):
        result = MathPackage.max([0 ,-2 ,-3])
        self.assertEqual(0, result)

    def test_max_function_with_infinity(self):
        result = MathPackage.max([float('-inf'), -1, 0, float('inf')])
        self.assertEqual(result, float('inf'))

    def test_max_function_duplicate_values(self):
        result = MathPackage.max([5, 5, 1, 3])
        self.assertEqual(result, 5)

    def test_max_function_mixed_types(self):
        result = MathPackage.max([1, 2.5, 3])
        self.assertEqual(result, 3)

    @patch.object(MathPackage, 'max')
    def test_random_func_mock_max(self, mock_max):
        # Mock return value
        mock_max.return_value = 6

        # Call the max function with the mock
        result = MathPackage.max([1, 6, 5])

        # Assertions for the mock
        mock_max.assert_called()
        mock_max.assert_called_once()
        mock_max.assert_called_with([1, 6, 5])
        mock_max.assert_called_once_with([1, 6, 5])
        self.assertEqual(mock_max.call_count, 1)
        self.assertEqual(mock_max.call_args, (([1, 6, 5],),))
        self.assertEqual(mock_max.call_args_list, [(([1, 6, 5],),)])
        self.assertEqual(result, 6)

    def test_min_function_emptyList(self):
        with self.assertRaises(ValueError) as context:
            result = MathPackage.min([])

        self.assertEqual(str(context.exception), "No values given in the list")

    def test_min_function_single(self):
        result = MathPackage.min([1])
        self.assertEqual(result, 1)

    def test_min_function_positive_number(self):
        result = MathPackage.min([1 ,2 ,3])
        self.assertEqual(result, 1)

    def test_min_function_negative_number(self):
        result = MathPackage.min([-1 ,-2 ,-3])
        self.assertEqual(result, -3)

    def test_min_function_positive_negative_number(self):
        result = MathPackage.min([-1 ,2,-3])
        self.assertEqual(result, -3)

    def test_min_function_with_zero(self):
        result = MathPackage.min([1 ,0 ,3])
        self.assertEqual(result, 0)

    def test_min_function_with_infinity(self):
        result = MathPackage.min([float('-inf'), -1, 0, float('inf')])
        self.assertEqual(result, float('-inf'))

    def test_min_function_duplicate_values(self):
        result = MathPackage.min([5, 5, 1, 3])
        self.assertEqual(result, 1)

    def test_min_function_mixed_types(self):
        result = MathPackage.min([1, 2.5, -3])
        self.assertEqual(result, -3)

    @patch.object(MathPackage, 'min')
    def test_random_func_mock_min(self, mock_min):
        # Mock return value
        mock_min.return_value = 6

        # Call the max function with the mock
        result = MathPackage.min([6, 7, 8])

        # Assertions for the mock
        mock_min.assert_called()
        mock_min.assert_called_once()
        mock_min.assert_called_with([6, 7, 8])
        mock_min.assert_called_once_with([6, 7, 8])
        self.assertEqual(mock_min.call_count, 1)
        self.assertEqual(mock_min.call_args, (([6, 7, 8],),))
        self.assertEqual(mock_min.call_args_list, [(([6, 7, 8],),)])
        self.assertEqual(result, 6)



if __name__ == '__main__':
    unittest.main()
