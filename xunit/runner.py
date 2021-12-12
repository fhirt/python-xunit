from xunit.test_case import TestSuite


class Runner():
    def __init__(self) -> None:
        self.__test_suites = []
        
    def add(self, *args) -> None:
        for suite in args:
            self.__test_suites.append(suite)

    def run(self) -> None:
        pass