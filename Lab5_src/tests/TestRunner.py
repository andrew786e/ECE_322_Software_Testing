# tests/TestRunner.py
#The basic idea here is to have a new Python file Testrunner.py
# alongside your tests that contains our runner.
import unittest

# import your tests modules (Apply integration testing method)
from tests.TopBottomTesting import TestModuleA
from tests.TopBottomTesting import TestModuleABCDE
from tests.TopBottomTesting import  TestModuleABCDEFG
from tests.BottomUpTesting import TestModuleABCDEFGBottom
from tests.BottomUpTesting import TestModuleB, TestModuleC, TestModuleD, TestModuleE , TestModuleF , TestModuleG

# import TestModuleB
#import TestModuleC
# .... Complete the missing imports



# initialize the tests suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(TestModuleA))
suite.addTests(loader.loadTestsFromModule(TestModuleABCDE))
suite.addTests(loader.loadTestsFromModule(TestModuleABCDEFG))
suite.addTests(loader.loadTestsFromModule(TestModuleABCDEFGBottom))
suite.addTests(loader.loadTestsFromModule(TestModuleB))
suite.addTests(loader.loadTestsFromModule(TestModuleC))
suite.addTests(loader.loadTestsFromModule(TestModuleD))
suite.addTests(loader.loadTestsFromModule(TestModuleE))
suite.addTests(loader.loadTestsFromModule(TestModuleF))
suite.addTests(loader.loadTestsFromModule(TestModuleG))

# .... Complete the missing additions


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)