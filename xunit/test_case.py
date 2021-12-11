import inspect
from .test_report import TestResult

class TestCase:
    def __init__(self, name) -> None:
        self.name = name

    def setup(self):
        """
        optional setup before each test method
        """       

    def run(self, test_result: TestResult) -> None:
        test_result.test_started()
        try:
            self.setup()
            try:
                method = getattr(self, self.name)
                method()
            except AssertionError as ae:
                test_result.test_failed(self.name, ae)
        except Exception as e:
            test_result.test_failed(self.name, e)
        finally:
            self.tear_down()        

    def tear_down(self):
        """
        optional tear down after each test method
        """
        
    @classmethod
    def create_test_suite(cls) -> "TestSuite":
        test_suite = TestSuite()
        for member in inspect.getmembers(cls):
            if inspect.isfunction(member[1]) and member[0].startswith("test_"):
                test_suite.add(cls(member[0]))
        return test_suite

class TestSuite(TestCase):
    def __init__(self) -> None:
        self.__tests = []
        
    def add(self, test):
        self.__tests.append(test)
        
    def number_of_tests(self) -> int:
        return len(self.__tests)
        
    def run(self, test_result: TestResult):
        for test in self.__tests:
            test.run(test_result)
