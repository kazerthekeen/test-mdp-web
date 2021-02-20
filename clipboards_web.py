from website import website
from selenium.webdriver.common.by import By

class clipboards_web(website):
    #Clipboards doesn't route you to the login page on completeion so
    # we use the logout text to see if the login was a success
    welcome_text = "Logout"

    def checkout(self, dm, user, login):
        dm.get("https://clipboards.com/index.php?route=checkout/checkout", 7)
        return super().checkout(dm, user, login)

    def go_home(self, dm):
        dm.get("https://clipboards.com")

    def change_password(self, dm, test_user, password_key):
        if not dm.get_route() =="https://clipboards.com/index.php?route=account/account":
            dm.get("https://clipboards.com/index.php?route=account/account")
        super().change_password(dm, test_user, password_key)

    def make_account(self, dm, test_user):
        dm.get("https://clipboards.com/index.php?route=account/register")
        super().make_account(dm, test_user)

    def logout(self, dm):
        dm.click_by((By.XPATH, "//a[contains(text(),'Logout')]"))
        return super().logout(dm)

    def login_with_backup(self, dm, test_user):
        dm.click_by((By.XPATH, "//a[contains(text(),'My Account')]"))
        if not dm.value_in_source("SECURE LOGIN"):
            self.logout(dm)
            self.login_with_backup(self, dm, test_user)
        return super().login_with_backup(dm, test_user)

    def login(self, dm, test_user):
        dm.click_by((By.XPATH, "//a[contains(text(),'My Account')]"))
        if not dm.value_in_source("SECURE LOGIN"):
            self.logout(dm)
            self.login(self, dm, test_user)
        return  super().login(dm, test_user)

    def add_address(self, dm , user):
        if not dm.get_route() =="https://clipboards.com/index.php?route=account/account":
            dm.get("https://clipboards.com/index.php?route=account/account")
        dm.click_by((By.XPATH, "//a[contains(text(),'Modify your address book entries')]"))
        dm.click_by((By.XPATH, "//a[contains(text(),'New Address')]"))
        super().add_address(dm , user)

    def go_basic_product_page(self, dm):
        page = "https://clipboards.com/120-mm-Teal-Clipboard-Clip"
        self.go_product_page(dm, page)
