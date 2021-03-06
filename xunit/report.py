from xunit.api import IFormatter, IReport, TestResult

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
CHECK_MARK = f"{GREEN}\N{HEAVY CHECK MARK}{RESET}"
CROSS_MARK = f"{RED}\N{HEAVY BALLOT X}{RESET}"
INDENT = "    "


class Report(IReport):
    def __init__(self) -> None:
        self.__test_results: dict[str, list] = {}
        self.__failure_count = 0
        self.__run_count = 0

    def record_test_result(self, test_result: TestResult):
        self.__run_count += 1
        if test_result.test_case() not in self.__test_results:
            self.__test_results.update({test_result.test_case(): [test_result]})
        else:
            self.__test_results.get(test_result.test_case()).append(test_result)
        if test_result.failed():
            self.__failure_count += 1

    def test_results(self) -> dict[str, list]:
        return self.__test_results.copy()

    def run_count(self) -> int:
        return self.__run_count

    def failure_count(self) -> int:
        return self.__failure_count


class DefaultFormatter(IFormatter):

    @classmethod
    def format(cls, test_report: Report) -> str:
        test_results = test_report.test_results()
        full_report = f"{CHECK_MARK if test_report.failure_count() == 0 else CROSS_MARK} Test Report ({test_report.run_count()} run, {test_report.failure_count()} failed):\n"
        for test_case, test_results in test_results.items():
            full_report = full_report + f"{cls.__format_test_case(test_case, test_results)}"

        return full_report

    @classmethod
    def __format_test_case(cls, test_case: str, test_results: list) -> str:
        failures = 0
        test_case_report = ""
        for result in test_results:
            if result.failed():
                failures += 1
            test_case_report = test_case_report + f"{INDENT}{cls.__format_test_result(result)}\n"

        return f"{INDENT}{CROSS_MARK if failures > 0 else CHECK_MARK} {test_case} ({len(test_results)} run, {failures} failed):\n" + test_case_report + "\n"

    @classmethod
    def __format_test_result(cls, test_result: TestResult) -> str:
        if test_result.failed():
            return cls.__format_failure(test_result)
        else:
            return cls.__format_success(test_result)

    @classmethod
    def __format_failure(cls, test_result: TestResult) -> str:
        return f"{INDENT}{CROSS_MARK} {test_result.test_name()}\n{RED}{INDENT*3}{test_result.reason()}{RESET}"

    @classmethod
    def __format_success(cls, test_result: TestResult) -> str:
        return f"{INDENT}{CHECK_MARK} {test_result.test_name()}"
