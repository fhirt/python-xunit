import xunit
from xunit.assertion import expect, fail


class MockTestCase(xunit.TestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        self.log = "setup "

    def should_run_successful_test(self):
        self.log = self.log + "test_method "

    def tear_down(self):
        self.log = self.log + "tear_down"

    def test_broken_method(self):
        expect(1).to_be(2)

    def expect_value_to_be(self):
        expect(2).to_be(2)

    def this_should_do_that(self):
        expect(7).to_be(7)


class MockTestCaseWithSetupException(MockTestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        super().setup()
        raise Exception("setup failed")


class TestCaseTest(xunit.TestCase):

    def setup(self):
        self.test_report = xunit.Report()

    def should_run_setup_test_case_and_teardown(self):
        test = MockTestCase("should_run_successful_test")
        test.run(self.test_report)
        
        expect(test.log).to_be("setup test_method tear_down")

    def should_report_success(self):
        test = MockTestCase("should_run_successful_test")
        test.run(self.test_report)
        
        expect(self.test_report.run_count()).to_be(1)
        expect(self.test_report.failure_count()).to_be(0)

    def should_report_failure(self):
        broken_test = MockTestCase("test_broken_method")
        broken_test.run(self.test_report)
        
        expect(self.test_report.run_count()).to_be(1)
        expect(self.test_report.failure_count()).to_be(1)

    def should_run_teardown_after_setup_exception(self):
        test = MockTestCaseWithSetupException("should_run_successfull_test")
        test.run(self.test_report)
        
        expect(test.log).to_be("setup tear_down")


class TestSuiteTest(xunit.TestCase):
    def setup(self):
        self.test_report = xunit.Report()

    def should_run_all_test_cases_in_test_suite(self):
        suite = xunit.TestSuite()
        suite.add(MockTestCase("should_run_successful_test"))
        suite.add(MockTestCase("test_broken_method"))
        suite.run(self.test_report)
        expect(self.test_report.run_count()).to_be(2)
        expect(self.test_report.failure_count()).to_be(1)

    def should_add_test_cases_starting_with_should_and_test(self):
        suite = MockTestCase.create_test_suite()
        expect(suite.number_of_tests()).to_be(4)

    def should_record_failure_reason(self):
        suite = MockTestCase.create_test_suite()
        suite.run(self.test_report)
        test_results = self.test_report.test_results()["MockTestCase"]

        expect(self.test_report.run_count()).to_be(4)
        expect(self.test_report.failure_count()).to_be(1)

        failing_test = None
        for test_result in test_results:
            if test_result.failed():
                failing_test = test_result
        expect(failing_test.reason()).not_().to_be(None)


class TestReportTest(xunit.TestCase):

    def should_record_test_case_name(self):
        test_result = xunit.TestResult(MockTestCase("should_run_successful_test"))
        assert test_result.test_case() == "MockTestCase"

    def should_record_successful_test(self):
        test_result = xunit.TestResult(MockTestCase("should_run_successful_test"))
        
        expect(test_result.test_name()).to_be("should_run_successful_test")
        expect(test_result.failed()).to_be(False)
        expect(test_result.reason()).to_be(None)

    def should_record_failure_reason_for_unsuccessful_test(self):
        test_result = xunit.TestResult(MockTestCase("test_broken_method"))
        test_result.record_failure("reason")
        
        expect(test_result.test_name()).to_be("test_broken_method")
        expect(test_result.failed()).to_be(True)
        expect(test_result.reason()).to_be("reason")

    def should_format_test_report(self):
        test_report = xunit.Report()
        test_result_one = xunit.TestResult(MockTestCase("test_broken_method"))
        test_result_one.record_failure("failure reason")
        test_report.record_test_result(test_result_one)

        test_result_two = xunit.TestResult(MockTestCase("should_run_successful_test"))
        test_report.record_test_result(test_result_two)

        expect(test_report.run_count()).to_be(2)
        expect(test_report.failure_count()).to_be(1)

        formatted_report = xunit.DefaultFormatter.format(test_report)
        
        expect(formatted_report).to_contain("MockTestCase")
        expect(formatted_report).to_contain("test_broken_method")
        expect(formatted_report).to_contain("should_run_successful_test")
        expect(formatted_report).to_contain("failure reason")


class RunnerTest(xunit.TestCase):
    def should_setup_and_run_specified_test_suites(self):
        mock_suite_one = MockTestCase.create_test_suite()
        mock_suite_two = MockTestCaseWithSetupException.create_test_suite()

        runner = xunit.Runner()
        runner.add(mock_suite_one, mock_suite_two)
        formatted_report = runner.run()

        expect(runner.run_count()).to_be(8)
        expect(runner.failure_count()).to_be(5)
        expect(formatted_report).to_contain("MockTestCase")
        expect(formatted_report).to_contain("MockTestCaseWithSetupException")


class AssertionTest(xunit.TestCase):
    def expect_value_to_be_should_raise_assertion_error(self):
        try:
            expect(3).to_be(2)
        except AssertionError as ae:
            expect(3).to_be_in(ae)
            expect(2).to_be_in(ae)

    def expect_value_to_be_should_pass_assertion(self):
        expect(2).to_be(2)
        expect("one").to_be("one")
        expect(MockTestCase).to_be(MockTestCase)
        expect(range(4)).to_be(range(4))
        expect([1, 3, 7]).to_be([1, 3, 7])

    def expect_value_to_contain_should_pass_assertion(self):
        expect("a string").to_contain("str")
        expect(range(5)).to_contain(3)
        expect({"a_key": "a_value", "b_key": "b_value"}).to_contain("b_key")

    def expect_value_to_contain_should_raise_assertion_error(self):
        try:
            expect(range(5)).to_contain(7)
        except AssertionError as ae:
            expect(7).to_be_in(ae)
            expect("range(0, 5)").to_be_in(ae)

    def expect_value_to_be_in_should_pass_assertion(self):
        expect(8).to_be_in(range(10))
        expect(3).to_be_in([1, 3, 5, 7])
        expect("hello").to_be_in("hello world")
        expect("key").to_be_in({"key": "value"})

    def expect_lambda_to_raise_expected_exception_passes(self):
        message = expect(lambda: fail("reason")).to_raise(AssertionError)
        expect(message).to_be("reason")

    def expect_lambda_to_raise_unexpected_exception_fails(self):
        try:
            message = expect(lambda: fail("reason")).to_raise(NameError)
        except Exception as error:
            expect(type(error)).to_be(AssertionError)
        else:
            fail("no exception was raised")

    def expect_lambda_to_raise_no_exception_to_fail(self):
        try:
            message = expect(lambda: 1 + 1).to_raise(Exception)
        except Exception as error:
            expect(type(error)).to_be(AssertionError)
        else:
            fail("no exception was raised")

    def should_negate_assertion(self):
        expect(1).not_().to_be(2)
        expect(5).not_().to_be_in([1, 2, 3])
        expect("hello world").not_().to_contain("ciao")


runner = xunit.Runner()
runner.add(TestCaseTest.create_test_suite(), TestSuiteTest.create_test_suite(),
           TestReportTest.create_test_suite(), RunnerTest.create_test_suite(), AssertionTest.create_test_suite())
formatted_report = runner.run()
print(formatted_report)
