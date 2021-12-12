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
        self.test_reporter = xunit.TestReporter()

    def test_template_method(self):
        test = WasRun("should_run_test_method")
        test.run(self.test_reporter)
        assert(test.log == "setup test_method tear_down")

    def should_report_success(self):
        test = WasRun("should_run_test_method")
        test.run(self.test_reporter)
        assert(self.test_reporter.summary() == "1 run, 0 failed")

    def should_report_failure(self):
        broken_test = WasRun("test_broken_method")
        broken_test.run(self.test_reporter)
        assert(self.test_reporter.summary() == "1 run, 1 failed")

    def should_return_formatted_summary_report(self):
        test_result = xunit.TestResult("test")
        test_result.record_failure("some reason")
        self.test_reporter.record_test_result(test_result)
        assert(self.test_reporter.summary() == "1 run, 1 failed")

    def should_handle_setup_exception(self):
        test = RaiseSetupException("should_run_test_method")
        test.run(self.test_reporter)
        assert(self.test_reporter.summary() == "1 run, 1 failed")

    def test_suite(self):
        suite = xunit.TestSuite()
        suite.add(WasRun("should_run_test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.test_reporter)
        assert("2 run, 1 failed" == self.test_reporter.summary())

    def should_create_suite_from_defined_test_cases(self):
        suite = WasRun.create_test_suite()
        assert(suite.number_of_tests() == 2)

    def should_record_failure_reason(self):
        suite = WasRun.create_test_suite()
        suite.run(self.test_reporter)
        assert(len(self.test_reporter.test_results()) == 3)        
        assert(self.test_reporter.full_report()[0].reason() == "reason")

suite = TestCaseTest.create_test_suite()
test_reporter = xunit.TestReporter()
suite.run(test_reporter)
print(test_reporter.full_report())

class TestReportTest(xunit.TestCase):
    def setup(self):
        self.test_reporter = xunit.TestReporter()

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

    def should_report_test_details(self):
        test_result_one = xunit.TestResult("test_1")
        test_result_one.record_failure("reason 1")
        self.test_reporter.record_test_result(test_result_one)

        test_result_two = xunit.TestResult("test_2")
        self.test_reporter.record_test_result(test_result_two)

        test_result_three = xunit.TestResult("test_3")
        test_result_three.record_failure("reason 2")
        self.test_reporter.record_test_result(test_result_three)

        assert(self.test_reporter.summary() == "3 run, 2 failed")
        assert(self.test_reporter.full_report() == {"test_1": "reason 1", "test_3": "reason 2"})


suite = TestReportTest.create_test_suite()
test_reporter = xunit.TestReporter()
suite.run(test_reporter)
print(test_reporter.full_report())
