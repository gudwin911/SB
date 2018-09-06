from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selenium import webdriver
from time import sleep


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def scroll_down(self, num):
        self.driver.execute_script("window.scrollTo(0, %s);" % num)


class DataPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def settings(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "configurationBtn")))
        except TimeoutException:
            print("ConfButton: TimeoutException")
        elm = self.driver.find_element(By.ID, "configurationBtn")
        elm.click()
        return Settings(self.driver)

    def go_to_data_selection(self):
        # TODO: make table wrapper ID changeable
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "DataTables_Table_5_wrapper")))
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "2 Data Selection")))
        sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "2 Data Selection").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DataTables_Table_7_wrapper")))
        return DataSelection(self.driver)

    def go_to_variable_selection(self):
        # TODO: make table wrapper ID changeable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "3 Variable Selection")))
        sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "3 Variable Selection").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "DataTables_Table_8_wrapper")))
        return VariableSelection(self.driver)

    def go_to_cluster_analysis(self):
        # TODO: make table wrapper ID changeable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "4 Cluster Analysis")))
        sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "4 Cluster Analysis").click()
        return ClusterAnalysis(self.driver)


class Settings(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "settings_enable_nds")))
        sleep(1)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "settings_enable_nds")))

    def settings_check_nbs(self):
        return self.driver.execute_script("return $(id=settings_enable_nds).prop('checked')")

    def enable_nbs(self, true):
        check = self.settings_check_nbs()
        if check & true:
            pass
        elif (not check) & (not true):
            pass
        else:
            self.driver.find_element(By.XPATH, "//*[@id='settings_dialog']/div/div/div[2]/div[3]/div/div/div/label/span").click()

    def settings_save(self):
        self.driver.find_element(By.ID, "settings_save").click()
        return DataPage(self.driver)


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://dev.nptb.periscope-solutions.com")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "html/body/div/div[1]/div/div[2]/div[1]/a/button")))

    def static(self):
        self.driver.find_element(By.XPATH, "html/body/div/div[1]/div/div[2]/div[2]/a/button").click()
        return LogInPage(self.driver)

    def ldap(self):
        self.driver.find_element(By.XPATH, "html/body/div/div[1]/div/div[2]/div[1]/a/button").click()
        return LogInPage(self.driver)

    def static_log_in(self):
        return HomePage(self.driver).static().log_in("admin@example.com", "password")


class LogInPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginButton")))

    def username(self, name):
        field = self.driver.find_element(By.ID, "login")
        field.send_keys(name)

    def password(self, password):
        field = self.driver.find_element(By.ID, "password")
        field.send_keys(password)

    def login(self):
        button = self.driver.find_element(By.ID, "loginButton")
        button.click()

    def log_in(self, name, password):
        self.username(name)
        self.password(password)
        self.login()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, "iframe"))
        return DataPreparation(self.driver)


class DataPreparation(DataPage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-file")))

    def enable_nbs(self, true):
        self.settings()
        Settings(self.driver).enable_nbs(true)
        Settings(self.driver).settings_save()
        return DataPreparation(self.driver)

    def header(self):
        return self.driver.find_element(By.CLASS_NAME, "breadcrumbTitle_3SJFe").text

    def upload_data_file(self, data_file):
        browse_btn = self.driver.find_element(By.XPATH, "//input[@type='file']")
        browse_btn.send_keys(os.getcwd()+data_file)
        # TODO: make table wrapper ID changeable [2;?] with step 3
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "DataTables_Table_2_wrapper")))
        return DataPreparation(self.driver)

    def map_var_btn(self):
        # TODO: find a decision to get rid of sleep on disable nbs mapping
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "DP_active_meta")))
        sleep(0.5)
        return self.driver.find_element(By.ID, "DP_active_meta")

    def nbs_derive_tnb_btn(self):
        return self.driver.find_element(By.ID, "DP_topnbox")

    def nbs_btn_convert_to_num_btn(self):
        return self.driver.find_element(By.ID, "DP_derivenum")

    def nbs_convert_all_to_num(self):
        self.driver.find_element(By.ID, "DP_derivenum_all").click()
        return DataPreparation(self.driver)

    def btn_outliers_treatment(self):
        self.driver.find_element(By.ID, "DP_Outliers_treatment").click()
        return OutliersTreatment(self.driver)

    def btn_missing_value_treatment(self):
        self.driver.find_element(By.ID, "DP_Missing_treatment").click()
        return MissingValueTreatment(self.driver)

    def click_map(self):
        self.map_var_btn().click()
        return MapVar(self.driver)

    def map_custid(self):
        self.click_map().cust_id()
        MapVar(self.driver).apply()
        return DataPreparation(self.driver)

    def map_from_file(self, data_file):
        self.click_map()
        MapVar(self.driver).map_from_file(data_file)
        return DataPreparation(self.driver)


class MapVar(BasePage):
    # TODO: idea with respondent and cust ids
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "VS_meta_method")))
        sleep(1)
        if self.driver.find_element(By.ID, "DP_Period_tag").is_displayed():
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'CustID')]")))
        else:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'RespondentID')]")))

    def apply(self):
        self.driver.find_element(By.ID, "DP_map_variables_apply").click()
        return DataPreparation(self.driver)

    def cancel(self):
        self.driver.find_element(By.ID, "DP_map_variables_cancel").click()
        return DataPreparation(self.driver)

    def close(self):
        self.driver.find_element(By.XPATH, "//*[@id='DP_meta_act']/div/div/div[1]/button")
        return DataPreparation(self.driver)

    def cust_id(self):
        # TODO: make it work not through ass
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "htAutocompleteArrow")))
        self.driver.find_element(By.CLASS_NAME, "htAutocompleteArrow").click()
        self.driver.find_element(By.CLASS_NAME, "htAutocompleteArrow").click()
        self.driver.find_element(By.ID, "VS_meta_method").click()

    def map_cust(self):
        self.cust_id()
        self.apply()
        return DataPreparation(self.driver)

    # TODO: make it work not through ass
    def map_from_file(self, data_file):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='VS_meta_method']/div/div[2]/label/input")))
        sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='VS_meta_method']/div/div[2]/label/input").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DP_input_meta_file_progress")))
        browse_btn = self.driver.find_element(By.ID, "DP_input_meta_file")
        browse_btn.send_keys(os.getcwd() + data_file)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "DP_map_variables_apply")))
        sleep(1)
        self.driver.find_element(By.ID, "DP_map_variables_apply").send_keys("\n")
        self.apply()
        return DataPreparation(self.driver)


# TODO: fill them in
class OutliersTreatment(BasePage):
    pass


class MissingValueTreatment(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DP_missing_treatment_table")))

    def trying(self, imp):
        # TODO: example. overwrite it
        sleep(3)
        self.driver.find_element(By.XPATH, "//*[@id='DP_missing_treatment_table']/div[1]/div/div/div/table/tbody/tr[1]/td[2]/div").click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[contains(@id, 'ht_')]/div[1]/div/div/div/table/tbody/tr[%s]/td" % imp).click()


class DataSelection(DataPage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DS_table")))

    def select_valid(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "DS_select_valid")))
        self.driver.find_element(By.ID, "DS_select_valid").click()

    def deselect(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "DS_select_none")))
        self.driver.find_element(By.ID, "DS_select_none").click()

    def nbs_rbn_btn(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "DS_respond")))
        self.driver.find_element(By.ID, "DS_respond").click()
        return RBN(self.driver)

    def categorical_table(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DS_profiling_table")))
        return self.driver.find_element(By.ID, "DS_profiling_table")


class RBN(BasePage):
    # TODO: make table wrapper ID changeable
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "DataTables_Table_8_wrapper")))


class VariableSelection(DataPage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "VS_table")))

    # TODO: remove sleep
    def select_all(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VS_select_all")))
        sleep(0.5)
        self.driver.find_element(By.ID, "VS_select_all").click()

    def deselect(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VS_select_none")))
        self.driver.find_element(By.ID, "VS_select_none").click()


class ClusterAnalysis(DataPage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CA_perform_clustering")))

    def perform_clustering(self):
        self.driver.find_element(By.ID, "CA_perform_clustering").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "KM_UI_tables")))
        return ClusterAnalysis(self.driver)

    def deselect_solution(self, solution):
        num = 0
        if solution == "a" or "A":
            num = 1
        elif solution == "b" or "B":
            num = 2
        elif solution == "c" or "C":
            num = 3
        else:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='KM_UI_settings']/div/div/div[%s]"
                                                      "/div[1]/div/div/label/div" % num)))
        sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='KM_UI_settings']/div/div/div[%s]/div[1]/div/div/label/div" % num)\
            .click()
        return ClusterAnalysis(self.driver)
