import xunit

class WasRun(xunit.TestCase):
    def __init__(self, name) -> None:
        super().__init__(name)

    def setup(self):
        self.log = "setup "

    def test_method(self):
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
        self.result = xunit.TestResult()    
    
    def test_template_method(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert(test.log == "setup test_method tear_down")

    def test_result(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert(self.result.summary() == "1 run, 0 failed")

    def test_failed_result(self):
        broken_test = WasRun("test_broken_method")
        broken_test.run(self.result)
        assert(self.result.summary() == "1 run, 1 failed")
        
    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed("test", "some reason")
        assert(self.result.summary() == "1 run, 1 failed")
        
    def test_should_handle_setup_exception(self):
        test = RaiseSetupException("test_method")
        test.run(self.result)
        assert(self.result.summary() == "1 run, 1 failed")

    def test_suite(self):
        suite = xunit.TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.result)
        assert("2 run, 1 failed" == self.result.summary())
        
    def test_result_details(self):
        self.result.test_started()
        self.result.test_failed("test_1", "reason 1")
        self.result.test_started()
        self.result.test_started()
        self.result.test_failed("test_3", "reason 2")
        assert(self.result.summary() == "3 run, 2 failed")
        assert(self.result.details() == { "test_1": "reason 1", "test_3": "reason 2"})
        
    def test_should_create_suite_from_test_case(self):
        suite = WasRun.create_test_suite()
        assert(suite.number_of_tests() == 2)
        
suite = TestCaseTest.create_test_suite()
result = xunit.TestResult()       
suite.run(result)

print(result.summary())
print(result.details())
