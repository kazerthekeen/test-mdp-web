from website import website
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class mdpocket_web(website):
    welcome_text = "Welcome to MDpocket.com!"

    def checkout(self, dm, user, login):
        dm.confirm_alert(dm.get, "https://mdpocket.com/index.php?route=checkout/checkout")
        return super().checkout(dm, user, login)

    def go_home(self, dm):
        dm.get("https://mdpocket.com")

    def change_password(self, dm, test_user, password_key):
        if not dm.get_route() =="https://mdpocket.com/index.php?route=account/account":
            dm.get("https://mdpocket.com/index.php?route=account/account")
        super().change_password(dm, test_user, password_key)

    def make_account(self, dm, test_user):
        dm.get("https://mdpocket.com/index.php?route=account/register")
        super().make_account(dm, test_user)

    def logout(self, dm):
        dm.get("https://mdpocket.com/index.php?route=account/logout")
        return super().logout(dm)

    def login_with_backup(self, dm, test_user):
        dm.get("https://mdpocket.com/index.php?route=account/login")
        return super().login_with_backup(dm, test_user)

    def login(self, dm, test_user):
        dm.get("https://mdpocket.com/index.php?route=account/login")
        return super().login(dm, test_user)

    def add_address(self, dm , user):
        if not dm.get_route() =="https://mdpocket.com/index.php?route=account/account":
            dm.get("https://mdpocket.com/index.php?route=account/account")
        dm.click_by((By.XPATH,  "//a[contains(text(),'Modify your address book entries')]"))
        dm.click_by((By.XPATH,  "//a[contains(text(),'New Address')]"))
        super().add_address(dm , user)

    def go_basic_product_page(self, dm):
        page = "https://mdpocket.com/Buttons/Ask-me-about-our-Jello-Cups-Pinback-Button"
        self.go_product_page(dm, page)

    def subscribe_to_newsletter(self,dm, user):
        dm.maximize()
        dm.submit_value_by_xpath("//input[@class='email']", user["email"])
        dm.click_by((By.ID,  "groupPopup"))
        dm.click_by((By.XPATH,  "//label/input[1]"))
        assert(dm.value_in_source("You have been subscribed to"))

    def purchase_custom_book(self, dm, product):
        self.go_product_page( dm, product)
        dm.click_by((By.ID, "bookCustomizerChaptersData"))

        while True:
            try:
                dm.click_by((By.XPATH,"//div[@id='sortable2']/div[2]/div[3]/span"), 1)
            except TimeoutException:
                break
        dm.click_by((By.ID, "customizedBookToCart"))
        dm.click_by((By.ID, "button-add"))
        self.add_to_cart(dm)
