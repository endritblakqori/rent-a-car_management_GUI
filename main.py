from tkinter import PhotoImage

import customtkinter
import login
import database
import os

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


def main():
    root = customtkinter.CTk()

    window_width = 800
    window_height = 400
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    icon = PhotoImage(os.getcwd() + '\\car.ico\\')
    root.iconbitmap(default=icon)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.title('Login - Dream Ride rent-a-car')
    root.resizable(False, False)

    database.init_database()
    login.Login(root)

    root.mainloop()


if __name__ == '__main__':
    main()
