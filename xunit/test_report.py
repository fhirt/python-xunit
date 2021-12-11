class TestResult:
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