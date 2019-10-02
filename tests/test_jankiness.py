import pytest
from os import environ

@pytest.mark.usefixtures("driver")
class TestPerformance:
    def setUpClass(self, driver):
        driver.get("https://googlechrome.github.io/devtools-samples/jank/")

        addBtn = driver.find_element_by_css_selector(".add")
        for x in range(10):
            addBtn.click()

    def test_jankiness_not_optimized(self, driver, request):
        self.setUpClass(driver)
        jankiness = driver.execute_script("sauce:jankinessCheck")
        '''
        returns tyhe following JSON object:
        {
            "url":"https://googlechrome.github.io/devtools-samples/jank/",
            "timestamp":1570026846192,
            "value":{
                "metrics":{
                    "averageFPS":30.37006789013138,
                    "scriptingTime":713,
                    "renderingTime":45,
                    "otherTime":1598,
                    "idleTime":2122,
                    "forcedReflowWarningCounts":440,
                    "scrollTime":5210,
                    "paintingTime":732,
                    "memoryUsageDiff":-2964452
                },
                "diagnostics":{
                    "layoutUpdateScore":0.9869911007302723,
                    "fpsScore":0.5061677981688564,
                    "idleDurationScore":0.4072936660268714,
                    "memoryUsageScore":1
                }
            },
            "score":0.6428077742596429,
            "loaderId":"b0099410-e521-11e9-b752-8375edd9807f",
            "type":"scroll"
        }
        '''
        assert jankiness["score"] < .7

    def test_jankiness_optimized(self, driver, request):
        self.setUpClass(driver)
        optimizeBtn = driver.find_element_by_css_selector(".optimize")
        optimizeBtn.click()
        jankiness = driver.execute_script("sauce:jankinessCheck")
        assert jankiness["score"] > .9
