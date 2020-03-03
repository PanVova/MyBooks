import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from sqlalchemy import Column, Integer, String, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from tkinter import messagebox as mb

engine = sa.create_engine("sqlite:///MyBooks1.db")
Base = declarative_base()
metadata = sa.MetaData()

titles = sa.Table("Books", metadata,
                  sa.Column("id", sa.Integer, primary_key=True),
                  sa.Column("Name", sa.String(50), nullable=False),
                  sa.Column("Author", sa.String(50), nullable=False),
                  sa.Column("Price",sa.Integer,nullable=False)

                  )
metadata.create_all(engine)
Session = sessionmaker(engine)
ses = Session()

class Book(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    price = Column(Integer)


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)



def delete_book(event):

    id = int(tree.item(tree.selection()).get('text'))
    ses.query(Book).filter_by(id=id).delete()
    ses.commit()
    show_books()

def show_books():

    for i in tree.get_children():
        tree.delete(i)

    books = ses.query(Book).all()
    for book in books:
        print(book.id, book.name,book.author,book.price)
        tree.insert('', 'end', text=str(book.id), values=(book.name, book.author, book.price))
    ses.commit()

def add_book(event , name,author,price):
    print(name+'\n'+author+'\n'+price)
    try:
        price1 = int(price)

        if name == '':
            name = "Empty"
        if author == '':
            author = "Empty"
        if price == '':
            price = 0

        book = Book(name=name, author=author, price=price1)
        ses.add(book)
        ses.commit()

    except ValueError:
        mb.showerror("Error", "Must be entered a number")



    show_books()

def edit_book(event , name,author,price):
    print(name+'\n'+author+'\n'+price)
    try:
        price1 = int(price)
        if name == '':
            name = "Empty"
        if author=='':
            author = "Empty"
        if price == '':
            price='0'

        id = int(tree.item(tree.selection()).get('text'))
        ses.query(Book).filter(Book.id == id).update({'name': name,'author': author, 'price':price1 })

        ses.commit()
        show_books()

    except ValueError:
        mb.showerror("Error", "Must be entered a number")

def open_dialog(event):
    window = tk.Toplevel(root)
    window.title('Add new book')
    window.geometry('400x220+400+300')
    window.resizable(False, False)

    label_name = tk.Label(window, text='Name:')
    label_name.place(x=50, y=50)

    label_author = tk.Label(window, text='Author:')
    label_author.place(x=50, y=80)

    label_sum = tk.Label(window, text='Price:')
    label_sum.place(x=50, y=110)

    window.entry_name = ttk.Entry(window)
    window.entry_name.place(x=200, y=50)

    window.entry_author = ttk.Entry(window)
    window.entry_author.place(x=200, y=80)

    window.entry_price = ttk.Entry(window)
    window.entry_price.place(x=200, y=110)


    btn_cancel = ttk.Button(window, text='Close', command=window.destroy)
    btn_cancel.place(x=300, y=170)

    window.btn_ok = ttk.Button(window, text='Add')
    window.btn_ok.place(x=220, y=170)


    window.btn_ok.bind('<Button-1>', lambda event: add_book(event, window.entry_name.get(),window.entry_author.get(),window.entry_price.get()))

    window.grab_set()
    window.focus_set()

def open_update_dialog(event):

    window = tk.Toplevel(root)
    window.title('Edit book')
    window.geometry('400x220+400+300')
    window.resizable(False, False)

    label_name = tk.Label(window, text='Name:')
    label_name.place(x=50, y=50)

    label_author = tk.Label(window, text='Author:')
    label_author.place(x=50, y=80)

    label_sum = tk.Label(window, text='Price:')
    label_sum.place(x=50, y=110)

    window.entry_name = ttk.Entry(window)
    window.entry_name.place(x=200, y=50)

    window.entry_author = ttk.Entry(window)
    window.entry_author.place(x=200, y=80)

    window.entry_price = ttk.Entry(window)
    window.entry_price.place(x=200, y=110)


    btn_cancel = ttk.Button(window, text='Close', command=window.destroy)
    btn_cancel.place(x=300, y=170)

    window.btn_ok = ttk.Button(window, text='Edit')
    window.btn_ok.place(x=220, y=170)

    window.btn_ok.bind('<Button-1>', lambda event: edit_book(event, window.entry_name.get(),window.entry_author.get(),window.entry_price.get()))

    window.grab_set()
    window.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)

    b = Button(text='ADD', width=10, height=3)
    b.grid(row=0, column=0)
    b.bind('<Button-1>', open_dialog)

    b1 = Button(text='EDIT', width=10, height=3)
    b1.grid(row=0, column=1)
    b1.bind('<Button-1>', open_update_dialog)

    b2 = Button(text='DELETE', width=10, height=3)
    b2.grid(row=0, column=2,pady=10)
    b2.bind('<Button-1>', delete_book)

    tree = Treeview(root, selectmode="extended", columns= ('Name','Author', 'Price'))

    tree.heading("#0", text="ID")
    tree.column("#0", minwidth=0, width=100, stretch=NO)

    tree.heading("Name", text="Name")
    tree.column("Name", minwidth=0, width=300, stretch=NO)

    tree.heading("Author", text="Author")
    tree.column("Author", minwidth=10, width=200, stretch=NO)

    tree.heading("Price", text="Price $")
    tree.column("Price", minwidth=0, width=100, stretch=NO)


    tree.grid(row=1, column=0,columnspan=3, pady=10)

    show_books()

    root.title("MyBooks")
    root.geometry("700x310")
    root.resizable(False, False)
    root.mainloop()


