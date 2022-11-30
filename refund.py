from __future__ import annotations
from connection import DB
from customeraccount import CustomerAccount
from returnclass import Return
from collection import Collection

from movement import Movement


class Refund:
    def __init__(self, id: int, account: CustomerAccount, operation: Movement):
        self._id = id
        self._acc = account
        self._op = operation

    def __repr__(self):
        return (
            f"<Refund@{hex(id(self))} id={self._id} account={hex(id(self._acc))} "
            f"op=@{hex(id(self._op))}>"
        )

    @classmethod
    def create(cls, account: CustomerAccount, operation: Movement):
        if not isinstance(operation, Movement):
            raise TypeError
        cur = DB.execute(
            """
            INSERT INTO
	     refund(account_id, return_id, collection_id)
	     VALUES (?, ?, ?)
	     RETURNING id
	     """,
            [
                account.getAccountNumber(),
                operation.getID() if isinstance(operation, Return) else None,
                operation.getID() if isinstance(operation, Collection) else None,
            ],
        )
        id = cur.fetchone()[0]
        DB.commit()
        return cls(id, account, operation)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            refund(
            id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            return_id INTEGER,
            collection_id INTEGER,
            FOREIGN KEY(return_id) REFERENCES return(id),
            FOREIGN KEY(collection_id) REFERENCES collection(id),
            FOREIGN KEY(account_id) REFERENCES account(id)
            );
            """
        )
