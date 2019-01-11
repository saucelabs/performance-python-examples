import pytest
from os import environ

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection


@pytest.fixture(scope='function')
def driver(request):
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = {}
    
    browser = {
        "platform": "Windows 10",
        "browserName": "chrome",
        "version": "latest",
        "extendedDebugging": True
    }

    desired_caps.update(browser)
    test_name = request.node.name
    username = environ.get('SAUCE_USERNAME', None)
    access_key = environ.get('SAUCE_ACCESS_KEY', None)

    selenium_endpoint = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key)
    desired_caps['name'] = test_name

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps
    )
    yield browser

    def fin():
        browser.execute_script("sauce:job-result={}".format(str(not request.node.rep_call.failed).lower()))
        browser.quit()
    request.addfinalizer(fin)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)