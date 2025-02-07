import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create book table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        qty INTEGER
    )
''')

# Insert initial book data if table is empty
cursor.execute("SELECT COUNT(*) FROM book")
if cursor.fetchone()[0] == 0:
    books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    cursor.executemany("INSERT INTO book VALUES (?, ?, ?, ?)", books)
    conn.commit()

# Function to add a new book
def add_book():
    try:
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter author: ")
        qty = int(input("Enter quantity: "))
        cursor.execute("INSERT INTO book VALUES (?, ?, ?, ?)", (book_id, title, author, qty))
        conn.commit()
        print("Book added successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Function to update book details
def update_book():
    try:
        book_id = int(input("Enter book ID to update: "))
        cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
        book = cursor.fetchone()
        if book:
            new_title = input(f"Enter new title ({book[1]}): ") or book[1]
            new_author = input(f"Enter new author ({book[2]}): ") or book[2]
            new_qty = input(f"Enter new quantity ({book[3]}): ") or book[3]
            cursor.execute("UPDATE book SET title=?, author=?, qty=? WHERE id=?", (new_title, new_author, int(new_qty), book_id))
            conn.commit()
            print("Book updated successfully!")
        else:
            print("Book not found.")
    except Exception as e:
        print(f"Error: {e}")

# Function to delete a book
def delete_book():
    try:
        book_id = int(input("Enter book ID to delete: "))
        cursor.execute("DELETE FROM book WHERE id=?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Function to search for a book
def search_books():
    try:
        search_term = input("Enter book title or author to search: ")
        cursor.execute("SELECT * FROM book WHERE title LIKE ? OR author LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        if results:
            for book in results:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Qty: {book[3]}")
        else:
            print("No books found.")
    except Exception as e:
        print(f"Error: {e}")

# Main menu
while True:
    print("\nBookstore Management System")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_books()
    elif choice == "0":
        print("Exiting the program...")
        break
    else:
        print("Invalid choice, please try again.")

# Close the database connection
conn.close()
