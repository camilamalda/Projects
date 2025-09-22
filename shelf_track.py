# Create a database called ebookstore and a table called boook with fields
# id, title, authorID, and qty.
import sqlite3


class BookstoreDB:
    def __init__(self, db_name="ebookstore.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER,
                qty INTEGER
            )
        ''')
        self.conn.commit()
# Create another table called author with fields id, name and country 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT
            )
        ''')
        self.conn.commit()


# Define insert, update, delete, search, and list functions for the book table.
    def insert_book(self, book):
        self.cursor.execute("INSERT INTO book VALUES (?, ?, ?, ?)", book)
        self.conn.commit()

    def update_book(self, book_id, field, new_value):
        self.cursor.execute(
            f"UPDATE book SET {field} = ? WHERE id = ?",
            (new_value, book_id)
        )
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
        self.conn.commit()

    def search_books(self, title):
        self.cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + title + '%',))
        return self.cursor.fetchall()

    def list_books(self):
        self.cursor.execute("SELECT * FROM book")
        return self.cursor.fetchall()    


# Insert sample data into the book table.
def insert_sample_data(store):
    books = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice’s Adventures in Wonderland", 5620, 12)
    ]
    for book in books:
        store.cursor.execute("INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)", book)
    store.conn.commit()


# Insert sample data into the author table.
def insert_sample_authors(store):
    author = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")      
    ]
    for a in author:
        store.cursor.execute("INSERT OR IGNORE INTO author VALUES (?, ?, ?)", a)
    store.conn.commit()


# Main function to interact with the user and perform operations on the book table.
def main():
    store = BookstoreDB()
    insert_sample_data(
        store
    )
    insert_sample_authors(store)

    while True:
        print("\n1. Enter book\n2. Update book\n3. Delete book\n4. Search books\n5. View all details of all books\n0. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            try:
                id = int(input("ID: "))
                title = input("Title: ")
                authorID = int(input("Author ID: "))
                qty = int(input("Quantity: "))
                store.insert_book((id, title, authorID, qty))
                print("Book added.")
            except Exception as e:
                print("Error:", e)

        elif choice == '2':
            id = int(input("Enter book ID to update: "))
            print("What do you want to update?\n1. Quantity\n2. Title\n3. Author ID")
            sub = input("Choose: ")
            if sub == '1':
                value = int(input("New quantity: "))
                store.update_book(id, 'qty', value)
            elif sub == '2':
                value = input("New title: ")
                store.update_book(id, 'title', value)
            elif sub == '3':
                value = int(input("New author ID: "))
                store.update_book(id, 'authorID', value)
            else:
                print("Invalid choice.")
            print("Book updated.")
            author_id = store.cursor.execute("SELECT authorID FROM book WHERE id = ?", (id,)).fetchone()
            if author_id:
                author_id = author_id[0]
                author = store.cursor.execute("SELECT name FROM author WHERE id = ?", (author_id,)).fetchone()
                if author:
                    print(f"\nCurrent Author: {author[0]}, {author[1]}")
                    new_name = input("New author name (press enter to keep current): ").strip()
                    new_country = input ("New author country (press enter to keep current): ").strip()
                    if new_name:
                        store.cursor.execute("UPDATE author SET name = ? WHERE id = ?", (new_name, author_id))
                    if new_country:
                        store.cursor.execute("UPDATE author SET country = ? WHERE id = ?", (new_country, author_id))
                    store.conn.commit()
                    print("Author details updated.")
        elif choice == '3':
            id = int(input("Enter book ID to delete: "))
            store.delete_book(id)
            print("Book deleted.")

        elif choice == '4':
            keyword = input("Enter title to search: ")
            results = store.search_books(keyword)
            for r in results:
                print(r)
# Add funcionality to display all details of all books use zip()            
        elif choice == '5':
            store.cursor.execute('''
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
            ''')
            results = store.cursor.fetchall()
            if results:
                for title, name, country in results: 
                    print("\n--------------------------------------")
                    print(f"Title: {title}")
                    print(f"Author: {name}")
                    print(f"Country: {country}")
                    print("--------------------------------------")
            else:
                print("No book details found.")
        elif choice == '0':
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
