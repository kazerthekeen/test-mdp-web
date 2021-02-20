from my_driver import driver_manager
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class website():
    input_keys = {
        "default":{
            "firstname": "input-firstname",
            "lastname": "input-lastname",
            "email": "input-email",
            "telephone": "input-telephone",
            "address-1": "input-address-1",
            "postcode" : "input-postcode",
            "address-2": "input-address-2",
            "company": "input-company",
            "country": "input-country",
            "city": "input-city",
            "zone": "input-zone"
        },

        "payment" : {
            "firstname": "input-payment-firstname",
            "lastname": "input-payment-lastname",
            "email": "input-payment-email",
            "telephone": "input-payment-telephone",
            "address-1": "input-payment-address-1",
            "postcode" : "input-payment-postcode",
            "address-2": "input-payment-address-2",
            "company": "input-payment-company",
            "country": "input-payment-country",
            "city": "input-payment-city",
            "zone": "input-payment-zone"
        }
    }

    welcome_text ="Welcome to  "

    def change_password(self, dm, user, password_key):
        dm.click_by((By.XPATH, "//a[contains(text(),'Change your password')]"))
        dm.submit_value_by_id("input-password", user[password_key])
        dm.submit_value_by_id("input-confirm", user[password_key])
        dm.click_by((By.XPATH, "//input[@value='Continue']"))
        assert dm.value_in_source("Success: Your password has been successfully updated.")

    def make_account(self, dm, user):
        self.__input_personal_details(dm, user)
        self.__input_address(dm, user)
        dm.submit_value_by_id("input-password", user["password"])
        dm.submit_value_by_id("input-confirm", user["confirm"])
        dm.scroll_bottom()
        dm.click_by((By.NAME, "agree"))
        dm.click_by((By.XPATH, "//input[@value='Continue']"))

    def add_address(self, dm , user):
        dm.submit_value_by_id("input-firstname", user["firstname"])
        dm.submit_value_by_id("input-lastname", user["lastname"])
        self.__input_address(dm , user)
        dm.click_by((By.XPATH, "//input[@value='Continue']"))

    def __input_personal_details(self, dm , user, input_type="default"):
        key = self.input_keys[input_type]
        dm.submit_value_by_id(key["firstname"], user["firstname"])
        dm.submit_value_by_id(key["lastname"], user["lastname"])
        dm.submit_value_by_id(key["email"], user["email"])
        dm.submit_value_by_id(key["telephone"],user["telephone"] )

    def __input_address(self, dm , user,input_type="default"):
        key = self.input_keys[input_type]
        dm.submit_value_by_id(key["address-1"], user["address-1"])
        dm.submit_value_by_id(key["postcode"], user["postcode"])
        dm.submit_value_by_id(key["city"], user["city"])
        dm.select_value_by_id(key["zone"], user["zone"])

    def logout(self, dm):
        result =  dm.value_in_source("You have been logged off your account.")
        print("Account logout : ", result)
        return result

    def login_with_backup(self, dm, user):
        if dm.value_in_source("SECURE LOGIN"):
            dm.submit_value_by_id("input-email", user["email"])
            pw = "password_2"
            dm.submit_value_by_id("input-password", user["password_1"])
            dm.click_by((By.XPATH, "//input[@value='Login']"))
            if dm.value_in_source(self.welcome_text):
                return pw
            else:
                dm.sleep(4)
                dm.submit_value_by_id("input-email", user["email"])
                pw = "password_1"
                dm.submit_value_by_id("input-password", user["password_2"])
                dm.click_by((By.XPATH, "//input[@value='Login']"))
                assert(self.welcome_text)
                return pw
        else:
            return False

    def select_required_options(self, dm):
        dm.click_by((By.ID, "select-options"))
        dm.select_all_required("//div[contains(@class, 'form-group') and contains(@class, 'required')]/div/div[2]/div/select")
        dm.click_by((By.ID, "button-add"))

    def login(self, dm, user):
        if dm.value_in_source("SECURE LOGIN"):
            dm.submit_value_by_id("input-email", user["email"])
            dm.submit_value_by_id("input-password", user["password"])
            dm.click_by((By.XPATH, "//input[@value='Login']"))
            result =  dm.value_in_source(self.welcome_text)
            return result

    def add_to_cart(self, dm, repeat=True):
        dm.click_by((By.ID, "button-cart"))
        try:
            dm.click_by((By.XPATH, "//input[@value='Continue Shopping']"), 1)
        except TimeoutException:
            self.select_required_options(dm)
            self.add_to_cart(dm, False)

    def checkout(self, dm, user, login):
        """
        This preforms the checkout process it fails if any part takes longer than 30 secs to load.
        """
        if login:
            try:
                dm.sleep(2)
                dm.confirm_alert(dm.click_by, (By.XPATH,"//div[@id='shipping-existing']/select/option[1]"))
                dm.click_by((By.ID, "button-payment-continue"))
                dm.wait(15, EC.element_to_be_clickable((By.NAME,"payment_method")))
            except UnexpectedAlertPresentException:
                return website.checkout(self, dm, user, login)
        else:
            dm.click_by((By.XPATH, "//input[@value='guest']"))
            dm.click_by((By.XPATH, "//a[contains(text(),'Guest Checkout')]"))
            self.__input_address(dm, user, "payment")
            self.__input_personal_details(dm, user, "payment")
            dm.click_by((By.ID, "button-guest"))
        dm.wait(10, EC.element_to_be_clickable((By.NAME,"payment_method")))
        dm.confirm_alert(dm.submit_value_by_id, "input-discountCode" , user["coupon"])
        dm.click_by((By.XPATH, "//span[@class='input-group-btn']"))
        dm.wait(10, EC.visibility_of_element_located((By.XPATH,"//div[@class='success']")))
        dm.click_by((By.ID, "billing-shipping-method"), 20)
        dm.click_by((By.ID, "button-go-green-popup"), 20)
        dm.click_by((By.ID, "button-confirm"), 20)
        try:
            dm.wait(30, EC.visibility_of_element_located((By.XPATH, "//div[@class='success-detail']")))
            return True
        except TimeoutException:
            return False

    def go_product_page(self, dm, product):
        dm.get(product)
