from selenium import webdriver
import pytest


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    #driver.implicitly_wait(30)
    yield driver
    driver.quit()
