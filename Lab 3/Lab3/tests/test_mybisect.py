import unittest

from mybisect import Polynomial, MyBisect


class TestMyBisectFunctions(unittest.TestCase):
    def test_constructor_with_tolerance_maxIterations_func(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(0.0001, 100, f)
        self.assertEqual(b.tolerance, 0.0001)
        self.assertEqual(b.max_iterations, 100)
        self.assertEqual(b._func, f)

    def test_constructor_with_tolerance_func(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(0.0001, f)
        self.assertEqual(b.tolerance, 0.0001)
        self.assertEqual(b._func, f)
        self.assertEqual(b.max_iterations, 50)

    def test_constructor_with_maxiterations_func(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(100, f)
        self.assertEqual(b.max_iterations, 100)
        self.assertEqual(b._func, f)
        self.assertEqual(b.tolerance, 0.000001)

    def test_constructor_with_func(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(f)
        self.assertEqual(b.tolerance, 0.000001)
        self.assertEqual(b.max_iterations, 50)
        self.assertEqual(b._func, f)

    def test_constructor_with_no_arguments(self):
        b = MyBisect()
        self.assertEqual(b.tolerance, 0.000001)
        self.assertEqual(b.max_iterations, 50)
        self.assertEqual(b._func, None)

    def test_setters_within_range(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(0.0001, 100, f)
        self.assertEqual(b.tolerance, 0.0001)
        self.assertEqual(b.max_iterations, 100)
        b.max_iterations = 23
        b.tolerance = 0.0000001
        self.assertEqual(b.tolerance, 0.0000001)
        self.assertEqual(b.max_iterations, 23)

    def test_setters_with_negative_value(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(0.0001, 100, f)
        self.assertEqual(b.tolerance, 0.0001)
        self.assertEqual(b.max_iterations, 100)
        b.max_iterations = -1
        b.tolerance = -10
        self.assertEqual(b.tolerance, 0.0001)
        self.assertEqual(b.max_iterations, 100)

    def test_run_function_root_found(self):
        f = Polynomial(1, -1) #f(x) = x - 1
        b = MyBisect(0.000001 , 50 , f)
        result = b.run(-10 , 10)
        self.assertAlmostEqual(result ,1 , places=5)

    def test_run_function_root_not_in_interval(self):
        f = Polynomial(1, 0, 1)  # f(x) = x^2 + 1 (no real roots)
        b = MyBisect(f)
        with self.assertRaises(ValueError) as context:
            b.run(-1 ,1 )
        self.assertEqual(str(context.exception) , 'Root Not Found')

    def test_run_function_convergence_by_tolerance(self):
        f = Polynomial(1, 0, -4)  # f(x) = x^2 - 4
        b = MyBisect(0.001, 50, f)
        result = b.run(1, 3)
        self.assertAlmostEqual(result, 2, places=3)

    def test_run_function_exceding_max_iterations(self):
        f = Polynomial(1, 0, -2, 2)  # f(x) = x^3 - 2x + 2
        b = MyBisect(0.000001, 5, f)
        with self.assertRaises(ValueError) as context:
            b.run(-2, 2)
        self.assertEqual(str(context.exception), 'Root Not Found')

    def test_run_function_with_multiple_iterations(self):
        f = Polynomial(1, 0, -9)  # f(x) = x^2 - 9
        b = MyBisect(0.000001, 50, f)
        result = b.run(2, 5)
        self.assertAlmostEqual(result, 3, places=5)

    # This causes an error the exception is not handled properly when no function is given
    def test_run_function_with_no_function(self):
        b = MyBisect()
        with self.assertRaises(ValueError) as context:
            b.run(2, 5)
        self.assertEqual(str(context.exception), 'No function given')


#     negative values can be set in the program
    def test_run_function_initialized_negative_value(self):
        f = Polynomial(1, 0, -9)  # f(x) = x^2 - 9
        b = MyBisect(-0.0001, -50, f)
        with self.assertRaises(ValueError) as context:
            b.run(2, 5)
        self.assertEqual(str(context.exception), 'Root Not Found')

if __name__ == '__main__':
    unittest.main()
