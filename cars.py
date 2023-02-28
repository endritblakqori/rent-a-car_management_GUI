import tkinter as tk
from tkinter import *
import customtkinter
import tkinter.messagebox as tkMessageBox
from tkinter import ttk
import datetime as dt
from datetime import datetime
import tkcalendar

import login
import clients
import database
import admin_screen


class Cars(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.root.title('Cars Window - Dream Ride rent-a-car')
        self.carsControlFrame()

    def carsControlFrame(self):
        self.cars = customtkinter.CTkFrame(self.root, width=400)
        self.cars.pack(fill='both', side=LEFT, expand=True)

        self.tree = customtkinter.CTkFrame(self.root, width=400)
        self.tree.pack(fill='both', side=RIGHT, expand=True)

        # Creating the menu
        menubar = tk.Menu(self)
        self.root.config(menu=menubar)

        # Function that will ask user to confirm logging out
        def logging_out():
            result = tk.messagebox.askquestion("Confirm", "Are you sure you want to log out?", icon='warning')
            if result == 'yes':
                self.cars.destroy()
                self.tree.destroy()
                self.root.config(menu=NONE)
                login.Login(self.root)

        def open_clients():
            self.cars.destroy()
            self.tree.destroy()
            clients.Clients(self.root)

        # Creating new window for authentication for admin screen
        def create_toplevel():
            window = customtkinter.CTkToplevel(self)
            window.attributes("-topmost", True)
            window.title("Admin Authorisation")

            window_width = 400
            window_height = 250
            # get the screen dimension
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            # find the center point
            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)
            window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            # Function that will check if admin password is correct
            def is_admin():
                password = admin_password_entry.get()
                if password == "admin":
                    self.cars.destroy()
                    self.tree.destroy()
                    window.destroy()
                    admin_screen.AdminScreen(self.root)
                elif password == "":
                    message_label.configure(text="Enter password")
                else:
                    message_label.configure(text="Wrong Password")

            # create label on CTkToplevel window
            admin_label = customtkinter.CTkLabel(window, text="The page you are trying to open is restricted."
                                                              " \nEnter the admin password below")
            admin_label.pack(padx=5, pady=15)

            admin_password_entry = customtkinter.CTkEntry(window, placeholder_text="Enter admin password",
                                                          corner_radius=8, text_color=("black", "silver"), show="*")
            admin_password_entry.pack(padx=5, pady=15)

            message_label = customtkinter.CTkLabel(window, text=None, text_color="red")
            message_label.pack(padx=5, pady=10)

            admin_password_button = customtkinter.CTkButton(window, text="Enter", corner_radius=8,
                                                            command=is_admin, fg_color="#556b2f")
            admin_password_button.pack(padx=5, pady=10)

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
            command=create_toplevel
        )

        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        help_menu.add_command(label="About", command=lambda: tkMessageBox.showinfo(
            title="Information",
            message="Here you can add new cars to the fleet or remove cars from the fleet"
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
            menu=car_screen
        )

        log_out = tk.Menu(
            menubar,
            tearoff=0
        )

        menubar.add_cascade(
            label="Log Out",
            command=logging_out
        )

        def save_car():
            mark = mark_entry.get()
            model = model_entry.get()
            year = year_entry.get()
            plates = plates_entry.get()
            reg_date = registration_entry.get()
            available = available_cb.get()
            other = text
            if mark != "" and model != "" and year != "" and plates != "" and reg_date != "" and available != "":
                database.save_car(mark, model, year, plates, reg_date, available, other)
                tkMessageBox.showinfo("Message", "Car saved successfully")
                displayData()
                expiring_reg()
                in_service()
            else:
                tkMessageBox.showinfo("Warning", "Fill the empty field!")

        def update_car():
            mark = mark_entry.get()
            model = model_entry.get()
            year = year_entry.get()
            plates = plates_entry.get()
            reg_date = registration_entry.get()
            available = available_cb.get()
            other = textbox.get("0.0", 'end')
            if mark == "" and model == "" and year == "" and plates == "" and reg_date == "" and available == "":
                tkMessageBox.showinfo("Warning", "Fill the empty field!")
            else:
                cur_item = tree.focus()
                contents = tree.item(cur_item)
                selected_item = contents['values']
                database.update_car(mark, model, year, plates, reg_date, available, other, selected_item)
                tkMessageBox.showinfo("Message", "Car updated successfully")
                displayData()
                expiring_reg()
                in_service()

        def delete_car():
            if not tree.selection():
                tkMessageBox.showwarning("Warning", "Select data to delete")
            else:
                result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                                  icon="warning")
                if result == 'yes':
                    cur_item = tree.focus()
                    contents = tree.item(cur_item)
                    selected_item = contents['values']
                    database.delete_car(selected_item)
                    tkMessageBox.showinfo("Message", "Car deleted successfully")
                    tree.delete(cur_item)
                    displayData()
                    expiring_reg()
                    in_service()

        mark_label = customtkinter.CTkLabel(self.cars, text="Car mark: ", text_color=("black", "silver"),
                                            corner_radius=8)
        mark_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky=tk.NSEW)

        mark_entry = customtkinter.CTkEntry(self.cars, placeholder_text="Enter car mark", corner_radius=10)
        mark_entry.grid(row=0, column=1, padx=5, pady=(20,5), sticky=tk.NSEW)

        model_label = customtkinter.CTkLabel(self.cars, text="Car model: ", text_color=("black", "silver"),
                                             corner_radius=8)
        model_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        model_entry = customtkinter.CTkEntry(self.cars, placeholder_text="Enter car model", corner_radius=10)
        model_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        year_label = customtkinter.CTkLabel(self.cars, text="Car year: ", text_color=("black", "silver"),
                                            corner_radius=8)
        year_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.NSEW)

        year_entry = customtkinter.CTkEntry(self.cars, placeholder_text="Enter car year", corner_radius=10)
        year_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.NSEW)

        plates_label = customtkinter.CTkLabel(self.cars, text="Car plates: ", text_color=("black", "silver"),
                                              corner_radius=8)
        plates_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)

        plates_entry = customtkinter.CTkEntry(self.cars, placeholder_text="Enter car plates", corner_radius=10)
        plates_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.NSEW)

        registration_label = customtkinter.CTkLabel(self.cars, text="Registration date: ",
                                                    text_color=("black", "silver"), corner_radius=8)
        registration_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.NSEW)

        registration_entry = tkcalendar.DateEntry(self.cars, selectmode=dt.date, date_pattern='dd/mm/yyyy')
        registration_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.NSEW)

        available_label = customtkinter.CTkLabel(self.cars, text="Availability: ",
                                                 text_color=("black", "silver"), corner_radius=8)
        available_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.NSEW)

        available_select = customtkinter.StringVar(value="Available")
        available_cb = customtkinter.CTkComboBox(self.cars, values=["Available", "In Service"],
                                                 variable=available_select, corner_radius=8, state='readonly')
        available_cb.grid(row=5, column=1, padx=5, pady=5, sticky=tk.NSEW)

        others_label = customtkinter.CTkLabel(self.cars, text="Other information: ", text_color=("black", "silver"),
                                              corner_radius=8)
        others_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.NSEW)

        textbox = customtkinter.CTkTextbox(self.cars, width=140, height=95, border_width=2)
        textbox.grid(row=6, column=1, padx=5, pady=5, sticky=tk.NSEW)

        textbox.insert("0.0", "")  # insert at line 0 character 0
        text = textbox.get("0.0", "end")  # get text from line 0 character 0 till the end

        textbox.configure(state="normal")

        save_car_button = customtkinter.CTkButton(self.cars, text="Save car", corner_radius=8, command=save_car,
                                                  fg_color="#556b2f")
        save_car_button.grid(row=7, columnspan=2, padx=5, pady=(15, 5))

        update_car_button = customtkinter.CTkButton(self.cars, text="Update car", corner_radius=8, command=update_car,
                                                    fg_color="#556b2f")
        update_car_button.grid(row=8, columnspan=2, padx=5, pady=5)

        delete_car_button = customtkinter.CTkButton(self.cars, text="Delete car", corner_radius=8, command=delete_car,
                                                    fg_color="#556b2f")
        delete_car_button.grid(row=9, columnspan=2, padx=5, pady=5)

        # Table
        columns = ('id', 'mark', 'model', 'year', 'plates', 'reg_date', 'available', 'other')
        tree = ttk.Treeview(self.tree, columns=columns, show='headings')

        tree.heading('id', text='ID')
        tree.heading('mark', text='Mark')
        tree.heading('model', text='Model')
        tree.heading('year', text='Year')
        tree.heading('plates', text='Plates')
        tree.heading('reg_date', text='Registration Date')
        tree.heading('available', text='Availability')
        tree.heading('other', text='Other')

        tree.column(0, stretch=NO, minwidth=0, width=0)
        tree.column('mark', width=90, anchor=tk.CENTER)
        tree.column('model', width=90, anchor=tk.CENTER)
        tree.column('year', width=50, anchor=tk.CENTER)
        tree.column('plates', width=70, anchor=tk.CENTER)
        tree.column('reg_date', width=100, anchor=tk.CENTER)
        tree.column('available', width=70, anchor=tk.CENTER)
        tree.column('other', width=180, anchor=tk.CENTER)

        tree.grid(row=1, column=4, rowspan=10, padx=10, pady=(20,10), ipady=70, sticky=tk.NSEW)

        tree.tag_configure("almost", background="#F3e145")
        tree.tag_configure("expiring", background="#F14848")
        tree.tag_configure("in_service", background="#979799")

        def displayData():
            # clear all the items present in Treeview
            tree.delete(*tree.get_children())
            # select query
            fetch = database.display_car()
            for data in fetch:
                tree.insert('', 'end', values=data)

        def expiring_reg():
            for i in tree.get_children():
                values = tree.item(i)['values']
                today = datetime.today().date()
                our_date = datetime.strptime(values[5], "%d/%m/%Y").date()
                if our_date - today <= dt.timedelta(days=10):
                    tree.item(i, tags=("almost",))
                elif our_date - today <= dt.timedelta(days=1):
                    tree.item(i, tags=("expiring",))

        def in_service():
            for i in tree.get_children():
                values = tree.item(i)['values']
                service = values[6]
                if service == 'In Service':
                    tree.item(i, tags=("in_service",))

        tree.bind("<<TreeviewOpen>>", expiring_reg)
        tree.bind("<<TreeviewOpen>>", in_service)

        displayData()
        expiring_reg()
        in_service()

        def on_click(self):
            mark_entry.delete(0, END)
            model_entry.delete(0, END)
            year_entry.delete(0, END)
            plates_entry.delete(0, END)
            registration_entry.delete(0, END)
            available_cb.set("")
            textbox.delete(1.0, END)

            if not tree.selection():
                pass
            else:
                selected_item = tree.selection()[0]
                mark_entry.insert(0, tree.item(selected_item)['values'][1])
                model_entry.insert(0, tree.item(selected_item)['values'][2])
                year_entry.insert(0, tree.item(selected_item)['values'][3])
                plates_entry.insert(0, tree.item(selected_item)['values'][4])
                registration_entry.insert(0, tree.item(selected_item)['values'][5])
                available = (tree.item(selected_item)['values'][6])
                available_cb.set(available)
                textbox.insert(1.0, tree.item(selected_item)['values'][7])

        tree.bind("<<TreeviewSelect>>", on_click)
