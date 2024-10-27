import mysql.connector

def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Your MySQL host (usually 'localhost')
            user="your_username",  # Your MySQL username
            password="your_password",  # Your MySQL password
            database="library_db"  # The database you created earlier
        )
        if connection.is_connected():
            print("Connection to MySQL database successful")
            return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_tables(connection):
    """Create tables in the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            availability BOOLEAN NOT NULL DEFAULT TRUE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            book_id INT,
            issued_to VARCHAR(255),
            issue_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
        """)
        connection.commit()
        print("Tables created successfully")
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")

def insert_book(connection, title, author):
    """Insert a new book into the books table."""
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        connection.commit()
        print("Book inserted successfully")
    except mysql.connector.Error as e:
        print(f"Error inserting book: {e}")

def issue_book(connection, book_id, issued_to, issue_date):
    """Insert a record into the issued_books table."""
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO issued_books (book_id, issued_to, issue_date) VALUES (%s, %s, %s)",
                       (book_id, issued_to, issue_date))
        connection.commit()
        print("Book issued successfully")
    except mysql.connector.Error as e:
        print(f"Error issuing book: {e}")

def main():
    connection = create_connection()  # Create the connection
    if connection is not None:  # Check if the connection is successful
        create_tables(connection)  # Create tables if connected

        # Example: Insert a book
        insert_book(connection, "The Great Gatsby", "F. Scott Fitzgerald")
        insert_book(connection, "1984", "George Orwell")

        # Example: Issue a book
        issue_book(connection, 1, "John Doe", "2024-10-25")

        connection.close()  # Close the connection after use
    else:
        print("Failed to create database connection")

if __name__ == "__main__":
    main()
