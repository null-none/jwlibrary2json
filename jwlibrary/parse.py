import os
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path

from db2json.client import Db2json


class JWlibrary:
    def __init__(self, file):
        self.file = file
        self.dir_path = os.getcwd()

    def parse(self):
        with ZipFile("{}/{}".format(self.dir_path, self.file), "r") as zipped:
            zipped.extractall("{}/tmp".format(self.dir_path))
        if os.path.exists("{}/tmp/user_data.db".format(self.dir_path)):
            db_name = "user_data.db"  # iPhone & iPad backups
        else:
            db_name = "userData.db"  # Windows & Android
        db = Db2json("{}/tmp/{}".format(self.dir_path, db_name))
        db.sqlite_to_json()
