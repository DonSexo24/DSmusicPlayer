import pickle
import tkinter as tk
from tkinter import messagebox

from AdminView import AdminHome
from DSFactory import Factory
from Users import User
from UserView import HomePlayer


class LoginView:

    def __init__(self):
        self.factory = Factory()
        self.load_Factory()
        # Create the login window
        self.window = tk.Tk()
        self.window.title("Login")

        # Username label and entry field
        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(fill=tk.X, padx=20, pady=10)

        # Password label and entry field
        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(fill=tk.X, padx=20, pady=10)

        # Login button
        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack(fill=tk.X, padx=20, pady=10)

        # Register button
        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.register_button.pack(fill=tk.X, padx=20, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Update window to calculate its size
        self.window.update_idletasks()

        # Calculate the center position of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window position
        self.window.geometry(f"+{x}+{y}")

        # Start the main window loop
        self.window.mainloop()

    # Function to handle the login process
    def load_Factory(self):
        try:
            with open(r"C:\Users\Samuel\PycharmProjects\DSmusicPlayer\factory.pkl", "rb") as archivo:
                self.factory = pickle.load(archivo)
        except FileNotFoundError:
            print("El archivo no se encuentra.")
            self.save_Factory()
        except pickle.UnpicklingError:
            print("Error al deserializar el objeto.")
            self.save_Factory()

    def save_Factory(self):
        factory_aux = pickle.dumps(self.factory)
        with open(r"C:\Users\Samuel\PycharmProjects\DSmusicPlayer\factory.pkl", "wb") as archivo:
            archivo.write(factory_aux)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username exists in the HashMap
        if self.factory.contains_user(username):
            # Retrieve the user object associated with the username
            user = self.factory.get_user(username)

            # Check if the entered password matches the stored password
            if password == user.password:
                if user.is_admin:
                    messagebox.showinfo("Success", "Admin login successful!")
                    self.window.destroy()
                    #admin_home = AdminHome(factory=self.factory)
                else:
                    messagebox.showinfo("Success", "User login successful!")
                    self.window.destroy()
                    user_home = HomePlayer(factory=self.factory, user=user)
            else:
                messagebox.showerror("Error", "Invalid password!")
        else:
            messagebox.showerror("Error", "Invalid username!")

    # Function to handle the registration process
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username is already taken
        if self.factory.contains_user(username):
            messagebox.showerror("Error", "Username already taken!")
        else:
            # Add the new user to the HashMap
            self.factory.add_user(User(username, password))
            self.save_Factory()
            messagebox.showinfo("Success", "Registration successful!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "would you like to quit"):
            self.save_Factory()
            self.window.destroy()
