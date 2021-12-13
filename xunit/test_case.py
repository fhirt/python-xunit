import inspect
from xunit.api import IReport, TestResult


class TestCase:
    def __init__(self, name) -> None:
        self.__name = name

    def setup(self):
        """
        optional setup before each test method
        """

    def run(self, test_report: IReport) -> None:
        test_result = TestResult(self)
        try:
            self.setup()
            try:
                method = getattr(self, self.__name)
                method()
            except AssertionError as ae:
                test_result.record_failure(ae)
        except Exception as e:
            test_result.record_failure(e)
        finally:
            test_report.record_test_result(test_result)
            self.tear_down()

    def name(self) -> str:
        return self.__name

    def tear_down(self):
        """
        optional tear down after each test method
        """

    @classmethod
    def create_test_suite(cls) -> "TestSuite":
        test_suite = TestSuite()
        for member in inspect.getmembers(cls):
            if inspect.isfunction(member[1]) and (member[0].startswith("test_") or member[0].startswith("should_") or member[0].startswith("expect_") or "_should_" in member[0]):
                test_suite.add(cls(member[0]))
        return test_suite


class TestSuite(TestCase):
    def __init__(self) -> None:
        self.__tests = []

    def add(self, test):
        self.__tests.append(test)

    def number_of_tests(self) -> int:
        return len(self.__tests)

    def run(self, test_report: IReport):
        for test in self.__tests:
            test.run(test_report)
