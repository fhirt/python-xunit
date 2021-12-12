class TestReport:
    def __init__(self) -> None:
        self.__test_results = []
        self.__failure_count = 0
        
    def record_test_result(self, test_result: "TestResult"):
        self.__test_results.append(test_result)
        if test_result.failed():
            self.__failure_count += 1     
    
    def test_results(self) -> list:
        return self.__test_results.copy()
    
    def failure_count(self) -> int:
        return self.__failure_count

    def summary(self) -> str:
        return f"{len(self.__test_results)} run, {self.__failure_count} failed"

    
class TestResult:
    def __init__(self, name) -> None:
        self.__test_name = name
        self.__failed = False
        self.__reason = None
        
    def record_failure(self, reason: str):
        self.__reason = reason
        self.__failed = True
        
    def test_name(self) -> str:
        return self.__test_name
    
    def failed(self) -> bool:
        return self.__failed
    
    def reason(self) -> str:
        return self.__reason

class TestReportFormatter:
    CHECK_MARK = "\N{HEAVY CHECK MARK}"
    CROSS_MARK = "\N{HEAVY BALLOT X}"
    INDENT = "  "
    
    @classmethod
    def format(cls, test_report: TestReport) -> str:
        full_report = f"{cls.CHECK_MARK if test_report.failure_count() == 0 else cls.CROSS_MARK} TestReport ({test_report.summary()}):\n"
        for result in test_report.test_results():
            full_report = full_report + f"{cls.__format_test_result(result)}\n"
        return full_report
    
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