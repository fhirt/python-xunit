
class Report:
    def __init__(self) -> None:
        self.__test_results: dict[str, list] = {}
        self.__failure_count = 0
        self.__run_count = 0
        
    def record_test_result(self, test_result: "TestResult"):
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

    def summary(self) -> str:
        return f"{self.run_count()} run, {self.failure_count()} failed"

    
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

class ReportFormatter:
    CHECK_MARK = "\N{HEAVY CHECK MARK}"
    CROSS_MARK = "\N{HEAVY BALLOT X}"
    INDENT = "  "
    
    @classmethod
    def format(cls, test_report: Report) -> str:
        test_results = test_report.test_results()
        full_report = f"{cls.CHECK_MARK if test_report.failure_count() == 0 else cls.CROSS_MARK} Test Report ({test_report.summary()}):\n"
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
            test_case_report = test_case_report + f"{cls.INDENT}{cls.__format_test_result(result)}\n"

        return f"{cls.INDENT}{cls.CROSS_MARK if failures > 0 else cls.CHECK_MARK} {test_case} ({len(test_results)} run, {failures} failed):\n" + test_case_report
    
    @classmethod
    def __format_test_result(cls, test_result: TestResult) -> str:
        if test_result.failed():
            return cls.__format_failure(test_result)
        else:
            return cls.__format_success(test_result)
        
    @classmethod
    def __format_failure(cls, test_result: TestResult) -> str:
        return f"{cls.INDENT}{cls.CROSS_MARK} {test_result.test_name()}\n{cls.INDENT*2}{test_result.reason()}"
    
    @classmethod
    def __format_success(cls, test_result: TestResult) -> str:
        return f"{cls.INDENT}{cls.CHECK_MARK} {test_result.test_name()}"