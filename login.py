import os
import json
import re
from tkinter import Label, Entry, Button, messagebox, Toplevel
from permission import open_permission_window

class LoginPage:
    def __init__(self, root):
        self.root = Toplevel(root)  # Use Toplevel instead of Tk
        self.root.title("Login")
        self.root.geometry("300x100")

        # Set window icon
        self.root.iconbitmap("./img/my_logo.ico")

        # Fix the size of the window
        self.root.resizable(False, False)

        self.email_label = Label(self.root, text="Email:")
        self.email_label.grid(row=0, column=0, padx=10, pady=10)

        self.email_entry = Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        self.continue_button = Button(self.root, text="Continue", command=self.continue_login)
        self.continue_button.grid(row=1, columnspan=2, padx=10, pady=10)

    def continue_login(self):
        email = self.email_entry.get()

        # Validate email format
        if not re.match(r"^[a-zA-Z0-9_.+-]+@gmail+\.(com|org|net|edu|gov|co|info|biz|io|me)$", email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        # Save email to JSON file
        save_path = r"E:\-SINGH PRODUCTION_\sidhhi chemicals\project1_camera based\user_information"
        filename = f"{email}.json"
        file_path = os.path.join(save_path, filename)

        # Set current user email in the main root
        self.root.master.current_user_email = email
        self.root.master.current_user_file_path = file_path

        # Check if the user file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as user_file:
                user_data = json.load(user_file)

            # Check permission status
            if "permission" in user_data:
                if user_data["permission"] == "yes":
                    messagebox.showinfo("Success", f"Welcome back, {email}!")
                    self.root.destroy()  # Close the login page
                else:
                    open_permission_window(self.root, file_path, self.root)
            else:
                # If permission status is not specified, open permission window
                open_permission_window(self.root, file_path, self.root)
        else:
            # If file does not exist, create a placeholder JSON file and open permission window
            with open(file_path, "w") as new_user_file:
                json.dump({"email": email, "permission": "no"}, new_user_file)
            open_permission_window(self.root, file_path, self.root)
