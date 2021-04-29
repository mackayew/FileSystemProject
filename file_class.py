# File class used to create new File objects and add them to the database

import sqlite3
import sys

db_file = "filemanager.db"
db_con = sqlite3.connect(db_file)
cursor = db_con.cursor()


class File:

    def __init__(self, file_name, parent_id):

        # Sets the File object's properties based on the given name and the current folder

        self.name = file_name
        self.parent = parent_id

        # Inserts a new row into the database with the File's information

        try:
            cursor.execute("INSERT INTO filesystem values(?, ?)", (self.name, str(self.parent)))
            db_con.commit()

        # Handler in the event that sqlite3 throws an Operational Error

        except sqlite3.OperationalError as e:
            print(e, file=sys.stderr)
