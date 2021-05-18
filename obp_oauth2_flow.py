# ©2021 TESOBE GmbH
# thx to Selenium IDE
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3 as published by the Free Software Foundation with the
# addition of the following permission added to Section 15 as permitted in Section 7(a): FOR ANY PART OF THE COVERED
# WORK IN WHICH THE COPYRIGHT IS OWNED BY ITEXT GROUP NV, ITEXT GROUP DISCLAIMS THE WARRANTY OF NON INFRINGEMENT OF
# THIRD PARTY RIGHTS This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details. You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see http://www.gnu.org/licenses/ or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA, 02110-1301 USA, or download the license from the following URL:
# http://itextpdf.com/terms-of-use/ The interactive user interfaces in modified source and object code versions of
# this program must display Appropriate Legal Notices, as required under Section 5 of the GNU Affero General Public
# License. In accordance with Section 7(b) of the GNU Affero General Public License, you must retain the producer
# line in every PDF that is created or manipulated using iText. You can be released from the requirements of the
# license by purchasing a commercial license. Buying such a license is mandatory as soon as you develop commercial
# activities involving the iText software without disclosing the source code of your own applications. These
# activities include: offering paid services to customers as an ASP, serving PDFs on the fly in a web application,
# shipping iText with a closed source product.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from testmail import get_otp
from time import sleep
import logging

# Configure logleve here logging.INFO for production, logging.DEBUG for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('default')
# This is the time we wait between clicking a button on the final presentation at the end of the flow
# and reading the result. Adjust to your needs.
sleeptime = 20


class ObpOAuth2Flow():
    # Use firefox for human eye
    def setup_method_firefox(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox()
        self.vars = {}

    # headless chrome for automated tests
    def setup_method_chrome_headless(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.vars = {}
        except Exception as e:
            logger.exception("could not create webdriver: " + str(e))
            exit(1)

    def teardown_method(self):
        self.driver.quit()

    def show_accountsBG(self, url, bank, iban, username, password, mail_host="DUMMY", mail_user=None, mail_password=None, accounts_only=True):
        self.driver.get(url)
        self.driver.set_window_size(960, 554)
        self.driver.find_element(By.LINK_TEXT, "Berlin Group").click()
        self.driver.find_element(By.ID, "bank").click()
        dropdown = self.driver.find_element(By.ID, "bank")
        dropdown.find_element(By.XPATH, f"//option[. = '{bank}']").click()
        self.driver.find_element(By.ID, "iban").click()
        element = self.driver.find_element(By.ID, "iban")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "iban").send_keys(iban)
        self.driver.find_element(By.NAME, "consents").click()
        if not accounts_only:
            self.driver.find_element(By.CSS_SELECTOR, ".checkbox:nth-child(2) input").click()
            self.driver.find_element(By.CSS_SELECTOR, "form").click()
            self.driver.find_element(By.CSS_SELECTOR, ".checkbox:nth-child(3) input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.NAME, "submit").click()
        self.driver.find_element(By.NAME, "submit").click()
        self.driver.find_element(By.ID, "password").click()
        otp = get_otp(mail_host, mail_user, mail_password)
        logger.debug("Extracted OTP: " + str(otp))
        self.driver.find_element(By.ID, "password").send_keys(otp)
        self.driver.find_element(By.NAME, "submit").click()
        accounts = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "get_accounts_bg")))
        accounts.click()
        sleep(2)
        logger.debug("look for account list: ")
        text_account_list = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "account_list_bg")))
        logger.debug(text_account_list.get_attribute("innerText"))
        account_details_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "get_account_detail_bg")))
        account_details_button.send_keys(Keys.ENTER)
        sleep(sleeptime)
        logger.debug("look for account details: ")
        text_account_details = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".account_detail_bg")))
        logger.debug(text_account_details.text)
        assert "resourceId" in text_account_details.text
        balances_button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "get_balances_bg")))
        balances_button.send_keys(Keys.ENTER)
        sleep(sleeptime)
        logger.debug("look for balances: ")
        text_balances = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".balances_bg")))
        logger.debug(text_balances.text)
        if accounts_only:
            assert "OBP-20060: User does not have access to the view ReadAccountsBerlinGroup" in text_balances.text
        else:
            assert "balanceAmount" in text_balances.text
        transactions_button = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".get_transactions_bg")))
        transactions_button.send_keys(Keys.ENTER)
        sleep(sleeptime)
        logger.debug("look for transactions")
        text_transactions = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".transactions_bg")))
        logger.debug(text_transactions.text)
        if accounts_only:
            assert "OBP-20061: Current user does not have access to the view ReadTransactionsBerlinGroup" in text_transactions.text
        else:
            assert "booked" in text_transactions.text


    def list_consents_and_delete_oldest_consentBG(self, url, bank, username, password):
        self.driver.get(url)
        self.driver.set_window_size(960, 554)
        self.driver.find_element(By.LINK_TEXT, "List Consents").click()
        self.driver.find_element(By.ID, "bank").click()
        dropdown = self.driver.find_element(By.ID, "bank")
        dropdown.find_element(By.XPATH, f"//option[. = '{bank}']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.NAME, "submit").click()
        chk = self.driver.find_elements_by_xpath("//input[@type='checkbox']")
        chk[-1].click()
        self.driver.find_element(By.NAME, "submit").click()
        alert = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
        assert "Warning! All selected consents have been deleted!" in alert













