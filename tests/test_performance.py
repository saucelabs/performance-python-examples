import pytest
from os import environ

@pytest.mark.usefixtures("driver")
class TestPerformance:
    def setUpClass(self, driver):
        driver.get("https://www.saucedemo.com")
        driver.find_element_by_css_selector("[data-test='username']").send_keys(
            environ.get("PERF_USERNAME", "standard_user"))
        driver.find_element_by_css_selector("[data-test='password']").send_keys("secret_sauce")
        driver.find_element_by_class_name("btn_action").click()
        driver.get("https://www.saucedemo.com/inventory.html")

    def test_performance_page_weight(self, driver, request):
        self.setUpClass(driver)
        performance = driver.execute_script("sauce:performance", {"name": request.node.name, "metrics": ["load"]})
        '''
        The custom command will return 'pass' if the test falls within the predicted baseline
	    or 'fail'  if the performance metric falls outside the predicted baseline.
        customers can decide how strict they want to be in failing tests by setting thier own
        failure points.
        assert(details[metric].actual < 5000, true, reason);
        '''
        if(performance["result"] != "pass"):
            assert performance["details"]["load"]["actual "] < 5000
        else:
            assert performance["result"] == "pass"

    def test_performance_timeToFirstInteractive(self, driver, request):
        self.setUpClass(driver)
        performance = driver.execute_script("sauce:performance", {
                                            "name": request.node.name, "metrics": ["timeToFirstInteractive"]})
        if(performance["result"] != "pass"):
            assert performance["details"]["timeToFirstInteractive"]["actual "] < 5000
        else:
            assert performance["result"] == "pass"
