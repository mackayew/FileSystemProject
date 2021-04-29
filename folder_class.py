# Folder class used to create new Folder objects and add them to the database

import sqlite3
import sys

db_file = "filemanager.db"
db_con = sqlite3.connect(db_file)
cursor = db_con.cursor()


class Folder:

    def __init__(self, folder_name, folder_id, parent_id):

        # Sets object's values appropriately based on user input, current folder, and folder count

        self.name = folder_name
        self.id = folder_id
        self.parent = parent_id

        # Inserts a new row into the database with the Folder's information

        try:
            cursor.execute("INSERT INTO folder_system values(?, ?, ?)", (str(self.id), self.name, str(self.parent)))
            db_con.commit()

        # Handler in the event that sqlite3 throws an Operational Error

        except sqlite3.OperationalError as e:
            print(e, file=sys.stderr)

        print("Created.")
