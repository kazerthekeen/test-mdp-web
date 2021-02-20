from my_driver import driver_manager
from web_tests import load_settings
from mdpocket_web import mdpocket_web
import fileinput
import csv

"""
Note inner workings of these scripts are liable to be changed based on situation
They may have been developed elsewhere and moved here for record keeping purposes
As such these scripts often do not follow best practices.

This can be used to make a bunch of accounts for a vendor, reads in from a file
named users.dat that has been formated to lastname, firstname, email.

"""


def Make_Accounts():
    config = load_settings("auto_account.json")
    users = parse_users(config["load_file"], config["protoype"])
    site = mdpocket_web()
    for user in users:
        print(user)
        try:
            dm = driver_manager(config)
            site.make_account(dm, user)
            assert dm.value_in_source("Your Account Has Been Created!")
            dm.quit()
            print("User success")
        except:
            print("User failed")


def parse_users(file_name, protoype):
    users = []
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            user = {}
            user["firstname"] = line[1]
            user["lastname"] = line[2]
            user["email"] = line[3]
            user.update(protoype)
            users.append(user)
    return users


if __name__ == "__main__":
    Make_Accounts()
