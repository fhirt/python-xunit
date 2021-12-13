from xunit.api import IFormatter, IReport
from xunit.report import DefaultFormatter, Report
from xunit.test_case import TestCase, TestSuite


class Runner():
    def __init__(self) -> None:
        self.__formatter: IFormatter = DefaultFormatter()
        self.__report: IReport = Report()
        self.__test_suites: list[TestSuite] = []
        
    def add(self, *args: TestCase) -> None:
        for test_case in args:
            self.__test_suites.append(test_case.create_test_suite())

    def run(self) -> str:
        for test_suite in self.__test_suites:
            test_suite.run(self.__report)
        
        return self.__formatter.format(self.__report)
        
    def run_count(self) -> int:
        return self.__report.run_count()
    
    def failure_count(self) -> int:
        return self.__report.failure_count()