# To installing/checking requirements automatically after running the app
# and then cleaning the CLI before runnung the app
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],stdout=subprocess.DEVNULL)


from Lib_db_conn import DB_CONN
from rich.console import Console
from datetime import datetime


class Book:
    
    def __init__(self, title, author, date):
        self.title = title
        self.author = author
        self.date = date

    def __str__(self):
        return f"{self.title} by {self.author}, published on {self.date}"
        
class LibMenu:
    global console
    console=Console()
    
    def __init__(self) -> None:
        return None

    def choices(self) -> int:
        print("Select an option:")
        print("1. Add book")
        print("2. Delete book")
        print("3. Update book")
        print("4. View all books")
        print("0. Quit")
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
        except ValueError:
            print(f"This {choice} is not a number.")

        return choice
    
    def start(self) -> None:
        console=Console()
        condition = -1
        while condition !=0:
            choice = self.choices()
            if choice == 1:
                console.print("[green]Add a book[/]")
                self.addBook()

            elif choice == 2:
                books = self.getBook()
                if not books:
                    console.print("[yellow]There are no books.[/]")
                    
                else:
                    console.print("[yellow]Select a book to delete: [/]")
                    for book_id, book in books:
                        print(f"ID: [{book_id}]. {book}")
                    book_id = console.input("[green]Enter the book ID: [/]")
                    if not book_id in books:
                        console.print(f"Book with [yellow]ID {book_id}[/] not found.")
                    else:
                        self.deleteBook(book_id)

            elif choice == 3:
                books = self.getBook()
                if not books:
                    console.print("[yellow]There are no books.[/]")
                else:
                    console.print("[green]Select a book to update: [/]")
                    for book in books:
                        print(f"ID: [{book[0]}]. {book[1]}")
                        
                    book_id = console.input("[green]Enter the book ID: [/]")
                    book_id = int(book_id)
                    book_ids = []
                    for book in books:
                        book_ids.append(book[0])
                    if book_id not in book_ids:
                        console.print(f"Book with [yellow]ID {book_id}[/] not found.")
                    else:
                        title = input("Enter the new title: ")
                        author = input("Enter the new author: ")
                        date = input("Enter the new publication date (YYYY-MM-DD): ")
                        book = Book(title, author, date)
                        self.updateBook(book_id, book)


            elif choice == 4:
                books = self.getBook()
                if not books:
                    print("No books found.")
                else:
                    for book_id, book in books:
                        print(f"{book_id}. {book}")

            elif choice == 0:
                break

            else:
                console=Console()
                console.print("[red]Invalid choice. Please try again.[/]")
    def addBook(self) -> None:
        cursor = DB_CONN.cursor()
        statement = "INSERT INTO books(title, author, date) VALUES(?, ?, ?)"
        record_data = self.Detailes()
        cursor.execute(statement, record_data)
        DB_CONN.commit()
        cursor.close()
        return None
    def Detailes(self) -> tuple[str, str, str]:
        title = input("Enter the title: ")
        author = input("Enter the author: ")
        date = input("Enter the publication date (DD-MM-YYYY): ")        
        book = (title, author, date)
        return book

    def deleteBook(self, book_id) -> None:
        delete = DB_CONN.cursor()
        delete.execute("DELETE FROM books WHERE id = ?", (book_id,))
        DB_CONN.commit()
        print(f"Deleted book with ID: {book_id}")
    


    def updateBook(self, book_id, book):
        
        update = DB_CONN.cursor()
        update.execute("UPDATE books SET title = ?, author = ?, date = ? WHERE id = ?",
                  (book.title, book.author, book.date, book_id))
        DB_CONN.commit()
        console.print(f"[green]Updated[/] book with ID: [{book_id}] to {book}") 


    def getBook(self) -> list[tuple[int, Book]]:
        cursor = DB_CONN.cursor()
        sql_statement = "SELECT * FROM books"
        cursor.execute(sql_statement)
        books = []
        for row in cursor.fetchall():
            book_id = row[0]
            title = row[1]
            author = row[2]
            date = row[3]
            book = Book(title, author, date)
            books.append((book_id, book))
        DB_CONN.commit()
        cursor.close()
        return books

    