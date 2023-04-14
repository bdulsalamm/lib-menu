from Lib_db_conn import DB_CONN
from lib_menu import LibMenu


Library_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS books(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(128) NOT NULL,
  author VARCHAR(128) NOT NULL,
  date VARCHAR(12) NOT NULL);
"""


class Main():
    def __init__(self) -> None:
        self.initDatabase()
        library = LibMenu()

        library.start()
        
        DB_CONN.close()

        return None

    def initDatabase(self1):
        cursor = DB_CONN.cursor()
        cursor.execute(Library_TABLE_STATEMENT)
        DB_CONN.commit()
        cursor.close()
        return None


if __name__ == "__main__":
    app = Main()

