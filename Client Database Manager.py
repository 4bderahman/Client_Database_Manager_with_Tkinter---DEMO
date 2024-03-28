import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('clients.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS clients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, date TEXT, number_of_commands INTEGER)''')
conn.commit()

def insert_sample_data():
    c.execute('SELECT * FROM clients')
    if c.fetchone() is None:
        sample_data = [
            ('hamid serghini', 'hamido@example.com', '2022-01-01', 5),
            ('aicha benani', 'aicha@example.com', '2022-02-15', 2)
        ]
        c.executemany('INSERT INTO clients (name, email, date, number_of_commands) VALUES (?,?,?,?)', sample_data)
        conn.commit()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    c.execute('SELECT * FROM clients')
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)

def add_client():
    try:
        c.execute('INSERT INTO clients (name, email, date, number_of_commands) VALUES (?,?,?,?)',
                  (name_var.get(), email_var.get(), date_var.get(), int(commands_var.get())))
        conn.commit()
        refresh_table()
        name_var.set('')
        email_var.set('')
        date_var.set('')
        commands_var.set('')
        messagebox.showinfo("Success", "Client added successfully.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to add client. Error: " + str(e))

def delete_client():
    selected_item = tree.selection()[0]
    client_id = tree.item(selected_item)['values'][0]
    c.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    refresh_table()
    messagebox.showinfo("Success", "Client deleted successfully.")
    

insert_sample_data()

root = tk.Tk()
root.title("Client Database Manager")

name_var = tk.StringVar()
email_var = tk.StringVar()
date_var = tk.StringVar()
commands_var = tk.StringVar()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, textvariable=email_var)
email_entry.pack()

tk.Label(root, text="Date").pack()
date_entry = tk.Entry(root, textvariable=date_var)
date_entry.pack()

tk.Label(root, text="Number of Commands").pack()
commands_entry = tk.Entry(root, textvariable=commands_var)
commands_entry.pack()

add_button = tk.Button(root, text="Add Client", command=add_client)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Client", command=delete_client)
delete_button.pack(pady=5)

refresh_button = tk.Button(root, text="Refresh", command=refresh_table)
refresh_button.pack(pady=5)

tree = ttk.Treeview(root, columns=("ID", "Name", "Email", "Date", "Number of Commands"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Date", text="Date")
tree.heading("Number of Commands", text="Number of Commands")
tree.pack()

refresh_table()

root.mainloop()

conn.close()
