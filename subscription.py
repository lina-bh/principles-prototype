from __future__ import annotations
from connection import DB
from customeraccount import CustomerAccount


class Subscription:
    def __init__(self, id, account):
        self.id = id
        self.account = account

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
    CREATE TABLE
    IF NOT EXISTS
    subscription(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES account(username)
    );
    """
        )

    @staticmethod
    def create(account: CustomerAccount):
        cur = DB.cursor()
        cur.execute(
            "INSERT INTO subscription(username) VALUES (?) RETURNING id",
            [account.username],
        )
        row = cur.fetchone()
        DB.commit()
        return Subscription(row[0], account)

    @staticmethod
    def loadById(id: int) -> Subscription:
        cur = DB.cursor()
        cur.execute(
            """
            SELECT subscription.id, account.id 
            FROM subscription
            JOIN account ON account.username = subscription.username
            WHERE subscription.id = ?", [id]
            """,
            [id],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError
        return Subscription(row[0], CustomerAccount.loadById(row[1]))
