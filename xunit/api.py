class TestResult:
    def __init__(self, test_case) -> None:
        self.__test_case = test_case
        self.__failed = False
        self.__reason = None

    def record_failure(self, reason: str):
        self.__reason = reason
        self.__failed = True

    def test_case(self) -> str:
        return type(self.__test_case).__name__

    def test_name(self) -> str:
        return self.__test_case.name()

    def failed(self) -> bool:
        return self.__failed

    def reason(self) -> str:
        return self.__reason


class IReport:
    def record_test_result(self, test_result: TestResult):
        raise NotImplementedError

    def test_results(self) -> dict[str, list]:
        raise NotImplementedError

    def run_count(self) -> int:
        raise NotImplementedError

    def failure_count(self) -> int:
        raise NotImplementedError


class IFormatter:

    @classmethod
    def format(cls, test_report: IReport) -> any:
        raise NotImplementedError
