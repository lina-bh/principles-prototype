from __future__ import annotations
from customeraccount import CustomerAccount
from specialdeal import SpecialDeal
from subscription import Subscription
from connection import DB


class Deal:
    def __init__(self, id, sub):
        self._id = id
        self._sub = sub

    def __repr__(self):
        return f"<Deal@{hex(id(self))} id={self._id} sub=@{hex(id(self._sub))}>"

    def getID(self):
        return self._id

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
            SELECT subscription_id, subscription.username FROM deal
            JOIN subscription ON subscription_id = subscription.id
            WHERE deal.id = ?
            """,
            [id],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError
        sub_id, acc_id = row
        acc = CustomerAccount.loadByUsername(acc_id)
        sub = Subscription(sub_id, acc)
        return Deal(id, sub)

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
