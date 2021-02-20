"""
This is my webdriver class I use to call common sequences of operations on
the driver itself.
"""
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException, UnexpectedAlertPresentException,  TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ARROW_DOWN = u'\ue015'

class driver_manager():

    def __init__(self, config, delay=30):
        if config["browser_type"] == "Firefox":
            self.set_firefox_driver(config)
        elif config["browser_type"] =="Chrome":
            self.set_chrome_driver(config)
        else:
            self.driver = None
        self.delay = delay

    def set_chrome_driver(self, config):
        self.driver = webdriver.Chrome(executable_path=config["chrome_executable_path"])

    def set_firefox_driver(self, config):
        binary = FirefoxBinary(config["firefox_browser_bin"])
        self.driver = webdriver.Firefox(firefox_binary=binary, executable_path=config["firefox_executable_path"])

    def submit_value_by_id(self, id, value, clear = True, submit=False):
        elem = self.driver.find_element_by_id(id)
        self.__submit(elem, value, clear, submit)

    def submit_value_by_xpath(self, path, value, clear = True, submit=False):
        elem = self.driver.find_element_by_xpath(path)
        self.__submit(elem, value, clear, submit)

    def submit_value_by_name(self, name, value, clear = True, submit=False):
        elem = self.driver.find_element_by_name(name)
        self.__submit(elem, value, clear, submit)

    def select_value_by_id(self, id, value , tries = 0):
        try:
            elem = self.driver.find_element_by_id(id)
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == value:
                    break
                else:
                    elem.send_keys(ARROW_DOWN)
        except StaleElementReferenceException as e:
            if tries >3:
                raise e
            self.sleep(1)
            self.select_value_by_id(id, value, tries + 1)

    def select_all_required(self, xpath):
        try:
            elems = self.driver.find_elements_by_xpath(xpath)
            if len(elems)>0:
                for elem in elems:
                    ARROW_DOWN = u'\ue015'
                    elem.send_keys(ARROW_DOWN)
                    elem.send_keys(ARROW_DOWN)

        except StaleElementReferenceException as e:
            if tries >3:
                raise e
            self.sleep(1)
            self.select_value_by_id(id, xpath)

    def __submit(self, elem, value, clear, submit):
        if clear:
            elem.clear()
            self.wait()
        elem.send_keys(value)
        self.wait()
        if submit:
            elem.submit()
            self.wait()

    def wait(self, timeout=-1, condition=None):
        if condition is not None:
            return WebDriverWait(self.driver, timeout).until( condition)
        else:
            if timeout < 0:
                timeout = self.delay
            self.driver.implicitly_wait(timeout)

    def click_by(self, by_Ref, timeout=5):
        elem = self.wait(timeout, EC.element_to_be_clickable(by_Ref))
        elem.click()
        self.wait()

    def get(self, value, timeout=5):
        self.driver.get(value)
        sleep(1)

        try :
            alert = self.driver.switch_to_alert()
            alert.accept()
        except NoAlertPresentException:
            pass
        finally:
            self.wait(timeout, EC.url_contains(value))

    def value_in_source(self, value):
        return value in self.driver.page_source

    def get_route(self):
        return self.driver.current_url

    def sleep(self, t):
        sleep(t)

    def quit(self):
        self.driver.quit()

    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def maximize(self):
        self.driver.maximize_window()

    def confirm_alert(self, func, *args, **kwargs):
        try:
            func(*args)
        except UnexpectedAlertPresentException:
            self.wait(8, EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            alert.accept()
            dm.sleep(1)
            if kwargs.get("retry", True):
                func(*args)
