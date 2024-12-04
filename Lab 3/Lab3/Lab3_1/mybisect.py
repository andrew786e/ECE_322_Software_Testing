class MyBisect:

    # constructor overloading
    # based on args
    def __init__(self, *args):
        # given tolerance, maxIterations, function
        if len(args) == 3:
            self._tolerance = args[0]
            self._maxIterations = args[1]
            self._func = args[2]
        # given tolerance or maxIterations, function
        elif len(args) == 2:
            if isinstance(args[0], float):
                self._tolerance = args[0]
                self._maxIterations = 50
                self._func = args[1]
            else:
                # if arg is an integer
                self._tolerance = 0.000001
                self._maxIterations = args[0]
                self._func = args[1]
        elif len(args) == 1:
            # only given a function
            self._tolerance = 0.000001
            self._maxIterations = 50
            self._func = args[0]
        else:
            self._tolerance = 0.000001
            self._maxIterations = 50
            self._func = None

    # using property decorator
    # a getter function
    @property
    def tolerance(self):
        return self._tolerance

    # a setter function
    @tolerance.setter
    def tolerance(self, tol):
        if tol > 0:
            self._tolerance = tol

    # using property decorator
    # a getter function
    @property
    def max_iterations(self):
        return self._maxIterations

    # a setter function
    @max_iterations.setter
    def max_iterations(self, max_iter):
        if max_iter > 0:
            self._maxIterations = max_iter

    def run(self, x1, x2):
        iter_num = 1
        mid = 0

        while True:
            f1 = self._func(x1)
            f2 = self._func(x2)
            if f1 * f2 > 0:
                raise ValueError('Root Not Found')
            mid = (x1 + x2) / 2.0
            fmid = self._func(mid)
            if fmid * f1 < 0:
                x2 = mid
            else:
                x1 = mid
            iter_num += 1
            if not ((abs(x1 - x2) / 2) >= self._tolerance and abs(
                    fmid) > self._tolerance and iter_num <= self._maxIterations):
                break
        print("iter_num: {}, max_iter: {}".format(iter_num, self._maxIterations))
        if iter_num >= self._maxIterations:
            raise ValueError('Root Not Found')
        return mid


class Polynomial:
    def __init__(self, *coefficients):
        """ input: coefficients are in the form a_n, ...a_1, a_0
        """
        self.coefficients = list(coefficients)  # tuple is turned into a list

    # The __repr__ and __str__ method can be included here,
    # but is not necessary for the immediately following code

    def __call__(self, x):
        res = 0
        for coeff in self.coefficients:
            res = res * x + coeff
        return res


# def main():
#     result = 0
#     f = Polynomial(1, -1)  # x-1    ### example for x^2+x-1 use Polynomial(1,1,-1)
#     b = MyBisect(f)
#     try:
#         result = b.run(-10, 10)
#         print("Root found at:" + str(result))
#     except ValueError as err:
#         print(err.args)
#
#
# if __name__ == "__main__":
#     main()