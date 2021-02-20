#import unittest
from my_driver import driver_manager
from mdpocket_web import mdpocket_web
from clipboards_web import clipboards_web
from selenium.webdriver.common.by import By
import fileinput
import json
import pytest
import random
import sys


def test_new_account_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    run_make_new_account(site, config)

def test_change_password_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    run_change_password(site, config)

def test_add_address_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    run_add_address(site, config)

def test_purchase_no_login_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    login = config["test_purchase_no_login"]
    run_purchase(site, config, login)

def test_custom_book():
    site = mdpocket_web()
    config = load_settings("testing.json")
    login = config["test_purchase_login"]
    url = config["book_url"]
    run_purchase_custom_book(site, config, login, url)

def test_purchase_login_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    login = config["test_purchase_login"]
    run_purchase(site, config, login)

def test_purchase_random_login_mdp():
    site = mdpocket_web()
    config = load_settings("testing.json")
    products = config["mdpocket_product_pages"]
    login = config["test_purchase_login"]
    product = random.choice(products)
    run_purchase(site, config, login, product)

def test_subscribe_mdp():
    config = load_settings("testing.json")
    run_subscribe(config)

def test_new_account_clipboards():
    config = load_settings("testing.json")
    run_make_new_account(clipboards_web(), config)

def test_change_password_clipboards():
    config = load_settings("testing.json")
    run_change_password(clipboards_web(), config)

def test_add_address_clipboards():
    config = load_settings("testing.json")
    run_add_address(clipboards_web(), config)

def test_purchase_no_login_clipboards():
    config = load_settings("testing.json")
    run_purchase(clipboards_web(), config, config["test_purchase_no_login"])

def test_purchase_login_clipboards():
    config = load_settings("testing.json")
    run_purchase(clipboards_web(), config, config["test_purchase_login"])

def test_purchase_random_login_clipboards():
    config = load_settings("testing.json")
    products = config["clipboards_product_pages"]
    run_purchase(clipboards_web(), config, config["test_purchase_login"],products[2])

def run_make_new_account(site, config):
    dm = driver_manager(config)
    try:
        site.make_account(dm, config["test_user1"])
        state =  dm.value_in_source("Your Account Has Been Created!")
        if state:
            assert( dm.value_in_source("Your Account Has Been Created!") )
            site.logout(dm)
            site.login(dm, config["test_user1"])
        else :
            if dm.value_in_source("Warning: E-Mail Address is already registered!") :
                pytest.skip("Testing account already exists, please reset testing environment")
            else:
                print("An unknown error occured")
    finally:
        dm.quit()

def run_change_password(site, config):
    dm = driver_manager(config)
    user = config["test_change_password"]
    try:
        site.go_home(dm)
        password_key = site.login_with_backup(dm, user)
        site.change_password(dm, user, password_key)
        site.logout(dm)
        user["password"] = user[password_key]
        assert site.login(dm, user)
    except:
        print("An error occured")
    finally:
        dm.quit()

def run_add_address(site, config):
    dm = driver_manager(config)
    user = config["test_add_address"]
    try:
        site.go_home(dm)
        site.login(dm, user)
        site.add_address(dm, user)
        assert dm.value_in_source("Your address has been successfully inserted")
    except Exception as e:
        print(e)
        dm.sleep(5)
    finally:
        dm.quit()

def run_purchase_custom_book(site, config, user, product_link):
    dm = driver_manager(config)
    try:
        site.go_home(dm)
        if (user["login"]):
            site.login(dm, user)
        site.purchase_custom_book(dm, product_link)
        checkout_success = site.checkout(dm, user, login=user["login"])
        assert checkout_success
    finally:
        dm.sleep(2)
        dm.quit()

def run_purchase(site, config, user, product_link=False):
    dm = driver_manager(config)
    try:
        site.go_home(dm)
        if (user["login"]):
            site.login(dm, user)
        if not product_link:
            site.go_basic_product_page(dm)
        else:
            site.go_product_page(dm, product_link)
        site.add_to_cart(dm)
        checkout_success = site.checkout(dm, user, login=user["login"])
        assert checkout_success
    finally:
        dm.sleep(2)
        dm.quit()

def run_subscribe(site, config):
    dm = driver_manager(config)
    try:
        site.go_home(dm)
        site.subscribe_to_newsletter(dm, config["test_subscribe"])
    finally:
        dm.quit()

def load_settings(file_name = "testing.json"):
    with open(file_name, 'r') as file:
        s = file.read()
    settings = json.loads(s)
    return settings

if __name__ == "__main__":
    pass
