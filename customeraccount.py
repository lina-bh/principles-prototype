from __future__ import annotations
from crypt import crypt
from copy import copy

from address import Address
from connection import DB
from visacheckaccount import VISACheckAccount


class CustomerAccount:
    def __init__(
        self,
        accNum: int,
        username: str,
        name: str,
        email: str,
        address: Address,
        visacheck,
    ):
        # Python has no visibility specifiers
        self._id = accNum
        self._username = username
        self._name = name
        self._address = address
        self._email = email
        self._visacheck = visacheck
        self._password = None

    def __repr__(self):
        return f"<CustomerAccount@{hex(id(self))} id={self._id} username={self._username} name={self._name} address={self._address} email={self._email} self.visacheck={self._visacheck}>"

    def getAccountNumber(self):
        return self._id

    def getUsername(self):
        return self._username

    def getName(self):
        return self._name

    def getAddress(self):
        return copy(self._address)

    def getEmail(self):
        return self._email

    def setName(self, name):
        self._name = name

    def setAddress(self, address):
        self._address = address

    def setEmail(self, email):
        self._email = email

    def setPassword(self, password):
        self._password = crypt(password)

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
            [self._address.to_str(), self._email, self._password, self._id],
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
        # print(row)
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
