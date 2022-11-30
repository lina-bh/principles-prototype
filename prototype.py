# allow returning self type in static method
from __future__ import annotations
from pprint import pprint
from getpass import getpass
from box import Box
from collection import Collection

from connection import DB
from deal import Deal
from returnclass import Return
from specialdeal import SpecialDeal
from staff import StaffMember, create_mike, create_lydia
from customeraccount import CustomerAccount
from address import Address
from subscription import Subscription
from tables import create_tables
from warehouse import create_stockwell_warehouse
from storage import Storage
from silly import *
from warehouserecord import WarehouseRecord


def get_tables():
    cur = DB.cursor()
    cur.execute("SELECT * FROM sqlite_master")
    [print(row[4]) for row in cur.fetchall() if row[0] == "table"]


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


def create_box_interactively(account):
    length = int(input("length in cm: "))
    width = int(input("width in cm: "))
    height = int(input("height in cm: "))
    return Box.create(account, length, width, height)


create_tables(DB)
create_mike()
create_lydia()

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
deal = Deal.create(sub)
print(deal, "created")

if input("use selected box details [y] ").startswith("n"):
    box = create_box_interactively(account)
else:
    box = Box.create(account, 44, 35, 16)

print(box, "created")
storage = Storage.create(deal, stockwell_warehouse, box, (1, 1))
print(storage, "created")
coll = Collection.create(deal, box, storage)
print(coll, "created")
mike = StaffMember.loadByUsername("mike")
coll_record = WarehouseRecord.create(stockwell_warehouse, mike, coll)
print(
    "box",
    box.getID(),
    "-- collected",
    coll.getID(),
    "--> storage",
    storage.getID(),
    "at warehouse",
    stockwell_warehouse.getID(),
    " ",
    stockwell_warehouse.getAddress().firstLine,
    "by staff no",
    mike.getID(),
    mike.getName(),
)

lydia = StaffMember.loadByUsername("lydia")

ret_deal = Deal.create(sub)
ret = Return.create(deal, box, storage)
print(ret_deal, "created for", ret)
ret_record = WarehouseRecord.create(stockwell_warehouse, mike, ret)
print(
    "box",
    box.getID(),
    "-- returned",
    ret.getID(),
    "--> customer",
    sub.getCustomer().getAccountNumber(),
    "by staff no",
    lydia.getID(),
    lydia.getName(),
)

special = SpecialDeal.create(25, "Valid once for collections")
print("😍 special deal created")
print(
    special.getDiscount(),
    "% off with code",
    special.getCode(),
    "!!",
    special.getTerms(),
)
special_dealed = Deal.create(sub, special)
special_box = Box.create(account, 44, 35, 16)
special_coll = Collection.create(special_deal, special_box, storage)
print("oops, cancelled")
