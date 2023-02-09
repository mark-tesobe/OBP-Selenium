from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ObpAPI:
    URI = "https://test.openbankproject.com"

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(ObpAPI.URI)

    def _find_element_by_id(self, value: str) -> WebElement:
        return self._find_element(By.ID, value)

    def _find_element_by_class_name(self, value: str) -> WebElement:
        return self._find_element(By.CLASS_NAME, value)

    def _find_element(self, by: str, value: str) -> WebElement:
        return self.driver.find_element(by, value)


class RegisterLogin(ObpAPI):
    EMAIL = "user@tesobe.com"
    USERNAME = "marksilva"
    PASSWORD = "sQZV0coC"

    def __init__(self) -> None:
        ObpAPI.__init__(self)

    def click_register(self) -> RegisterLogin:
        self.driver.find_element(By.ID, "register-link").click()
        return self

    def register(self) -> RegisterLogin:
        self._find_element_by_id("txtFirstName").send_keys("Mark")
        self._find_element_by_id("txtLastName").send_keys("Silva")
        self._find_element_by_id("txtEmail").send_keys(RegisterLogin.EMAIL)
        self._find_element_by_id("txtUsername").send_keys(RegisterLogin.USERNAME)
        self._find_element_by_id("textPassword").send_keys(RegisterLogin.PASSWORD)
        self._find_element_by_id("textPasswordRepeat").send_keys(RegisterLogin.PASSWORD)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "terms_checkbox").click()))
        self._find_element_by_id("privacy_checkbox").click()
        self._find_element_by_id("submit-button").click()
        # username_text = self._find_element_by_id("authuser_username").text
        # assert username_text != "Unique username."
        return self

    def click_logon(self) -> RegisterLogin:
        self._find_element_by_class_name("btn.btn-danger.login").click()
        return self

    def login(self) -> RegisterLogin:
        self._find_element_by_id("username").send_keys(RegisterLogin.USERNAME)
        self._find_element_by_id("password").send_keys(RegisterLogin.PASSWORD)
        self._find_element_by_class_name("submit").click()
        # error = self._find_element_by_class_name("toast.toast-error").text
        # assert error != "Error. Invalid Login Credentials"
        return self


if __name__ == "__main__":
    print("Running OBP-API Selenium test..")
    # RegisterLogin().click_register().register()
    RegisterLogin().click_register().register().click_logon().login()
