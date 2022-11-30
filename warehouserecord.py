from __future__ import annotations
from collection import Collection
from connection import DB
from movement import Movement
from returnclass import Return
from staff import StaffMember

from warehouse import Warehouse


class WarehouseRecord:
    def __init__(
        self, id: int, warehouse: Warehouse, staff: StaffMember, operation: Movement
    ):
        self._id = id
        self._warehouse = warehouse
        self._staff = staff
        if isinstance(operation, Collection):
            self._coll = operation
        elif isinstance(operation, Return):
            self._return = operation
        else:
            raise TypeError

    def getID(self):
        return self._id

    @classmethod
    def create(cls, warehouse: Warehouse, staff: StaffMember, operation: Movement):
        if isinstance(operation, Collection):
            ret = operation
            id = DB.execute(
                """
                INSERT INTO
                warehouse_record(warehouse_id, staff_id, collection_id)
                VALUES (?, ?, ?)
                RETURNING id
                """,
                [warehouse.getID(), staff.getID(), ret.getID()],
            ).fetchone()[0]
            return cls(id, warehouse, staff, ret)
        elif isinstance(operation, Return):  # if isinstance(operation, Return):
            ret = operation
            id = DB.execute(
                """
                INSERT INTO
                warehouse_record(warehouse_id, staff_id, return_id)
                VALUES (?, ?, ?)
                RETURNING id
                """,
                [warehouse.getID(), staff.getID(), ret.getID()],
            ).fetchone()[0]
            return cls(id, warehouse, staff, ret)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            warehouse_record(
            id INTEGER PRIMARY KEY,
            warehouse_id INTEGER NOT NULL,
            staff_id INTEGER NOT NULL,
            collection_id INTEGER,
            return_id INTEGER,
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(id),
            FOREIGN KEY(collection_id) REFERENCES collection(id),
            FOREIGN KEY(return_id) REFERENCES return(id),
            FOREIGN KEY(staff_id) REFERENCES staff_account(id)
            );
            """
        )
