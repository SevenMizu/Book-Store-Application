from python_program import databaseConnector, loginMember, menuMember, register

# Import necessary modules and functions
import sys

# Define a function to print the menu
def display_menu():
        print('''

**********************************************************************************************
********                                                                              ********
********                        Welcome to the Online Bookstore                       ********
********                                                                              ********
**********************************************************************************************
''') 
        print("Please select an option:")
        print("1. Login for members.")
        print("2. Registration for members.")
        print("q. Exit")


def main():
    connection = databaseConnector()

    if connection:
        while True:
            display_menu()
            choice = input("Input your choice (1, 2, or q): ")

            if choice == "1":
                current_user = loginMember(connection)
                if current_user:
                    menuMember(connection, current_user)
                    input("Are you sure? Press ENTER to confirm.")
            elif choice == "2":
                register(connection)
                input("Press Enter to return to the menu.")
            elif choice == "q":
                break
            else:
                print("Invalid choice. Please enter 1, 2, or q.")

        connection.close()

# Call the main function if this is the main module
if __name__ == "__main__":
    main()

