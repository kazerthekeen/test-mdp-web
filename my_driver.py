from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

class driver_manager():

    def __init__(self, browser_type="Firefox"):
        if browser_type == "Firefox":
            self.set_firefox_driver()
        else:
            self.driver = None

    def set_firefox_driver(self):
        binary = FirefoxBinary('/usr/lib64/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=binary, executable_path='/home/kazer/Programs/Libraries/geckodriver-v0.27.0-linux64/geckodriver')

    def submit_value_by_id(self, id, value, clear = True):
        elem = self.driver.find_element_by_id(id)
        if clear:
            elem.clear()
        elem.send_keys(value)

    def click_by_id(self, id):
        elem = self.driver.find_element_by_id(id)
        elem.click()

    def click_by_name(self, name):
        elem = self.driver.find_element_by_name(name)
        elem.click()

    def click_by_xpath(self, path):
        elem = self.driver.find_element_by_xpath(path)
        elem.click()

    def get(self, value):
        self.driver.get(value)

    def value_in_source(self, value):
        return value in self.driver.page_source
