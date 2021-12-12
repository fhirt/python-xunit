import xunit


class MockTestCase(xunit.TestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        self.log = "setup "

    def should_run_test_method(self):
        self.log = self.log + "test_method "

    def tear_down(self):
        self.log = self.log + "tear_down"

    def test_broken_method(self):
        assert 1 == 2, "should be 1, but was 2"


class MockTestCaseWithSetupException(MockTestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        super().setup()
        raise Exception("setup failed")


class TestCaseTest(xunit.TestCase):

    def setup(self):
        self.test_report = xunit.TestReport()

    def should_run_setup_test_case_and_teardown(self):
        test = MockTestCase("should_run_test_method")
        test.run(self.test_report)
        assert test.log == "setup test_method tear_down", f"should run all TestCase methods but was: {test.log}"

    def should_report_success(self):
        test = MockTestCase("should_run_test_method")
        test.run(self.test_report)
        assert self.test_report.run_count() == 1
        assert self.test_report.failure_count() == 0

    def should_report_failure(self):
        broken_test = MockTestCase("test_broken_method")
        broken_test.run(self.test_report)
        assert self.test_report.run_count() == 1
        assert self.test_report.failure_count() == 1

    def should_run_teardown_after_setup_exception(self):
        test = MockTestCaseWithSetupException("should_run_test_method")
        test.run(self.test_report)
        assert test.log == "setup tear_down", f"should run tear_down: {test.log}"


suite = TestCaseTest.create_test_suite()
test_report = xunit.TestReport()
test_report.test_suite("TestCaseTest")
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))

class TestSuiteTest(xunit.TestCase):
    def setup(self):
        self.test_report = xunit.TestReport()
        
    def should_run_all_test_cases_in_test_suite(self):
        suite = xunit.TestSuite()
        suite.add(MockTestCase("should_run_test_method"))
        suite.add(MockTestCase("test_broken_method"))
        suite.run(self.test_report)
        assert "2 run, 1 failed" == self.test_report.summary(), f"should print correct summary but was: {self.test_report.summary()}"

    def should_add_test_cases_starting_with_should_and_test(self):
        suite = MockTestCase.create_test_suite()
        assert suite.number_of_tests() == 2, f"should be 2, but was: {suite.number_of_tests()}"
        
    def should_record_failure_reason(self):
        suite = MockTestCase.create_test_suite()
        suite.run(self.test_report)
        test_results = self.test_report.test_results()
        assert len(test_results) == 2, f"should be 2, but was: {len(test_results)}"
        assert self.test_report.failure_count() == 1, f"should be 1, but was: {self.test_report.failure_count()}"
        failing_test = None
        for test_result in test_results:
            if test_result.failed():
                failing_test = test_result
        assert failing_test.reason() != None, f"should not be None"
        
suite = TestSuiteTest.create_test_suite()
test_report = xunit.TestReport()
test_report.test_suite("TestSuiteTest")
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))

class TestReportTest(xunit.TestCase):
    def should_record_successful_test(self):
        test_result = xunit.TestResult("successful_test")
        assert test_result.test_name() == "successful_test"
        assert test_result.failed() == False
        assert test_result.reason() == None

    def should_record_failure_reason_for_unsuccessful_test(self):
        test_result = xunit.TestResult("failing_test")
        test_result.record_failure("reason")
        assert test_result.test_name() == "failing_test", "should be failing_test, but was:"
        assert test_result.failed() == True, "should be True, but was:"
        assert test_result.reason() == "reason", "should record reason, but was:"

    def should_format_test_report(self):
        test_report = xunit.TestReport()
        test_report.test_suite("TestSuiteName")
        test_result_one = xunit.TestResult("test_1")
        test_result_one.record_failure("failure reason")
        test_report.record_test_result(test_result_one)

        test_result_two = xunit.TestResult("test_2")
        test_report.record_test_result(test_result_two)

        assert test_report.summary() == "2 run, 1 failed", f"should display summary, but was: '{test_report.summary()}'"
        formatted_report = xunit.TestReportFormatter.format(test_report)
        assert "TestSuiteName" in formatted_report, "should contain 'TestSuiteName'"
        assert "test_1" in formatted_report, "should report failing test"
        assert "test_2" in formatted_report, "should report successful test"
        assert "failure reason" in formatted_report, "should report failure reason"

suite = TestReportTest.create_test_suite()
test_report = xunit.TestReport()
test_report.test_suite("TestReportTest")
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))

class RunnerTest(xunit.TestCase):
    def should_setup_and_run_specified_test_suites(self):
        mock_suite_one = MockTestCase.create_test_suite()
        mock_suite_two = MockTestCaseWithSetupException.create_test_suite()
        
        runner = xunit.Runner()
        runner.add(mock_suite_one, mock_suite_two)
        runner.run()
        
suite = RunnerTest.create_test_suite()
test_report = xunit.TestReport()
test_report.test_suite("RunnerTest")
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))