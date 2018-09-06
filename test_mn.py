import PageObject
from PageObject import HomePage, BasePage, DataPreparation, Settings, DataPage, DataSelection, VariableSelection
import pytest
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selene import elements
import robot

# def test_log_in(driver):
#     header = PageObject.HomePage(driver).static_login().log_in("admin@example.com", "password").header()
#     assert header == "Segmentation Builder"


def test_upload_file(driver):
    # tables are populated with the data (objects with dataTables_wrapper class are created)
    HomePage(driver).static_log_in().\
        upload_data_file("/Data.sav")
    table = driver.find_elements(By.CLASS_NAME, "dataTables_wrapper")
    assert len(table) == 3


# to think about missing value and outliers testing
def test_miss(driver):
    HomePage(driver).static_log_in().\
        enable_nbs(True).\
        upload_data_file("/Data.sav").\
        btn_missing_value_treatment().\
        trying()


def test_nbs_map_var(driver):
    HomePage(driver).static_log_in().\
        enable_nbs(True).\
        upload_data_file("/Data.sav").\
        map_custid()
    sleep(1)
    assert driver.find_element(By.XPATH, "//div/table/thead/tr/th[1]").text == "RespondentID"


def test_map_from_file(driver):
    HomePage(driver).static_log_in().\
        enable_nbs(False).\
        upload_data_file("/trans.csv").\
        map_from_file("/map_trans.csv")
    sleep(5)
    assert driver.find_element(By.XPATH, "//div/table/thead/tr/th[2]").text == "CustID"


def test_cluster_solution(driver):
    HomePage(driver).static_log_in(). \
        enable_nbs(True). \
        upload_data_file("/Data.sav"). \
        map_custid().\
        go_to_data_selection().\
        select_valid()
    DataSelection(driver).go_to_variable_selection().\
        select_all()
    VariableSelection(driver).go_to_cluster_analysis().\
        perform_clustering().\
        deselect_solution("a")
    sleep(1)
    assert driver.find_element(By.XPATH, "//*[@id='KM_UI_tables']/div/div[3]").get_attribute("style") == "width: 0%;"


if __name__ == "__main__":
    pytest.main()