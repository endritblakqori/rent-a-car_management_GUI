import hashlib
import os
import tkinter as tk
from tkinter import *
import customtkinter
import tkinter.messagebox as tkMessageBox
from tkinter import ttk
import database
import cars
import login
import clients


class AdminScreen(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        window_width = 800
        window_height = 400
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        icon = PhotoImage(os.getcwd() + '\\car.ico\\')
        root.iconbitmap(default=icon)

        # set the position of the window to the center of the screen
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        self.root.title('Admin Window - Dream Ride rent-a-car')
        self.adminControlFrame()

    def adminControlFrame(self):
        self.entry = customtkinter.CTkFrame(self.root, width=400)
        self.entry.pack(fill='both', side=LEFT, expand=True)

        self.tree = customtkinter.CTkFrame(self.root, width=400)
        self.tree.pack(fill='both', side=RIGHT, expand=True)

        # Function that will ask user to confirm logging out
        def logging_out():
            result = tk.messagebox.askquestion("Confirm", "Are you sure you want to log out?", icon='warning')
            if result == 'yes':
                self.entry.destroy()
                self.tree.destroy()
                self.root.config(menu=NONE)
                login.Login(self.root)

        def open_cars():
            self.entry.destroy()
            self.tree.destroy()
            cars.Cars(self.root)

        def open_clients():
            self.entry.destroy()
            self.tree.destroy()
            clients.Clients(self.root)

        # Creating the menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # create the main
        main = tk.Menu(
            menubar,
            tearoff=0
        )

        # add the main menu to the menubar
        menubar.add_cascade(
            label="Main",
            command=open_clients
        )

        admin = tk.Menu(
            menubar,
            tearoff=0
        )

        menubar.add_cascade(
            label="Admin",
            menu=admin  # Add admin screen
        )

        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        help_menu.add_command(label="About", command=lambda: tkMessageBox.showinfo(
            title="Information",
            message="Here you can add, update, and delete users"
        ))

        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )

        car_screen = tk.Menu(
            menubar,
            tearoff=0
        )

        menubar.add_cascade(
            label="Cars",
            command=open_cars
        )

        log_out = tk.Menu(
            menubar,
            tearoff=0
        )

        menubar.add_cascade(
            label="Log Out",
            command=logging_out
        )

        def save_employee():
            user = user_entry.get()
            passw = password_entry.get()
            password = passw.encode('utf-8')
            hash_pass = hashlib.sha3_256(password).hexdigest()

            if user != "" and password != "":
                database.save_employee(user, hash_pass)
                tkMessageBox.showinfo("Message", "User saved successfully")
                displayData()
            else:
                tkMessageBox.showinfo("Warning", "Fill the empty field!")

        def update_employee():
            user = user_entry.get()
            password = password_entry.get()
            if user == "" and password == "":
                tkMessageBox.showinfo("Warning", "Fill the empty field!")
            else:
                cur_item = tree.focus()
                contents = tree.item(cur_item)
                selected_item = contents['values']
                database.update_employee(user, password, selected_item)
                tkMessageBox.showinfo("Message", "User updated successfully")
                displayData()

        def delete_employee():
            if not tree.selection():
                tkMessageBox.showwarning("Warning", "Select data to delete")
            else:
                result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                                  icon="warning")
                if result == 'yes':
                    cur_item = tree.focus()
                    contents = tree.item(cur_item)
                    selected_item = contents['values']
                    database.delete_employee(selected_item)
                    tree.delete(cur_item)
                    displayData()

        user_label = customtkinter.CTkLabel(self.entry, text="Employee ID:", corner_radius=8, text_color=("black", "silver"))
        user_label.grid(row=0, column=0, padx=5, pady=(60, 5), sticky=tk.NSEW)

        user_entry = customtkinter.CTkEntry(self.entry, placeholder_text="Enter employee ID", corner_radius=8)
        user_entry.grid(row=0, column=1, padx=5, pady=(60, 5), sticky=tk.NSEW)

        password_label = customtkinter.CTkLabel(self.entry, text="Employee password:", corner_radius=8,
                                                text_color=("black", "silver"))
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        password_entry = customtkinter.CTkEntry(self.entry, placeholder_text="Enter employee password", corner_radius=8)
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        save_employee_button = customtkinter.CTkButton(self.entry, text="Save employee", corner_radius=8,
                                                       fg_color="#556b2f", command=save_employee)
        save_employee_button.grid(row=2, columnspan=2, padx=5, pady=(15, 5))

        update_employee_button = customtkinter.CTkButton(self.entry, text="Update employee", corner_radius=8,
                                                         fg_color="#556b2f", command=update_employee)
        update_employee_button.grid(row=3, columnspan=2, padx=5, pady=(15, 5))

        delete_employee_button = customtkinter.CTkButton(self.entry, text="Delete employee", corner_radius=8,
                                                         fg_color="#556b2f", command=delete_employee)
        delete_employee_button.grid(row=4, columnspan=2, padx=5, pady=(15, 5))

        # table
        columns = ('id', 'user', 'password')
        tree = ttk.Treeview(self.tree, columns=columns, show='headings')
        # define headings
        tree.heading('id', text='ID')
        tree.heading('user', text='Employee ID')
        tree.heading('password', text='Password')

        # setting width of the columns
        tree.column(0, stretch=NO, minwidth=0, width=0)
        tree.column(1, stretch=NO, minwidth=0, width=190, anchor=tk.CENTER)
        tree.column(2, stretch=NO, minwidth=0, width=190, anchor=tk.CENTER)

        tree.grid(column=1, rowspan=5, row=2, sticky=tk.NSEW, padx=5, pady=40)

        def displayData():
            # clear all the items present in Treeview
            tree.delete(*tree.get_children())
            # select query
            fetch = database.display_user()
            for data in fetch:
                tree.insert('', 'end', values=data)

        displayData()

        def on_click(self):
            user_entry.delete(0, END)
            password_entry.delete(0, END)

            if not tree.selection():
                pass
            else:
                selected_item = tree.selection()[0]
                user_entry.insert(0, tree.item(selected_item)['values'][1])
                password_entry.insert(0, tree.item(selected_item)['values'][2])

        tree.bind("<<TreeviewSelect>>", on_click)