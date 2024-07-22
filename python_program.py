from getpass import getpass
from mysql.connector import connect, Error
import re
import datetime



# Checks if an email is valid 
def emailCheck(email):
    
    pattern = r'^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    return re.match(pattern, email) is not None


# Logs the member in and takes the connection as an argument
def loginMember(connection):
    print("Member Login")
    email = input("Please enter your email address: ")
    if emailCheck(email):
        password = getpass("Please enter your password: ")

        try:
            with connection.cursor() as cursor:
                # Execute the SELECT query to find the member with the given user ID and password
                select_query = "SELECT * FROM Members WHERE email = %s AND password = %s"
                select_values = (email, password)
                cursor.execute(select_query, select_values)

                # Get the results of the query
                result = cursor.fetchone()

                if result:
                    print("Login successful.")
                    print(f"Welcome, {result[2]} {result[3]}!")
                    # Returns the user ID to be used as a parameter in functions while logged in
                    user_id = result[0]
                    return user_id
                else:
                    print("\n")
                    print("Invalid email or password. Please try again or register as a new member.")
                    print("\n")

        except Error as e:
            print("Error executing login query:", e)
    else:
        print("\n")
        print("Invalid email format. Please try again or register as a new member.")
        print("\n")


# Registers a new user
def register(connection):
    print("Welcome to the Online Book Store New Member Registration")
    email_check = True
    
    while email_check:
        email = input("Please enter a valid email address: ")
        if emailCheck(email):
            email_check = False
    password = getpass("Please create a password: ")
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    state = input("Please enter your state: ")
    zip = input("Please enter your zip code: ")
    city = input("Please enter your city: ")
    street_address = input("Please enter your street address: ")
    phone = input("Please enter your phone number: ")

    try:
        with connection.cursor() as cursor:
            
            insert_query = "INSERT INTO Members (password, fname, lname, state, zip, city, address, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_values = (password, first_name, last_name, state, zip, city, street_address, phone, email)
            cursor.execute(insert_query, insert_values)

            
            connection.commit()

            print("You have been added as a member successfully.")

            


    except Error as e:
        print("Error occurred:", e)


# Shows the number of books
def bookShower(rows, num_books, cursor, member, connection):
    i = 0
    while i < len(rows):
        for j in range(num_books):
            if i + j >= len(rows):
                break
            print(f"{rows[i+j][2]} by {rows[i+j][1]} (ISBN: {rows[i+j][0]}, Price: ${rows[i+j][3]})")
        i += num_books
        choice = input("Enter ISBN to add to cart, press ENTER to return to main menu, or press n ENTER to continue browsing: ")
        if choice == "":
            return
        elif choice == "n":
            continue
        else:
            # Check if the isbn is true 
            select_query = "SELECT * FROM books WHERE isbn = %s"
            select_values = (choice,)
            cursor.execute(select_query, select_values)
            row = cursor.fetchone()
            if row and digitCheck(choice):
                # Prompt the user for the quantity to add to the cart
                quantity = int(input("Enter quantity to add to cart: "))
                select_query = "SELECT * FROM Cart WHERE isbn = %s AND user_id = %s"
                select_values = (choice, member)
                cursor.execute(select_query, select_values)
                existing_row = cursor.fetchone()
                # Update the quantity desired if the book is already in the cart
                if existing_row:
                    update_query = "UPDATE Cart SET quantity = %s WHERE isbn = %s AND user_id = %s"
                    update_values = (quantity, choice, member)
                    cursor.execute(update_query, update_values)
                    connection.commit()
                else:
                    # Insert the book into the cart table
                    insert_query = "INSERT INTO Cart (user_id, isbn, quantity) VALUES (%s, %s, %s)"
                    insert_values = (member, choice, quantity)
                    cursor.execute(insert_query, insert_values)
                    connection.commit()
                    print(row[2] + " has been added to your cart.")
            else:
                print("\nInvalid ISBN or it contains non-digits\n")


# Looks thru books by subject 
def subjectBrowser(connection, member):
    try:
        with connection.cursor() as cursor:
            
            cursor.execute("SELECT DISTINCT subject FROM books ORDER BY subject ASC")
            rows = cursor.fetchall()
            subjects = []
            print('There are', len(subjects))

            
            print("Subjects:")
            for row in rows:
                subjects += row
                print("-", row[0])

            
            number = int(input("Choose a subject number: "))
            if number < len(subjects) + 1 and number != 0:
                subject = subjects[number - 1]

                
                select_query = "SELECT * FROM books WHERE subject = %s"
                select_values = (subject,)
                cursor.execute(select_query, select_values)
                rows = cursor.fetchall()

                
                bookShower(rows, 2, cursor, member, connection)
            else:
                print("\n")
                print("Please enter valid subject number!")
                print("\n")

    except Error as e:
        print(e)


# Checks if a string contains only numbers 
def digitCheck(string):
    return string.isdigit()


# Compiles the user cart 
def cart(member, connection):
    with connection.cursor() as cursor:
        
        select_query = """SELECT books.title, books.author, Cart.isbn, Cart.quantity, books.price
                          FROM Cart JOIN books ON Cart.isbn = books.isbn
                          WHERE user_id = %s"""
        select_values = (member,)
        cursor.execute(select_query, select_values)
        items = cursor.fetchall()
        
        total_price = 0
        total_quantity = 0

        if not items:
            print("\n")
            print("Your cart is empty!")
            print("\n")

        else:
            print("Your Cart:")
            for item in items:
                total_quantity += item[3]
                total_price += item[3] * item[4]
                print(item[0] + " by " + item[1] + " (ISBN: " + item[2] + ", Quantity: " + str(item[3]) + ", Price: $" + str(item[4]) + "," + " Total Price: $" + str(item[3] * item[4]) + ")")

            print("Total Quantity: ", total_quantity, "Total Price: ", total_price )
            proceed = input("Proceed to checkout? (Y/N): ")
            if proceed.upper() == "Y":
                memberInvoice(member, connection)
            else:
                print("\n")
                print("Order cancelled.")
                print("\n")


def memberInvoice(member, connection):
    with connection.cursor() as cursor:
        
        select_query = "SELECT address, city, state, zip FROM Members WHERE user_id = %s"
        select_values = (member,)
        cursor.execute(select_query, select_values)
        address = cursor.fetchone()
        addressString = [str(item) for item in address]


        
        select_query = """SELECT books.title, books.author, Cart.isbn, Cart.quantity, books.price, books.isbn
                          FROM Cart JOIN books ON Cart.isbn = books.isbn
                          WHERE user_id = %s"""
        select_values = (member,)
        cursor.execute(select_query, select_values)
        items = cursor.fetchall()

        
        total_price = sum(item[3] * item[4] for item in items)
        total_quantity = sum(item[3] for item in items)
        new_isbn = items[-1][5] if items else ""
        today = datetime.date.today()
        delivery_date = datetime.date.today() + datetime.timedelta(days=10)



        cursor.execute("SELECT COUNT(*) FROM Orders")
        order_count = cursor.fetchone()[0]
        invoice_number = order_count + 1

        insert_query = "INSERT INTO Orders (ono, user_id, shipped, recieved, shipState, shipCity, shipZIP) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert_values = (invoice_number, member, today, delivery_date, address[2], address[1], address[3])
        cursor.execute(insert_query, insert_values)

        insert_query = "INSERT INTO odetails (ono, isbn, quantity, price) VALUES (%s, %s, %s, %s)"
        insert_values = (invoice_number, new_isbn, total_quantity, total_price)
        cursor.execute(insert_query, insert_values)

        # Removes users items from the cart 
        delete_query = "DELETE FROM Cart WHERE user_id = %s"
        delete_values = (member,)
        cursor.execute(delete_query, delete_values)
     
        connection.commit()

        
    # Print a blank line
    print("\n")

    # Print the invoice details
    print(f"Invoice Number: {invoice_number}")
    print(f"Order Date: {today}")
    print(f"Delivery Date: {delivery_date}")
    print(f"Shipping Address: {', '.join(addressString[:4])}")
    print(f"Billing Address: {', '.join(addressString[:4])}")

    # Print the ordered items
    for item in items:
        # extra* to ignore the extra unpacked variables
        title, author, isbn, quantity, price, *extra = item
        print(f"{title} by {author} (ISBN: {isbn}, Quantity: {quantity}, Price: ${price})")

    # Print the total price
    print(f"Total Price: ${total_price}")

    # Print a blank line
    print("\n")



# completes checkout for the user 
def checkout(connection, member):
    cart(member, connection)

# Starts the datababse connection 
def databaseConnector():
    try:
        connection = connect(
            host="localhost",
            user=input("Please input your database username: "),
            password=getpass("Please input your database password: "),
            database="book_Store"
        )
        
        return connection
    except Error as e:
        print("Error connecting to database:", e)
        return None

# allows the user to browse by subject or author 
def menuMember(connection, member):
    while True:
        print("Kindly choose an alternative:")
        print("1. Navigate by subject")
        print("2. Search by author/title")
        print("3. Checkout")
        print("4. Log out")
        choice = input("Please input the number corresponding to your selection (1, 2, 3, or 4):")

        if choice == "1":
            subjectBrowser(connection, member)
        elif choice == "2":
            searchAuthorOrTitle(connection, member)
        elif choice == "3":
            checkout(connection, member)
        elif choice == "4":
            break
        else:
            print("\n")
            print(" Invalid choice")
            print("\n")

# in depth search using author or title 
def searchAuthorOrTitle(connection, member):
    while True:
        print("Search by Author/Title:")
        print("1. Author Search")
        print("2. Title Search")
        print("3. Go Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == "1":
            
            substring = input("Enter author name or part of name: ")
            with connection.cursor() as cursor:
                
                query = "SELECT * FROM books WHERE author LIKE %s"
                values = ("%" + substring + "%",)
                cursor.execute(query, values)
                found_books = cursor.fetchall()
                print("found " + str(len(found_books)) + " books")
                bookShower(found_books, 3, cursor, member, connection)

        elif choice == "2":
            
            substring = input("Enter title or part of title: ")
            with connection.cursor() as cursor:
                query = "SELECT * FROM books WHERE title LIKE %s"
                values = ("%" + substring + "%",)
                cursor.execute(query, values)
                found_books = cursor.fetchall()
                print("found " + str(len(found_books)) + " books")
                bookShower(found_books, 3, cursor, member, connection)
        elif choice == "3":
            
            return

        else:
            print("\n")
            print("Invalid choice. Please try again.\n")
            print("\n")