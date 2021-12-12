CHECK_MARK = "\N{HEAVY CHECK MARK}"
CROSS_MARK = "\N{HEAVY BALLOT X}"

class TestReporter:
    def __init__(self) -> None:
        self.__test_results = []
        self.__failure_count = 0
        
    def record_test_result(self, test_result: "TestResult"):
        self.__test_results.append(test_result)
        if test_result.failed():
            self.__failure_count += 1     
    
    def test_results(self) -> list:
        return self.__test_results.copy()
    
    def full_report(self) -> str:
        full_report = f"{CHECK_MARK if self.__failure_count == 0 else CROSS_MARK} TestReport ({self.summary()}):\n"
        for result in self.__test_results:
            full_report = full_report + f"{result}\n"
        return full_report

    def summary(self) -> str:
        return f"{len(self.__test_results)} run, {self.__failure_count} failed"
    
class TestResult:
    def __init__(self, name) -> None:
        self.__test_name = name
        self.__failed = False
        self.__reason = None
        
    def record_failure(self, reason: str):
        print("debug", reason)
        self.__reason = reason
        self.__failed = True
        
    def test_name(self) -> str:
        return self.__test_name
    
    def failed(self) -> bool:
        return self.__failed
    
    def reason(self) -> str:
        return self.__reason
    
    def __str__(self) -> str:
        if self.failed():
            return self.__format_failure()
        else:
            return self.__format_success()
    
    def __format_failure(self) -> str:
        return f"  {CROSS_MARK} {self.__test_name}\n\t{self.__reason}"
    
    def __format_success(self) -> str:
        return f"  {CHECK_MARK} {self.__test_name}"