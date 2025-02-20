# Importing packages I need for the program to run

from folder_class import Folder
from file_class import File
import sys, os, sqlite3

# Variables that need to be declared outside of the functions so that they can be modified by all
# Both folder_pic and file_pic will only display their unicode symbols in the PyCharm Run window, otherwise appear as ?

folder_pic = "\U0001f5c0"
file_pic = "\U0001f5c5"
id_counter = 1
current_folder = 0
folder_names = list()
file_names = list()
save_file_fo = "folder_info.csv"
save_file_fi = "file_info.csv"

# Building a connection to the database

db_file = "filemanager.db"
db_con = sqlite3.connect(db_file)
cursor = db_con.cursor()


# Function that will run upon starting up the program to read info from save files and create tables if necessary

def on_startup():
    global file_names, folder_names, id_counter

    # Opens the file containing all used folder names and writes them to a list to be used

    try:
        with open(save_file_fo, 'r') as file:
            for row in file:
                row = row.strip('\n')
                folder_names.append(row)

    # Catches an error in the event that the file doesn't exist (Either deleted or hasn't been created yet)

    except FileNotFoundError as e:
        print(e, file=sys.stderr)

    # Does the same thing as the above block except with filenames

    try:
        with open(save_file_fi, 'r') as file1:
            for row1 in file1:
                row1 = row1.strip('\n')
                file_names.append(row1)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)

    # Creates the SQL table that will hold the info for all folders if it doesn't already exist

    create_folder_table = """CREATE TABLE IF NOT EXISTS folder_system (
                        folder_ID INT,
                        folder_name VARCHAR(50),
                        parent_ID INT
                        );"""

    # Creates the SQL table that wil hold the info for all files if it doesn't already exist

    create_file_table = """CREATE TABLE IF NOT EXISTS filesystem (
                            file_name VARCHAR(50),
                            folder_ID INT
                            );"""

    # Runs the folder table creation code, handling any errors thrown by sqlite3

    try:
        cursor.execute(create_folder_table)
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)
    except sqlite3.DatabaseError as e:
        print(e, file=sys.stderr)

    # Runs the file table creation code, handling any errors thrown by sqlite3

    try:
        cursor.execute(create_file_table)
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)
    except sqlite3.DatabaseError as e:
        print(e, file=sys.stderr)

    db_con.commit()

    # If this is the first time the user runs the program, it will create a 'root' folder by default
    # Also sets the id counter to the appropriate value to keep track of how many folders have been created

    if len(folder_names) == 0:
        Folder("root", 0, None)
        folder_names.append("root")
        id_counter = 1
    else:
        id_counter = len(folder_names)


# This will run once before the program closes, used to write information to files to be read in on_startup()

def on_closing():

    # Writes all folder names to the save file

    try:
        with open(save_file_fo, 'w') as file:
            for item in folder_names:
                file.write(item + '\n')

    # Handles errors thrown by either the file not being found, or a value error when writing to the file

    except FileNotFoundError as e:
        print(e, file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)

    # Completes the same task as the above block but with filenames instead of folders

    try:
        with open(save_file_fi, 'w') as file1:
            for item1 in file_names:
                file1.write(item1 + '\n')
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)

    # Terminates the connection to the database before closing the program

    db_con.close()


# This will print out the menu to be displayed each time the program is finished with a task

def main_menu():
    print("""        -------------------------------------------------
        *              File Manager Program             *
        -------------------------------------------------
        *             1 - Create New Folder             *
        *             2 - Create New File               *
        *             3 - Change Current Folder         *
        *             4 - View Current Folder           *
        *             5 - View Folders Sorted           *
        *             6 - Copy File                     *
        *             7 - Move File                     *
        *             8 - Exit Program                  *
        -------------------------------------------------""")

    # Gives the user the name of the folder they're currently in

    try:
        cursor.execute("SELECT * FROM folder_system WHERE folder_ID = ?", [current_folder])

    # Handles an operational error that could be thrown by sqlite3

    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    row = cursor.fetchmany(1)
    for item in row:
        print("        current folder:", item[1])


# This function was created to clear the output screen every time the user selects an option or returns to the main menu

def clear_screen():
    os.system('cls')


# Function to create a new folder given a filename specified by the user.

def new_folder():

    global id_counter

    while True:

        # Gets a name from the user, checks to see if it is both valid and not in use

        try:
            name = str(input("Please enter a name for your new folder: "))
            if name in folder_names:
                print("That name is already in use.")
            else:
                if verify_folder_name(name):

                    # If the name passes both tests, it is added to the list of names

                    folder_names.append(name)
                    break
                else:
                    print(r"Please use only valid characters. (. /\ :; ' * [] , | <> = not allowed.)")

        # This will handle an error in the event that the user inputs an incorrect value

        except ValueError as e:
            print(e, file=sys.stderr)
            print("Please enter a valid name.")

    # Updates the counters appropriately, and creates a Folder object with the entered values

    folder_id = id_counter

    id_counter += 1

    parent_id = current_folder

    Folder(name, folder_id, parent_id)


# This function will create a copy of the file entered by the user

def copy_file():
    while True:

        # Gets input from the user for the name of the file to be copied

        try:
            name = str(input("Please enter the name of the file you wish to copy: "))

            # If the file exists, this will run through the names to see how many copies already exist

            if name in file_names:
                copy_count = 1
                while True:
                    if (name + "(" + str(copy_count) + ")") in file_names:
                        copy_count += 1
                    else:

                        # Copies are created by adding an (x) to the end of the filename
                        # Where x = number of copies + 1
                        # Once x is reached, the number is added to the end of the filename and breaks out

                        name_copy = name + ("(" + str(copy_count) + ")")
                        break
                break
            else:
                print("This file doesn't exist.")

        # Handles an error in the event that the user enters an incorrect value

        except ValueError as e:
            print("Please enter a valid name.")
            print(e, file=sys.stderr)

    # Retrieves the existing file's information from the database

    try:
        cursor.execute("SELECT * FROM filesystem WHERE file_name = ?", [name])
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Fetches the entire row, and takes the file's parent ID to be used in creating the copy

    row = cursor.fetchall()
    for item in row:
        parent_id = item[1]
        break

    # Creates a File object using the copied name and parent folder's ID

    File(name_copy, parent_id)
    file_names.append(name_copy)


# This function changes the folder that a file is currently located in

def move_file():
    while True:
        try:

            # Gets a filename from the user

            name = str(input("Please enter the name of the file you wish to move: "))
            if name in file_names:

                # Gets a folder name from the user if the entered file exists

                new_parent = str(input("Please enter the name of the folder you wish to move it to: "))
                if new_parent in folder_names:
                    break
                else:
                    print("Folder doesn't exist.")
            else:
                print("File doesn't exist.")

        # Handles an error in the event that the user enters an incorrect value

        except ValueError as e:
            print("Please enter a valid name.")
            print(e, file=sys.stderr)

    # Gets the folder from the database

    try:
        cursor.execute("SELECT * FROM folder_system WHERE folder_name = ?", [new_parent])

    # Handles an error in the event that sqlite3 throws an Operational Error

    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Takes the folder's ID to be used to change the file's folder ID to

    row = cursor.fetchall()
    for item in row:
        parent_id = int(item[0])
        break

    # Updates the file's folder ID to the folder entered by the user

    try:
        cursor.execute("UPDATE filesystem SET folder_ID = ? WHERE file_name = ?", (parent_id, name))
        db_con.commit()
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)


# This function will create a new file in the current folder

def new_file():
    while True:
        try:

            # Gets a filename from the user and checks to see that it's valid

            name = str(input("Please enter a name for your new file 'filename.extension': "))
            if name in file_names:
                print("That name is already in use.")
            else:
                if verify_file_name(name):

                    # If the name passes verifications, it is added to the list of used filenames

                    file_names.append(name)
                    break
                else:
                    print('Please use only valid characters. (\, /, :, ;, *, <, >, =, , not allowed. Only one ".")')

        # Handles an error in the event that the user enters an incorrect value

        except ValueError as e:
            print(e, file=sys.stderr)

    # Sets the parent ID to the ID of the current folder and creates a File object with entered info

    parent_id = current_folder

    File(name, parent_id)


# This function will output the contents of the current folder

def get_folder_contents():

    # Gets the name of the current folder from the database

    try:
        cursor.execute("SELECT * FROM folder_system WHERE folder_ID = ?", [current_folder])

    # Handler in the event that sqlite3 throws an Operational Error

    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Prints the current folder name

    row = cursor.fetchmany(1)
    for item in row:
        print(item[1])

    # Gets all folders from the database whose parent folder is the current one

    try:
        cursor.execute("SELECT * FROM folder_system WHERE parent_ID = ?", [current_folder])
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Prints the folders retrieved from the database

    row = cursor.fetchall()
    for item1 in row:
        print("|")
        print("|")
        print(folder_pic, item1[1])

    # Gets all files from the database whose parent folder is the current one

    try:
        cursor.execute("SELECT * FROM filesystem WHERE folder_ID = ?", [current_folder])
    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Prints the files retrieved from the database

    row = cursor.fetchall()
    for item2 in row:
        print("|")
        print("|")
        print(file_pic, item2[0])

    wait = input("")


# This function allows the user to enter into a different folder

def change_current_folder():
    global current_folder

    while True:
        try:

            # Gets a folder name from the user and checks to see if it exists

            folder_name_user = str(input("Please enter the name of the folder you wish to open: "))
            if folder_name_user in folder_names:
                break
            else:
                print("Please enter an existing folder name.")

        # Handles an error in the event that the user enters an incorrect value

        except ValueError as e:
            print("Please enter a valid folder name.")

    # Fetches the desired folder's information from the database

    try:
        cursor.execute("SELECT * FROM folder_system WHERE folder_name = ?", [folder_name_user])

    # Handler in the event that sqlite3 throws an Operational Error

    except sqlite3.OperationalError as e:
        print(e, file=sys.stderr)

    # Sets the current folder to the desired folder's ID and returns the value

    row = cursor.fetchone()
    current_folder = int(row[0])
    return current_folder


# This function sorts all created folders alphabetically and outputs them to the user

def print_sorted_folders():

    # Sorts the folder names

    current_folders_sorted = sorted(folder_names)
    counter = 1

    # Outputs them to the user in a numbered list

    for folder in current_folders_sorted:
        print(counter, "---", folder)
        counter += 1
    wait = input("")


# This function is used to check entered filenames for illegal characters

def verify_file_name(filename):

    if filename.count('.') != 1:
        return False

    illegals = {'/', '\\', ':', ';', "'", '"', '*', ' ', '=', '<', '>'}
        
    for i in illegals:
        if i in filename:
            return False
            
    return True


# This function is used to check entered folder names for illegal characters

def verify_folder_name(foldername):

    illegals = {'/', '\\', ':', ';', "'", '"', '*', '=', '<', '>', '[', ']', ',', '|'}

    for i in illegals:
        if i in foldername:
            return False
    return True
