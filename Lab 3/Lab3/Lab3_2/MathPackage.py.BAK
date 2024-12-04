from typing import List
from typing import *

import random
import sys
import math


class MathPackage:

    @classmethod
    def random(self,n:int ,a:float, b:float)->List:
        """
         Creates an array of n random values in the range [a,b]
        :param n: n Number of values to generate
        :param a:lower bound
        :param b: upper bound
        :return: Array of random values

        """
        values=[]

        # create a list of prime numbers
        for i in range(n):
            values.append( a + (random.random()*(b - a)))
        return  values



    @classmethod
    def max(self,values:List)->float:
        """
        Returns the maximum values contained in the passed array
        :param values values Array to search in
        :return: Highest value in passed array
        """
        max=sys.float_info.min
        for value in values:
            if (max < value):
                max = value
        return max

    @classmethod
    def min(self,values:List)->float:
        """
        Returns the minimum values of an array
        :param values values Array to search in
        :return: Smallest value in the array
        """
        min=sys.float_info.max
        for value in values:
            if(min > value):
                min = value
        return min


