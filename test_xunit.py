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

    def test_template_method(self):
        test = MockTestCase("should_run_test_method")
        test.run(self.test_report)
        assert test.log == "setup test_method tear_down", f"should run all TestCase methods but was: {test.log}"

    def should_report_success(self):
        test = MockTestCase("should_run_test_method")
        test.run(self.test_report)
        assert self.test_report.summary() == "1 run, 0 failed", f"should print correct summary but was: {self.test_report.summary()}"

    def should_report_failure(self):
        broken_test = MockTestCase("test_broken_method")
        broken_test.run(self.test_report)
        assert self.test_report.summary() == "1 run, 1 failed", f"should print correct summary but was: {self.test_report.summary()}"

    def should_return_formatted_summary_report(self):
        test_result = xunit.TestResult("test")
        test_result.record_failure("some reason")
        self.test_report.record_test_result(test_result)
        assert self.test_report.summary() == "1 run, 1 failed", f"should print correct summary but was: {self.test_report.summary()}"

    def should_handle_setup_exception(self):
        test = MockTestCaseWithSetupException("should_run_test_method")
        test.run(self.test_report)
        assert self.test_report.summary() == "1 run, 1 failed", f"should print correct summary but was: {self.test_report.summary()}"

    def test_suite(self):
        suite = xunit.TestSuite()
        suite.add(MockTestCase("should_run_test_method"))
        suite.add(MockTestCase("test_broken_method"))
        suite.run(self.test_report)
        assert "2 run, 1 failed" == self.test_report.summary(), f"should print correct summary but was: {self.test_report.summary()}"

    def should_create_suite_from_defined_test_cases(self):
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

suite = TestCaseTest.create_test_suite()
test_report = xunit.TestReport()
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))

class TestReportTest(xunit.TestCase):
    def setup(self):
        self.test_report = xunit.TestReport()

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
        test_result_one = xunit.TestResult("test_1")
        test_result_one.record_failure("failure reason")
        self.test_report.record_test_result(test_result_one)

        test_result_two = xunit.TestResult("test_2")
        self.test_report.record_test_result(test_result_two)

        assert self.test_report.summary() == "2 run, 1 failed", f"should display summary, but was: '{self.test_report.summary()}'"
        formatted_report = xunit.TestReportFormatter.format(self.test_report)
        assert "test_1" in formatted_report, "should report failing test"
        assert "test_2" in formatted_report, "should report successful test"
        assert "failure reason" in formatted_report, "should report failure reason"

suite = TestReportTest.create_test_suite()
test_report = xunit.TestReport()
suite.run(test_report)
print(xunit.TestReportFormatter.format(test_report))
