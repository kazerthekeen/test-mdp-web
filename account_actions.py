#import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from my_driver import driver_manager

BROWSER = "Firefox"

"""driver = get_firefox_driver()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
"""

def test_make_account(browser):
    dm = driver_manager(browser)
    dm.get("https://mdpocket.com/index.php?route=account/register")
    dm.submit_value_by_id("input-firstname", "tester")
    dm.submit_value_by_id("input-lastname", "auto")
    dm.submit_value_by_id("input-email", "mdpocket-test@maildrop.cc")
    dm.submit_value_by_id("input-telephone", "1234567890")
    dm.submit_value_by_id("input-password", "password123")
    dm.submit_value_by_id("input-confirm", "password123")
    dm.submit_value_by_id("input-address-1", "7621 Branch st")
    dm.submit_value_by_id("input-postcode", "27320")
    dm.submit_value_by_id("input-city", "reidsville")
    dm.submit_value_by_id("input-zone", "North Carolina", False)
    dm.click_by_name("agree")
    dm.click_by_xpath("//input[@value='Continue']")
    assert dm.value_in_source("Your Account Has Been Created!")


test_make_account("Firefox")
