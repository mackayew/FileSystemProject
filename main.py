# Assignment 1 - File Manager
# Ethan Mackay

from functions import *


def main():
    global current_folder

    # Runs on_startup() once every time the program is opened

    on_startup()

    # Will continue to run the program until the user wishes to exit

    while True:
        clear_screen()
        main_menu()
        #print()
        try:

            # After the menu is displayed to the user, they will have the chance to choose what they want to do
            # Depending on the user input, the program will either run a function, or exit

            ans = int(input("  > "))
            if ans == 1:
                clear_screen()
                new_folder()
            elif ans == 2:
                clear_screen()
                new_file()
            elif ans == 3:

                # Checks to make sure that there is at least one other folder before giving the option to change

                if len(folder_names) > 1:
                    clear_screen()
                    current_folder = change_current_folder()
                else:
                    print("No folders to change to.")
            elif ans == 4:
                clear_screen()
                get_folder_contents()
            elif ans == 5:
                clear_screen()
                print_sorted_folders()
            elif ans == 6:

                # Checks to make sure that there is at least one file before giving the option to copy

                if len(file_names) > 0:
                    clear_screen()
                    copy_file()
                else:
                    print("No files to copy.")
            elif ans == 7:

                # Checks to make sure that there is at least one file before giving the option to move

                if len(file_names) > 0:
                    clear_screen()
                    move_file()
                else:
                    print("No files to move.")
            elif ans == 8:
                break
            else:

                # The user must select a valid option on the menu in order to run something

                clear_screen()
                print("Please enter a number on the menu.")

        # Exception that will handle user input that raises an error

        except ValueError as e:
            clear_screen()
            print("Please enter a valid option.")

    # Runs on_closing() once before the program closes

    on_closing()


if __name__ == '__main__':
    main()
