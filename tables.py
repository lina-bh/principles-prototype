from connection import DB
from customeraccount import CustomerAccount
from subscription import Subscription
from warehouse import Warehouse


def create_tables():
    cur = DB.cursor()
    CustomerAccount.create_tables(cur)
    Subscription.create_tables(cur)
    Warehouse.create_tables(cur)
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    deal(
    id INTEGER PRIMARY KEY,
    storage_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    FOREIGN KEY(subscription_id) REFERENCES subscription(id)
    );
    """
    )

    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    storage(
    id INTEGER PRIMARY KEY,
    deal_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    row INTEGER NOT NULL,
    shelf INTEGER NOT NULL,
    FOREIGN KEY(deal_id) REFERENCES deal(id),
    FOREIGN KEY(warehouse_id) REFERENCES warehouse(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    staff(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    staff_account(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    phonenumber INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    FOREIGN KEY(staff_id) REFERENCES staff(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    warehouse_record(
    id INTEGER PRIMARY KEY,
    warehouse_id INTEGER NOT NULL,
    FOREIGN KEY(warehouse_id) REFERENCES warehouse(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    box(
    id INTEGER PRIMARY KEY,
    storage_id INTEGER NOT NULL,
    length INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    FOREIGN KEY(storage_id) REFERENCES storage(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    collection(
    id INTEGER PRIMARY KEY,
    collection_id INTEGER NOT NULL,
    deal_id INTEGER NOT NULL,
    box_id INTEGER NOT NULL,
    FOREIGN KEY(deal_id) REFERENCES deal(id),
    FOREIGN KEY(box_id) REFERENCES box(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    return(
    id INTEGER PRIMARY KEY,
    return_id INTEGER NOT NULL,
    deal_id INTEGER NOT NULL,
    box_id INTEGER NOT NULL,
    FOREIGN KEY(deal_id) REFERENCES deal(id),
    FOREIGN KEY(box_id) REFERENCES box(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    refund(
    id INTEGER PRIMARY KEY,
    refund_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    FOREIGN KEY(refund_id) REFERENCES refund(id),
    FOREIGN KEY(account_id) REFERENCES account(id)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE
    IF NOT EXISTS
    specialDeal(
    id INTEGER PRIMARY KEY,
    discount INTEGER NOT NULL,
    terms TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL
    );
    """
    )
