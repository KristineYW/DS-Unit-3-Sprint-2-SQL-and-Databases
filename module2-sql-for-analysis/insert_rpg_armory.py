import os
from dotenv import load_dotenv
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

load_dotenv() # looks inside the .env file for some env vars

# passes env var values to python var
DB_HOST = os.getenv("DB_HOST", default="OOPS")
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

# what is the filepath to connect to our sqlite database?
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module1-introduction-to-sql", "rpg_db.sqlite3") 

class SqliteService_armory():
    def __init__(self, db_filepath=DB_FILEPATH):
        self.connection = sqlite3.connect(db_filepath)
        self.cursor = self.connection.cursor()
    def fetch_armory(self): #fix
        return self.cursor.execute("SELECT * FROM armory_item;").fetchall() #fix

class ElephantSQLService_armory():
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        self.cursor = self.connection.cursor()

    def create_armory_table(self): #fix
        create_query = """
        DROP TABLE IF EXISTS armory; -- allows this to be run idempotently, avoids psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "armory_pkey" DETAIL:  Key (armory_id)=(1) already exists.
        CREATE TABLE IF NOT EXISTS armory (
            item_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            value INT,
            weight INT
        );
        """
        print(create_query)
        self.cursor.execute(create_query)
        self.connection.commit()

    def insert_armory(self, armory):
        """
        Param armory needs to be a list of tuples, each representing a row to insert (each should have each column)
        """
        insertion_query = """
            INSERT INTO armory (item_id, name, value, weight)
            VALUES %s
        """
        execute_values(self.cursor, insertion_query, armory)
        self.connection.commit()
if __name__ == "__main__":
    #
    # EXTRACT (AND MAYBE TRANSFORM IF NECESSARY)
    #
    sqlite_service = SqliteService_armory()
    armory = sqlite_service.fetch_armory()
    print(type(armory), len(armory))
    print(type(armory[0]), armory[0])
    #
    # LOAD
    #
    pg_service = ElephantSQLService_armory()
    pg_service.create_armory_table()
    pg_service.insert_armory(armory)