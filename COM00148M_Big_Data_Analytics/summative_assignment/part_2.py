import sqlite3
from typing import Final
from typing import Optional

# I was going to write my own contextmanager for sqlite, but turns out
# that this is the archetypical example.
# source: https://oneuptime.com/blog/post/2026-01-30-python-custom-context-managers/view
class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Handle transaction based on whether an exception occurred
        if exc_type is not None:
            self.connection.rollback()
            print(f"Transaction rolled back due to: {exc_val}")
        else:
            self.connection.commit()

        self.cursor.close()
        self.connection.close()
        return False


def main() -> None:
    # Step 1: create the database and tables
    create_table_cmds: Final[list[str]] = [
    ]

    with DatabaseConnection("db.db") as cur:
        for cmd in create_table_cmds:
            cur.execute(cmd)

    # Step 2: insert data from csv file

    # Step 3: extract all casualties who
    # - suffered serious or fatal injuries
    # - were involved in pedestrian-related incidents
    # - occured under a specific condition
        # NOTE: I think the last one is up to us to decide

    # Step 4: Perform descriptive analysis of casualty severity by casualty type
    # (aggregation query)


if __name__ == "__main__":
    raise SystemExit(main())
