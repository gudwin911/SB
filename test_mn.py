import PageObject
import pytest
from selenium.webdriver.common.by import By
from time import sleep


# def test_log_in(driver):
#     header = PageObject.HomePage(driver).static_login().log_in("admin@example.com", "password").header()
#     assert header == "Segmentation Builder"


def test_upload_file(driver):
    PageObject.HomePage(driver).static_login().log_in("admin@example.com", "password")
    # sleep(10)
    elm = driver.find_element(By.CLASS_NAME, "btn-file")
    elm.click()
    elm.send_keys("C:/Users/User/Desktop/2010_GrocerySegmentationLOP.sav")