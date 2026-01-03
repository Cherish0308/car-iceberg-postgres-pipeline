from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import create_engine, text

from config import POSTGRES_URL
from interfaces import Writer


class PostgresWriter(Writer):

    def __init__(self, engine=None):
        self._engine = engine or create_engine(POSTGRES_URL)

    def upsert(self, table: str, records: Sequence[dict[str, any]]) -> None:
        records = list(records)
        if not records:
            return

        cols = records[0].keys()
        col_list = ",".join(cols)
        val_list = ",".join([f":{c}" for c in cols])
        update_list = ",".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "car_id"])

        sql = f"""
        INSERT INTO {table} ({col_list})
        VALUES ({val_list})
        ON CONFLICT (car_id)
        DO UPDATE SET {update_list}
        """

        with self._engine.begin() as conn:
            conn.execute(text(sql), records)