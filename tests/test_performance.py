import pytest
from os import environ

@pytest.mark.usefixtures("driver")
class TestPerformance:
    def setUpClass(self, driver):
        driver.get("https://www.saucedemo.com")
        driver.find_element_by_css_selector("[data-test='username']").send_keys(
            environ.get("PERF_USERNAME", "standard_user"))
        driver.find_element_by_css_selector("[data-test='password']").send_keys("secret_sauce")
        driver.find_element_by_class_name("login-button").click()
        driver.get("https://www.saucedemo.com/inventory.html")

    def test_performance_page_weight(self, driver, request):
        self.setUpClass(driver)
        performance = driver.execute_script("sauce:performance", {"name": request.node.name, "metrics": ["pageWeight"]})
        assert performance["result"] == "pass"

    def test_performance_speed_index(self, driver, request):
        self.setUpClass(driver)
        performance = driver.execute_script("sauce:performance", {"name": request.node.name, "metrics": ["speedIndex"]})
        assert performance["result"] == "pass"
    