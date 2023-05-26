import tkinter as tk
from tkinter import messagebox

from DSFactory import Factory
from Users import User

factory = Factory()


# Function to handle the login process
def load_Factory():
    return Factory()  # Lectura de factory serializado


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username exists in the HashMap
    if factory.contains_user(username):
        # Retrieve the user object associated with the username
        user = factory.get_user(username)

        # Check if the entered password matches the stored password
        if password == user.password:
            if user.is_admin:
                messagebox.showinfo("Success", "Admin login successful!")
            else:
                messagebox.showinfo("Success", "User login successful!")
        else:
            messagebox.showerror("Error", "Invalid password!")
    else:
        messagebox.showerror("Error", "Invalid username!")


# Function to handle the registration process
def register():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username is already taken
    if factory.contains_user(username):
        messagebox.showerror("Error", "Username already taken!")
    else:
        # Add the new user to the HashMap
        factory.add_user(User(username, password))
        messagebox.showinfo("Success", "Registration successful!")


# Create the login window
window = tk.Tk()
window.title("Login")

# Username label and entry field
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack(fill=tk.X, padx=10, pady=5)

# Password label and entry field
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack(fill=tk.X, padx=10, pady=5)

# Login button
login_button = tk.Button(window, text="Login", command=login)
login_button.pack(fill=tk.X, padx=10, pady=5)

# Register button
register_button = tk.Button(window, text="Register", command=register)
register_button.pack(fill=tk.X, padx=10, pady=5)

# Update window to calculate its size
window.update_idletasks()

# Calculate the center position of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = window.winfo_width()
window_height = window.winfo_height()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the window position
window.geometry(f"+{x}+{y}")

# Start the main window loop
window.mainloop()
