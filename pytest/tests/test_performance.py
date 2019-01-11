import pytest
import time
from os import environ


@pytest.mark.usefixtures("driver")
class TestPerformance:
    def setUpClass(self, driver):
        driver.get("https://www.saucedemo.com")
        driver.find_element_by_css_selector("[data-test='username']").send_keys(
            environ.get("PERF_USERNAME", "standard_user"), "standard_user")
        driver.find_element_by_css_selector("[data-test='password']").send_keys("secret_sauce")
        driver.find_element_by_class_name("login-button").click()
        driver.get("https://www.saucedemo.com/inventory.html")

    def test_main_js(self, driver):
        self.setUpClass(driver)
        network = driver.execute_script("sauce:log", {"type": "sauce:network"})
        # is_request_exists = network.some(req.url.includes("main.js"))
        is_request_exists = False
        for x in network:
            if "main.js" in x["url"]:
                is_request_exists = True

        assert is_request_exists is True

    def test_page_load(self, driver):
        self.setUpClass(driver)
        metrics = driver.execute_script("sauce:log", {"type": "sauce:metrics"})
        pageLoadTime = metrics["domContentLoaded"] - metrics["navigationStart"]
        assert pageLoadTime<=5

    def test_timing(self, driver):
        self.setUpClass(driver)
        timing = driver.execute_script("sauce:log", {"type": "sauce:timing"})
        assert "domLoading" in timing

    def test_speed_index(self, driver):
        self.setUpClass(driver)
        metrics = ["load", "speedIndex", "pageWeight", "pageWeightEncoded", "timeToFirstByte",
                   "timeToFirstInteractive", "firstContentfulPaint", "perceptualSpeedIndex", "domContentLoaded"]
        performance = driver.execute_script("sauce:log", {"type": "sauce:performance"})
        for metric in metrics:
            assert metric in performance

    def test_hello(self, driver, request):
        self.setUpClass(driver)
        hello = driver.execute_script("sauce:hello", {"name": request.node.name })
        assert request.node.name in hello
