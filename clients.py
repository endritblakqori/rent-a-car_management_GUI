import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import customtkinter
import dateutil

import database
import datetime as dt
from datetime import datetime
import tkcalendar
from dateutil.relativedelta import relativedelta
import login
import cars
import admin_screen


class Clients(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        window_width = 1000
        window_height = 500
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

        self.root.title('Clients Window - Dream Ride rent-a-car')
        self.clientsControlFrame()

    def clientsControlFrame(self):
        self.clients = customtkinter.CTkFrame(self.root)
        self.clients.pack(fill='both', side=TOP, expand=True)

        date = dt.datetime.now()

        # Function that will ask user to confirm logging out
        def logging_out():
            result = tk.messagebox.askquestion("Confirm", "Are you sure you want to log out?", icon='warning')
            if result == 'yes':
                self.clients.destroy()
                # self.tree.destroy()
                self.root.config(menu=NONE)
                login.Login(self.root)

        def open_cars():
            self.clients.destroy()
            cars.Cars(self.root)

        # Creating new window for authentication for admin screen
        def create_toplevel():
            window = customtkinter.CTkToplevel(self)
            window.attributes("-topmost", True)
            window.title("Admin Authorisation")

            icon = PhotoImage(os.getcwd() + '\\car.ico\\')
            window.iconbitmap(default=icon)

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
                    self.clients.destroy()
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
            menu=main
        )

        admin = tk.Menu(
            menubar,
            tearoff=0
        )

        menubar.add_cascade(
            label="Admin",
            command=create_toplevel  # Add admin screen
        )

        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        help_menu.add_command(label="About", command=lambda: tkMessageBox.showinfo(
            title="Information",
            message="Here you can add, update, search and delete clients"
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

        # Function that will search clients by name
        def search_client():
            if name_entry.get() != "":
                tree.delete(*tree.get_children())
                res = database.search_client(name_entry.get())
                tree.insert('', 'end', values=res)
            else:
                tkMessageBox.showinfo('Message', 'Fill the name field')

        # Function that will add new clients
        def add_client():
            name = name_entry.get()
            surname = surname_entry.get()
            gender = gender_cb.get()
            no_id = id_entry.get()
            birthday = birthday_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            date_from = date_from_entry.get()
            date_until = date_until_entry.get()
            car = cars_cb.get()
            plates = plates_cb.get()
            if name != "" and surname != "" and gender != "" and no_id != "" and birthday != "" and address != "" \
                    and phone != "" and email != "" and date_from != "" and date_until != "" and car != "" and plates != "":
                for i in tree.get_children():
                    values = tree.item(i)['values']
                    plates_exist = values[12]
                    date_expire = values[10]
                    date_start = values[9]
                    # Converting date string into datetime object
                    date_f = datetime.strptime(date_from, "%d/%m/%Y")
                    date_u = datetime.strptime(date_until, "%d/%m/%Y")
                    date_e = datetime.strptime(date_expire, "%d/%m/%Y")
                    date_s = datetime.strptime(date_start, "%d/%m/%Y")
                    if plates == plates_exist:
                        if date_e >= date_f >= date_s or date_e >= date_u >= date_s:
                            tkMessageBox.showinfo("Message", f"{car} with plates {plates} is unavailable at selected "
                                                             f"dates")
                            return
                    if date_f > date_u:
                        tkMessageBox.showwarning("Message", "Dates are invalid. Please check the dates!")
                        return
                # Checking if client is over 18 years old
                now = datetime.utcnow()
                now = now.date()
                birthday_form = datetime.strptime(birthday, "%d/%m/%Y").date()
                age = dateutil.relativedelta.relativedelta(now, birthday_form)
                age = age.years
                if age < 18:
                    tkMessageBox.showwarning("Client under 18", "Client must be over 18 years old")
                    return

                database.add_client(name, surname, gender, no_id, birthday, address, phone, email, date_from,
                                    date_until,
                                    car, plates)
                tkMessageBox.showinfo("Message", "Client added successfully")
                displayData()
                expiring_car()
            else:
                tkMessageBox.showinfo("Message", "Fill all the empty fields")

        # Updating clients information
        def update_client():
            name = name_entry.get()
            surname = surname_entry.get()
            gender = gender_cb.get()
            no_id = id_entry.get()
            birthday = birthday_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            date_from = date_from_entry.get()
            date_until = date_until_entry.get()
            car = cars_cb.get()
            plates = plates_cb.get()
            if name == "" and surname == "" and birthday == "" and gender == "" and no_id == "" and address == "" \
                    and phone == "" and email == "" and date_from == "" and date_until == "" and car == "" \
                    and plates == "":
                tkMessageBox.showinfo("Warning", "Fill the empty field!")
            else:
                for i in tree.get_children():
                    values = tree.item(i)['values']
                    plates_exist = values[12]
                    date_expire = values[10]
                    date_start = values[9]
                    # Converting date string into datetime object
                    date_f = datetime.strptime(date_from, "%d/%m/%Y")
                    date_u = datetime.strptime(date_until, "%d/%m/%Y")
                    date_e = datetime.strptime(date_expire, "%d/%m/%Y")
                    date_s = datetime.strptime(date_start, "%d/%m/%Y")
                    if date_f != date_s and date_u != date_e:
                        if date_f > date_u:
                            tkMessageBox.showwarning("Message", "Dates are invalid. Please check the dates!")
                            return
                        if plates == plates_exist:
                            if date_e >= date_f >= date_s or date_e >= date_u >= date_s:
                                tkMessageBox.showinfo("Message", f"{car} with plates {plates} is unavailable at selected "
                                                                 f"dates")
                                return
                # Checking if client is over 18 years old
                now = datetime.utcnow()
                now = now.date()
                birthday_form = datetime.strptime(birthday, "%d/%m/%Y").date()
                age = dateutil.relativedelta.relativedelta(now, birthday_form)
                age = age.years
                if age < 18:
                    tkMessageBox.showwarning("Client under 18", "Client must be over 18 years old")
                    return
                item = tree.focus()
                contents = (tree.item(item))
                selected_item = contents['values']
                database.update_client(name, surname, gender, no_id, birthday, address, phone, email, date_from,
                                       date_until, car, plates, selected_item)
                tkMessageBox.showinfo("Message", "Updated successfully")
                displayData()
                expiring_car()

        # Deleting clients
        def delete_client():
            if not tree.selection():
                tkMessageBox.showwarning("Warning", "Select data to delete")
            else:
                result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                                  icon="warning")
                if result == "yes":
                    item = tree.focus()
                    contents = tree.item(item)
                    selected_item = contents['values']
                    database.delete_client(selected_item)
                    tree.delete(item)
                    displayData()
                    expiring_car()

        def reset_client():
            tree.delete(*tree.get_children())
            displayData()
            expiring_car()
            name_entry.delete(0, END)
            surname_entry.delete(0, END)
            gender_cb.set("")
            id_entry.delete(0, END)
            birthday_entry.set_date(date)
            address_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            date_from_entry.set_date(date)
            date_until_entry.set_date(date)
            cars_cb.set("")
            plates_cb.set("")

        # name
        name_label = customtkinter.CTkLabel(self.clients, text="Name:", corner_radius=8)
        name_label.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)

        name_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        name_entry.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # surname
        surname_label = customtkinter.CTkLabel(self.clients, text="Surname:", corner_radius=8)
        surname_label.grid(column=2, row=0, sticky=tk.NSEW, padx=5, pady=5)

        surname_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        surname_entry.grid(column=3, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # gender_label
        gender_label = customtkinter.CTkLabel(self.clients, text="Gender:", corner_radius=8)
        gender_label.grid(column=4, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # create a combobox
        selected_gender = customtkinter.StringVar(value="Male")

        gender_cb = customtkinter.CTkComboBox(self.clients, values=["Male", "Female"],
                                              variable=selected_gender, corner_radius=8, state='readonly')

        # place the widget
        gender_cb.grid(column=5, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # ID
        id_label = customtkinter.CTkLabel(self.clients, text="NO. ID:", corner_radius=8)
        id_label.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5)

        id_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        id_entry.grid(column=1, row=1, sticky=tk.NSEW, padx=5, pady=5)

        # birthday
        birthday_label = customtkinter.CTkLabel(self.clients, text="Birthday:", corner_radius=8)
        birthday_label.grid(column=2, row=1, sticky=tk.NSEW, padx=5, pady=5)

        birthday_entry = tkcalendar.DateEntry(self.clients, selectmode=date, date_pattern='dd/mm/yyyy')
        birthday_entry.grid(column=3, row=1, sticky=tk.NSEW, padx=5, pady=5)

        # Address
        address_label = customtkinter.CTkLabel(self.clients, text="Address:", corner_radius=8)
        address_label.grid(column=4, row=1, sticky=tk.NSEW, padx=5, pady=5)

        address_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        address_entry.grid(column=5, row=1, sticky=tk.NSEW, padx=5, pady=5, ipadx=9)

        date_from_label = customtkinter.CTkLabel(self.clients, text="Date When:", corner_radius=8)
        date_from_label.grid(column=4, row=2, sticky=tk.NSEW, padx=5, pady=5)

        date_from_entry = tkcalendar.DateEntry(self.clients, selectmode=date, date_pattern='dd/mm/yyyy')
        date_from_entry.grid(column=5, row=2, sticky=tk.NSEW, padx=5, pady=5)

        date_until_label = customtkinter.CTkLabel(self.clients, text="Date Until:", corner_radius=8)
        date_until_label.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=5)

        date_until_entry = tkcalendar.DateEntry(self.clients, selectmode=date, date_pattern='dd/mm/yyyy')
        date_until_entry.grid(column=1, row=3, sticky=tk.NSEW, padx=5, pady=5)

        car_label = customtkinter.CTkLabel(self.clients, text="Car:", corner_radius=8)
        car_label.grid(column=2, row=3, sticky=tk.NSEW, padx=5, pady=5)

        def show_plates(event):
            plates_cb.set('')
            selected_car = cars_cb.get()
            mark, model = selected_car.split(" ", 1)
            plates = database.fetch_plates(mark, model)
            plates_cb.configure(values=plates)

        results = database.show_car()

        selected_cars = customtkinter.StringVar()
        cars_cb = customtkinter.CTkComboBox(self.clients, values=[f"{mark} {model}" for mark, model, available in results],
                                            variable=selected_cars, state='readonly', width=158, command=show_plates)

        cars_cb.grid(column=3, row=3, sticky=tk.NSEW, padx=5, pady=5)

        phone_label = customtkinter.CTkLabel(self.clients, text="Phone Number:", corner_radius=8)
        phone_label.grid(column=0, row=2, sticky=tk.NSEW, padx=5, pady=5)

        phone_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        phone_entry.grid(column=1, row=2, sticky=tk.NSEW, padx=5, pady=5)

        email_label = customtkinter.CTkLabel(self.clients, text="Email:", corner_radius=8)
        email_label.grid(column=2, row=2, sticky=tk.NSEW, padx=5, pady=5)

        email_entry = customtkinter.CTkEntry(self.clients, corner_radius=8)
        email_entry.grid(column=3, row=2, sticky=tk.NSEW, padx=5, pady=5)

        plates_label = customtkinter.CTkLabel(self.clients, text="Car plates:", corner_radius=8)
        plates_label.grid(column=4, row=3, padx=5, pady=5)

        plates_cb = customtkinter.StringVar()
        plates_cb = customtkinter.CTkComboBox(self.clients, width=158, state='readonly')
        plates_cb.grid(column=5, row=3, sticky=tk.NSEW, padx=5, pady=5)

        search_button = customtkinter.CTkButton(self.clients, text="Search", corner_radius=8, command=search_client,
                                                width=100, fg_color="#556b2f")
        search_button.grid(column=0, row=4, padx=(25, 1), pady=5)

        update_button = customtkinter.CTkButton(self.clients, text="Update", corner_radius=8, command=update_client,
                                                width=100, fg_color="#556b2f")
        update_button.grid(column=1, row=4, padx=5, pady=5)

        save_button = customtkinter.CTkButton(self.clients, text="Save", corner_radius=8, command=add_client, width=100,
                                              fg_color="#556b2f")
        save_button.grid(column=2, row=4, padx=5, pady=5, columnspan=2)

        delete_button = customtkinter.CTkButton(self.clients, text="Delete", corner_radius=8, command=delete_client,
                                                width=100,
                                                fg_color="#556b2f")
        delete_button.grid(column=4, row=4, padx=5, pady=5)

        rest_button = customtkinter.CTkButton(self.clients, text="Reset", corner_radius=8, command=reset_client,
                                              width=100,
                                              fg_color="#556b2f")
        rest_button.grid(column=5, row=4, padx=5, pady=5)

        # Table
        columns = ('id', 'name', 'surname', 'birthday', 'gender', 'no_id', 'address', 'phone', 'email', 'date_from',
                   'date_until', 'car', 'plates')
        tree = ttk.Treeview(self.clients, columns=columns, show='headings')

        tree.heading('id', text='ID')
        tree.heading('name', text='Name')
        tree.heading('surname', text='Surname')
        tree.heading('birthday', text='Birthday')
        tree.heading('gender', text='Gender')
        tree.heading('no_id', text='No ID.')
        tree.heading('address', text='Address')
        tree.heading('phone', text='Phone Nr.')
        tree.heading('email', text='Email')
        tree.heading('date_from', text='Date From')
        tree.heading('date_until', text='Date Until')
        tree.heading('car', text='Car')
        tree.heading('plates', text='Plates')

        tree.column(0, stretch=NO, minwidth=0, width=0)
        tree.column("name", width=50, anchor=CENTER)
        tree.column("surname", width=50, anchor=CENTER)
        tree.column("birthday", width=50, anchor=CENTER)
        tree.column("gender", width=30, anchor=CENTER)
        tree.column("no_id", width=50, anchor=CENTER)
        tree.column("address", width=80, anchor=CENTER)
        tree.column("phone", width=50, anchor=CENTER)
        tree.column("email", width=80, anchor=CENTER)
        tree.column("date_from", width=40, anchor=CENTER)
        tree.column("date_until", width=40, anchor=CENTER)
        tree.column("car", width=70, anchor=CENTER)
        tree.column("plates", width=50, anchor=CENTER)

        tree.grid(column=0, columnspan=10, row=5, sticky=tk.NSEW, padx=5, pady=5, ipadx=33, ipady=22)

        # Create a new tag with a specific background color
        tree.tag_configure("expiring", background="#F14848")
        tree.tag_configure("not_expiring", background="white")
        tree.tag_configure("almost", background="#F3e145")

        today = datetime.today().date()
        formatted_date = today.strftime("%d/%m/%Y")
        one_day = dt.timedelta(days=1)
        tomorrow = today + one_day
        formatted_tomorrow = tomorrow.strftime("%d/%m/%Y")

        def displayData():
            # clear all the items present in Treeview
            tree.delete(*tree.get_children())
            # select query
            fetch = database.display_data()
            for data in fetch:
                tree.insert('', 'end', values=data)

        def expiring_car():
            for i in tree.get_children():
                # Get the values of the current row
                values = tree.item(i)["values"]
                our_date = date.strptime(values[10], "%d/%m/%Y")
                today_dt = date.strptime(formatted_date, "%d/%m/%Y")
                tomorrow_dt = date.strptime(formatted_tomorrow, "%d/%m/%Y")
                if our_date <= today_dt:
                    # If it is, configure the tag for that row
                    tree.item(i, tags=("expiring",))
                elif our_date == tomorrow_dt:
                    tree.item(i, tags=("almost",))
                else:
                    tree.item(i, tags=("not_expiring",))

        tree.bind("<<TreeviewOpen>>", expiring_car)

        displayData()
        expiring_car()

        def on_double_click(self):
            name_entry.delete(0, END)
            surname_entry.delete(0, END)
            birthday_entry.delete(0, END)
            gender_cb.set("")
            id_entry.delete(0, END)
            address_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            date_from_entry.delete(0, END)
            date_until_entry.delete(0, END)
            cars_cb.set("")
            plates_cb.set("")

            if not tree.selection():
                pass
            else:
                selected_item = tree.selection()[0]
                name_entry.insert(0, tree.item(selected_item)['values'][1])
                surname_entry.insert(0, tree.item(selected_item)['values'][2])
                birthday_entry.insert(0, tree.item(selected_item)['values'][3])
                gen = (tree.item(selected_item)['values'][4])
                gender_cb.set(gen)
                id_entry.insert(0, tree.item(selected_item)['values'][5])
                address_entry.insert(0, tree.item(selected_item)['values'][6])
                phone_entry.insert(0, tree.item(selected_item)['values'][7])
                email_entry.insert(0, tree.item(selected_item)['values'][8])
                date_from_entry.insert(0, tree.item(selected_item)['values'][9])
                date_until_entry.insert(0, tree.item(selected_item)['values'][10])
                car = (tree.item(selected_item)['values'][11])
                cars_cb.set(car)
                plates = (tree.item(selected_item)['values'][12])
                plates_cb.set(plates)

        tree.bind("<<TreeviewSelect>>", on_double_click)
