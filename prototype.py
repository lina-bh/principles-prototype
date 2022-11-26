# allow returning self type in static method
from __future__ import annotations
from pprint import pprint
from getpass import getpass

from connection import DB
from tables import create_tables
from customeraccount import CustomerAccount
from address import Address
from subscription import Subscription
from warehouse import create_stockwell_warehouse


def get_tables():
    cur = DB.cursor()
    cur.execute("SELECT * FROM sqlite_master")
    pprint([row[4] for row in cur.fetchall() if row[0] == "table"])


def read_address_interactively() -> Address:
    print("address please")
    first_line = input("first line: ")
    second_line = input("second line: ")
    town = input("town: ")
    county = input("county: ")
    postcode = input("postcode: ")
    return Address(first_line, second_line, town, county, postcode)


def create_account_interactively():
    print("creating account")
    username = input("username: ")
    name = input("your name: ")
    email = input("email: ")
    address = read_address_interactively()
    password = getpass("password: ")
    account = CustomerAccount.create(username, name, email, address)
    account.setPassword(password)
    account.store()
    return account


create_tables()
if input("use default account details? [y] ").startswith("n"):
    account = create_account_interactively()
else:
    account = CustomerAccount.create(
        "linabee",
        "Lina",
        "36717206+lina-bh@users.noreply.github.com",
        Address("30 Park Row", "", "London", "", "SE10 9LS"),
    )
    account.setPassword("hunter2")
    account.store()
print(repr(account), "created")
stockwell_warehouse = create_stockwell_warehouse()
print(stockwell_warehouse, "was created")
sub = Subscription.create(account)
print(sub, "created")
