class TestReporter:
    def __init__(self) -> None:
        self.__details = {}
        self.run_count = 0
        self.error_count = 0

    def test_started(self):
        self.run_count += 1
        
    def test_failed(self, test_name: str, failure_reason: str):
        self.__details.update({test_name: failure_reason})
        self.error_count += 1

    def details(self) -> dict:
        return self.__details.copy() 

    def summary(self) -> str:
        return f"{self.run_count} run, {len(self.__details)} failed"
    
class TestResult:
    def __init__(self, name) -> None:
        self.__test_name = name
        self.__failed = False
        self.__reason = None
        
    def record_failure(self, reason: any):
        self.__reason = reason
        self.__failed = True
        
    def test_name(self) -> str:
        return self.__test_name
    
    def failed(self) -> bool:
        return self.__failed
    
    def reason(self) -> any:
        return self.__reason