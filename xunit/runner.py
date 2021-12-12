from xunit.test_case import TestSuite


class Runner():
    def __init__(self) -> None:
        self.__test_suites: list[TestSuite] = []
        
    def add(self, *args) -> None:
        for suite in args:
            self.__test_suites.append(suite)

    def run(self) -> None:
        print(self.__test_suites)