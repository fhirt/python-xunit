import inspect
from .test_report import TestReport

class TestCase:
    def __init__(self, name) -> None:
        self.name = name

    def setup(self):
        """
        optional setup before each test method
        """       

    def run(self, test_report: TestReport) -> None:
        test_report.test_started()
        try:
            self.setup()
            try:
                method = getattr(self, self.name)
                method()
            except AssertionError as ae:
                test_report.test_failed(self.name, ae)
        except Exception as e:
            test_report.test_failed(self.name, e)
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
            if inspect.isfunction(member[1]) and (member[0].startswith("test_") or member[0].startswith("should_")):
                test_suite.add(cls(member[0]))
        return test_suite

class TestSuite(TestCase):
    def __init__(self) -> None:
        self.__tests = []
        
    def add(self, test):
        self.__tests.append(test)
        
    def number_of_tests(self) -> int:
        return len(self.__tests)
        
    def run(self, test_report: TestReport):
        for test in self.__tests:
            test.run(test_report)
