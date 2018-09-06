from selenium import webdriver
import pytest
from selenium.webdriver.remote.file_detector import UselessFileDetector


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    # driver.file_detector = UselessFileDetector()
    # driver.implicitly_wait(30)
    yield driver
    # driver.quit()
    driver.close()
