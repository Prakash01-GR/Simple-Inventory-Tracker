from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
import mysql.connector
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='thirumuruga'
)
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        price FLOAT NOT NULL,
        restock_quantity INT NOT NULL
    )
''')
db.commit()
def add_product():
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()
    restock_quantity = entry_restock_quantity.get()
    if name and quantity.isdigit() and price.replace('.', '', 1).isdigit() and restock_quantity.isdigit():
        cursor.execute("INSERT INTO products (name, quantity, price, restock_quantity) VALUES (%s, %s, %s, %s)", (name, int(quantity), float(price), int(restock_quantity)))
        db.commit()
        msg.showinfo("Success", "Product added successfully!")
        entry_name.delete(0, END)
        entry_quantity.delete(0, END)
        entry_price.delete(0, END)
        entry_restock_quantity.delete(0, END)
    else:
        msg.showerror("Error", "Please enter valid data.")

def display_products():
    display_window = Toplevel()
    display_window.title("All Products")
    display_window.geometry('1000x400')
    display_window.configure(bg='white')

    tree = ttk.Treeview(display_window, columns=('ID', 'Name', 'Quantity', 'Price', 'Restock Quantity'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Price', text='Price')
    tree.heading('Restock Quantity', text='Restock Quantity')
    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    for product in products:
        tree.insert('', END, values=product)

def search_product():
    name = entry_search.get()
    search_window = Toplevel()
    search_window.title(f"Search Results for '{name}'")
    search_window.geometry('1000x400')
    search_window.configure(bg='white')
    tree = ttk.Treeview(search_window, columns=('ID', 'Name', 'Quantity', 'Price', 'Restock Quantity'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Price', text='Price')
    tree.heading('Restock Quantity', text='Restock Quantity')
    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{name}%",))
    products = cursor.fetchall()
    for product in products:
        tree.insert('', END, values=product)

def display_restock():
    restock_window = Toplevel()
    restock_window.title("Products That Need Restocking")
    restock_window.geometry('1000x400')
    restock_window.configure(bg='white')
    
    tree = ttk.Treeview(restock_window, columns=('ID', 'Name', 'Quantity', 'Price', 'Restock Quantity'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Price', text='Price')
    tree.heading('Restock Quantity', text='Restock Quantity')
    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM products WHERE quantity > restock_quantity AND restock_quantity < 100")
    products = cursor.fetchall()
    if not products:
        tree.insert('', END, values=("No products need restocking", "", "", "", ""))
    else:
        for product in products:
            tree.insert('', END, values=product)
a = Tk()
a.title("Simple Inventory Tracker")
a.geometry('800x800')
a.configure(bg='white')
frame_add = LabelFrame(a, text="Add Product", bg='white')
frame_add.pack(pady=20)

Label(frame_add, text="Product Name:", bg='white').grid(row=0, column=0, padx=10, pady=10)
entry_name = Entry(frame_add)
entry_name.grid(row=0, column=1, padx=10, pady=10)

Label(frame_add, text="Quantity:", bg='white').grid(row=1, column=0, padx=10, pady=10)
entry_quantity = Entry(frame_add)
entry_quantity.grid(row=1, column=1, padx=10, pady=10)

Label(frame_add, text="Price:", bg='white').grid(row=2, column=0, padx=10, pady=10)
entry_price = Entry(frame_add)
entry_price.grid(row=2, column=1, padx=10, pady=10)

Label(frame_add, text="Restock Quantity:", bg='white').grid(row=3, column=0, padx=10, pady=10)
entry_restock_quantity = Entry(frame_add)
entry_restock_quantity.grid(row=3, column=1, padx=10, pady=10)

Button(frame_add, text="Add Product", command=add_product).grid(row=4, columnspan=2, pady=20)
Button(a, text="Display All Products", command=display_products).pack(pady=20)
frame_search_section = LabelFrame(a, text="Search Product", bg='white')
frame_search_section.pack(pady=20)
Label(frame_search_section, text="Product Name:", bg='white').grid(row=0, column=0, padx=10, pady=10)
entry_search = Entry(frame_search_section)
entry_search.grid(row=0, column=1, padx=10, pady=10)

Button(frame_search_section, text="Search", command=search_product).grid(row=1, columnspan=2, pady=10)
Button(a, text="Display Products Threshold Restocking", command=display_restock).pack(pady=20)

a.mainloop()