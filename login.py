import tkinter
from tkinter import *
import customtkinter
import database
import os
import clients


class Login(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # window_width = 800
        # window_height = 400
        # # get the screen dimension
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # # find the center point
        # center_x = int(screen_width / 2 - window_width / 2)
        # center_y = int(screen_height / 2 - window_height / 2)
        #
        # icon = PhotoImage(os.getcwd() + '\\car.ico\\')
        # root.iconbitmap(default=icon)
        #
        # # set the position of the window to the center of the screen
        # self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        # self.root.resizable(False, False)
        # Call the tkinter frame to the window
        self.loginControlFrame()

    """Login Frame"""

    def loginControlFrame(self):
        # Sign in frame
        self.signin = customtkinter.CTkFrame(self.root, width=400)
        self.signin.pack(fill='both', side=LEFT)

        # email
        email_label = customtkinter.CTkLabel(self.signin, text="Employee ID:", corner_radius=8, width=200,
                                             text_color=('black', 'silver'))
        email_label.pack(padx=10, pady=(40, 1), anchor='n')

        email_entry = customtkinter.CTkEntry(self.signin, placeholder_text="Enter your Employee ID", corner_radius=8,
                                             width=300)
        email_entry.pack(padx=20, pady=(1, 20), anchor='w')
        email_entry.focus()

        # password
        password_label = customtkinter.CTkLabel(self.signin, text="Password:", corner_radius=8, width=200,
                                                text_color=('black', 'silver'))
        password_label.pack(padx=10, pady=1, anchor='n')

        password_entry = customtkinter.CTkEntry(self.signin, show="*", corner_radius=8,
                                                placeholder_text="Enter your password", width=300)
        password_entry.pack(padx=20, pady=(1, 20), anchor='w')

        # msg
        msg_label = customtkinter.CTkLabel(self.signin, text=None, text_color="red", width=200)
        msg_label.pack(padx=40, pady=20, anchor='n')

        # Login function that will check user and password and login user if credentials are correct
        def login():
            # getting form data
            uname = email_entry.get()
            pwd = password_entry.get()
            # applying empty validation
            if uname == '' or pwd == '':
                msg_label.configure(self.signin, text="Fill the empty field!")
            else:
                if database.login(uname, pwd):
                    # Closing two frames we had opened
                    self.signin.destroy()
                    self.title_frame.destroy()
                    # Call main screen
                    clients.Clients(self.root)
                try:
                    msg_label.configure(self.signin, text="Wrong username or password!")
                except tkinter.TclError:
                    pass

        # login button
        signin_button = customtkinter.CTkButton(self.signin, text="Log in", corner_radius=8, command=login,
                                                fg_color="#556b2f", width=300)
        signin_button.pack(padx=20, pady=10, anchor='w')

        self.title_frame = customtkinter.CTkFrame(self.root, width=400)
        self.title_frame.pack(side=RIGHT, fill='both', expand=True)

        rent_label = customtkinter.CTkLabel(self.title_frame, text='RENT A CAR', font=('Stencil', 15),
                                             text_color='#C5B358')

        rent_label.pack(anchor=tkinter.CENTER, pady=(100, 1))

        brand_label = customtkinter.CTkLabel(self.title_frame, text='DREAM RIDE', font=('Broadway', 55),
                                             text_color='#CFB53B')
        brand_label.pack(anchor=tkinter.CENTER, pady=2)

        slogan_label = customtkinter.CTkLabel(self.title_frame, text='ENJOY YOUR HOLIDAYS WITH OUR WHEELS', font=('Perpetua', 15),
                                             text_color='#D2691E')
        slogan_label.pack(anchor=tkinter.CENTER, pady=2)
