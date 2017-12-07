from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("http://dev.sb.4tree.de")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "html/body/div/div[1]/div/div[2]/div[1]/a/button")))

    def static_login(self):
        self.driver.find_element(By.XPATH, "html/body/div/div[1]/div/div[2]/div[2]/a/button").click()
        return LogInPage(self.driver)

    def ldap_login(self):
        self.driver.find_element(By.XPATH, "html/body/div/div[1]/div/div[2]/div[1]/a/button").click()
        return LogInPage(self.driver)


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
        return SB1Page(self.driver)


class SB1Page(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME("iframe")))
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "configurationBtn")))

    def header(self):
        return self.driver.find_element(By.CLASS_NAME, "breadcrumbTitle_3SJFe").text


