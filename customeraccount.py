from __future__ import annotations
from crypt import crypt

from address import Address
from connection import DB
from visacheckaccount import VISACheckAccount


class CustomerAccount:
    def __init__(
        self,
        cusAccNum: int,
        username: str,
        name: str,
        email: str,
        address: Address,
        visacheck,
    ):
        # Python has no visibility specifiers
        self.cusAccNum = cusAccNum
        self.username = username
        self.name = name
        self.address = address
        self.email = email
        self.visacheck = visacheck
        self.password = None

    def __repr__(self):
        return f"<CustomerAccount cusAccNum={self.cusAccNum} username={self.username} name={self.name} address={self.address} email={self.email} self.visacheck? {bool(self.visacheck)}>"

    def setName(self, name):
        self.name = name

    def setAddress(self, address):
        self.address = address

    def setEmail(self, email):
        self.email = email

    def setPassword(self, password):
        self.password = crypt(password)

    def store(self):
        cur = DB.cursor()
        cur.execute(
            """
            UPDATE account SET
            address = ?,
            email = ?,
            password = ?
            WHERE id = ?
            """,
            [self.address.to_str(), self.email, self.password, self.cusAccNum],
        )
        DB.commit()

    @staticmethod
    def create(username: str, name: str, email: str, address: Address):
        cur = DB.cursor()
        cur.execute(
            "INSERT INTO account(username, email, address) VALUES (?, ?, ?);",
            [
                username,
                email,
                address.to_str(),
            ],
        )
        cur.execute(
            "INSERT INTO customer(name, username) VALUES (?, ?);",
            [
                name,
                username,
            ],
        )
        DB.commit()
        return CustomerAccount.loadByUsername(username)

    @staticmethod
    def loadById(id: int) -> CustomerAccount:
        cur = DB.cursor()
        cur.execute(
            """
            SELECT id, account.username, name, email, address, cardDetails
            FROM account
            INNER JOIN customer
            ON customer.username = account.username
            WHERE id = ?
            """,
            [id],
        )
        row = cur.fetchone()
        print(row)
        return CustomerAccount(
            row[0],
            row[1],
            row[2],
            row[3],
            Address.from_str(row[4]),
            VISACheckAccount(row[5]),
        )

    @staticmethod
    def loadByUsername(username: str):
        cur = DB.cursor()
        cur.execute(
            "SELECT id FROM account WHERE username = ?;",
            [username],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError  # stand-in for a custom exception type
        return CustomerAccount.loadById(row[0])

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            account(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            cardDetails TEXT
            );
            """
        )
        cur.execute(
            """
        CREATE TABLE
        IF NOT EXISTS
        customer(
        name TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        FOREIGN KEY(username) REFERENCES account(username)
        );
        """
        )
