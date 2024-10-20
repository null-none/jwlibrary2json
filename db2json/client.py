import sqlite3
import json
from pathlib import Path
from os import path


class Db2json:
    def __init__(self, path):
        self.path = path

    def open_if_not_exists(self, filename):
        if not path.exists(filename):
            Path(filename).touch()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def open_connection(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        return connection, cursor

    def get_all_records(self, table_name):
        conn, curs = self.open_connection()
        conn.row_factory = self.dict_factory
        curs.execute("SELECT * FROM '{}' ".format(table_name))
        results = curs.fetchall()
        conn.close()
        return json.dumps(results)

    def sqlite_to_json(self):
        connection, cursor = self.open_connection()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            results = self.get_all_records(table_name["name"])
            self.open_if_not_exists("result/{}.json".format(table_name["name"]))
            with open("result/{}.json".format(table_name["name"]), "w") as the_file:
                the_file.write(results)
        connection.close()
