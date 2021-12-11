import xunit

class WasRun(xunit.TestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        self.log = "setup "

    def should_run_test_method(self):
        self.log = self.log + "test_method "

    def tear_down(self):
        self.log = self.log + "tear_down"

    def test_broken_method(self):
        assert(1 == 2)            
    
    
class RaiseSetupException(WasRun):
    def __init__(self, name) -> None:
        super().__init__(name)
        
    def setup(self):
        super().setup()
        raise Exception("setup failed")
    
class TestCaseTest(xunit.TestCase):
    
    def setup(self):
        self.test_report = xunit.TestReporter()    
    
    def test_template_method(self):
        test = WasRun("should_run_test_method")
        test.run(self.test_report)
        assert(test.log == "setup test_method tear_down")

    def should_report_success(self):
        test = WasRun("should_run_test_method")
        test.run(self.test_report)
        assert(self.test_report.summary() == "1 run, 0 failed")

    def should_report_failure(self):
        broken_test = WasRun("test_broken_method")
        broken_test.run(self.test_report)
        assert(self.test_report.summary() == "1 run, 1 failed")
        
    def should_return_formatted_summary_report(self):
        self.test_report.test_started()
        self.test_report.test_failed("test", "some reason")
        assert(self.test_report.summary() == "1 run, 1 failed")
        
    def should_handle_setup_exception(self):
        test = RaiseSetupException("should_run_test_method")
        test.run(self.test_report)
        assert(self.test_report.summary() == "1 run, 1 failed")

    def test_suite(self):
        suite = xunit.TestSuite()
        suite.add(WasRun("should_run_test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.test_report)
        assert("2 run, 1 failed" == self.test_report.summary())
        
    def should_report_test_details(self):
        self.test_report.test_started()
        self.test_report.test_failed("test_1", "reason 1")
        self.test_report.test_started()
        self.test_report.test_started()
        self.test_report.test_failed("test_3", "reason 2")
        assert(self.test_report.summary() == "3 run, 2 failed")
        assert(self.test_report.details() == { "test_1": "reason 1", "test_3": "reason 2"})
        
    def should_create_suite_from_defined_test_cases_(self):
        suite = WasRun.create_test_suite()
        assert(suite.number_of_tests() == 2)
        
    def should_record_successful_test(self):
        test_result = xunit.TestResult("successful_test")
        assert(test_result.test_name() == "successful_test")
        assert(test_result.failed() == False)
        assert(test_result.reason() == None)
        
    def should_record_failure_reason_for_unsuccessful_test(self):
        test_result = xunit.TestResult("failing_test")
        test_result.record_failure("reason")
        assert(test_result.test_name() == "failing_test")
        assert(test_result.failed() == True)
        assert(test_result.reason() == "reason")
        
    def should_collect_test_results(self):
        pass
        
suite = TestCaseTest.create_test_suite()
result = xunit.TestReporter()       
suite.run(result)

print(result.summary())
print(result.details())
