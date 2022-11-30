from box import Box
from collection import Collection
from customeraccount import CustomerAccount
from refund import Refund
from returnclass import Return
from specialdeal import SpecialDeal
from staff import StaffMember
from storage import Storage
from subscription import Subscription
from warehouse import Warehouse
from deal import Deal
from warehouserecord import WarehouseRecord


def create_tables(db):
    cur = db.cursor()
    CustomerAccount.create_tables(cur)
    Subscription.create_tables(cur)
    Warehouse.create_tables(cur)
    Deal.create_tables(cur)
    Storage.create_tables(cur)
    Box.create_tables(cur)
    Collection.create_tables(cur)
    WarehouseRecord.create_tables(cur)
    StaffMember.create_tables(cur)
    Return.create_tables(cur)
    SpecialDeal.create_tables(cur)
    Refund.create_tables(cur)
