from __future__ import annotations
from customeraccount import CustomerAccount
from specialdeal import SpecialDeal
from subscription import Subscription
from connection import DB


class Deal:
    def __init__(self, id, sub, special=None):
        self._id = id
        self._sub = sub
        self._special = special

    def __repr__(self):
        return f"<Deal@{hex(id(self))} id={self._id} sub=@{hex(id(self._sub))}>"

    def getID(self):
        return self._id

    def getPrice(self):
        return 25.00

    def getSpecial(self):
        return self._special

    @staticmethod
    def create(sub: Subscription, special=None) -> Deal:
        cur = DB.cursor()
        cur.execute(
            """
            INSERT INTO
	    deal(subscription_id, special_id)
	    VALUES (?, ?)
	    RETURNING id;
            """,
            [sub.getID(), special.getID() if special else None],
        )
        row = cur.fetchone()
        DB.commit()
        return Deal(row[0], sub)

    @staticmethod
    def loadById(id):
        cur = DB.execute(
            """
            SELECT subscription_id, subscription.username, special_id FROM deal
            JOIN subscription ON subscription_id = subscription.id
            WHERE deal.id = ?
            """,
            [id],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError
        sub_id, acc_id, special_id = row
        acc = CustomerAccount.loadByUsername(acc_id)
        sub = Subscription(sub_id, acc)
        special = None
        try:
            special = SpecialDeal.loadById(special_id)
        except FileNotFoundError:
            pass
        return Deal(id, sub, special)

    @classmethod
    def loadDealsForCustomer(cls, account: CustomerAccount):
        cur = DB.execute(
            """
            SELECT deal.id
            FROM deal
            JOIN subscription ON subscription_id = subscription.id
            WHERE subscription.username = ?
            """,
            [account.getUsername()],
        )
        rows = cur.fetchall()
        deals = []
        for row in rows:
            deals.append(cls.loadById(row[0]))
        return deals

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            deal(
            id INTEGER PRIMARY KEY,
            subscription_id INTEGER NOT NULL,
            special_id INTEGER,
            FOREIGN KEY(subscription_id) REFERENCES subscription(id),
	    FOREIGN KEY(special_id) REFERENCES specialDeal(id)
            );
            """
        )
