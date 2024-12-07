import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import json
from login import LoginPage
from profile_window import ProfileWindow
from button import create_buttons
from surveillance import start_surveillance, stop_surveillance, save_output_folder
from permission import open_permission_window
from import_data import open_import_window
from face_recognition import open_video_file  # Import the function to open video files

# Define the path to the user data file
user_data_file = 'user_data.json'

# Ensure the user data file exists
if not os.path.exists(user_data_file):
    with open(user_data_file, 'w') as f:
        json.dump({}, f)  # Create an empty dictionary as the initial data

def on_resize(event):
    line_canvas.config(width=event.width)

def load_and_process_image(image_path, size, remove_color=(0, 0, 0)):
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"Image file {image_path} not found.")
        return None

    image = Image.open(image_path).resize(size, Image.BILINEAR).convert("RGBA")
    data = image.getdata()
    new_data = [(0, 0, 0, 0) if item[:3] == remove_color else item for item in data]
    image.putdata(new_data)
    return ImageTk.PhotoImage(image)

def is_logged_in():
    return hasattr(root, 'current_user_email')

def check_login():
    if not is_logged_in():
        LoginPage(root)

def button_click(option):
    if not is_logged_in():
        tk.messagebox.showwarning("Warning", "You are not logged in")
    else:
        if option == "Surveillance":
            start_surveillance_handler()
        elif option == "Import_Data":
            open_import_window(root)  # Call the import data function
        elif option == "Face\nRecognition":  # Adjust for the correct button text
            open_video_file(root)  # Call the function to open and play video files
        else:
            print(option)  # Placeholder for other button actions

def start_surveillance_handler():
    if hasattr(root, 'current_user_email') and hasattr(root, 'current_user_file_path'):
        try:
            with open(root.current_user_file_path, 'r') as file:
                user_data = json.load(file)
                print(f"User data: {user_data}")  # Debug statement
                if user_data['email'] == root.current_user_email:
                    if user_data.get('permission') == 'yes':
                        if 'save_path' in user_data:
                            save_path = user_data['save_path']
                            print(f"Save path: {save_path}")  # Debug statement
                            # Check if save_path exists and has write permission
                            if os.path.exists(save_path):
                                if os.access(save_path, os.W_OK):
                                    start_surveillance(root, root.current_user_file_path, root.current_user_email, 4)
                                else:
                                    messagebox.showerror("Error", f"Permission denied: Check folder permissions for {save_path}")
                            else:
                                messagebox.showerror("Error", f"Save path '{save_path}' does not exist.")
                        else:
                            save_path = filedialog.askdirectory(title="Select Folder for Recordings")
                            if save_path:
                                save_output_folder(root.current_user_file_path, save_path, root.current_user_email)
                                start_surveillance(root, root.current_user_file_path, root.current_user_email, 4)
                    else:
                        messagebox.showerror("Error", "Please allow both permissions.")
                        open_permission_window(root, root.current_user_file_path)
                else:
                    messagebox.showerror("Error", "User email does not match the logged-in user.")
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error decoding JSON: {str(e)}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {root.current_user_file_path} not found.")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied: Check folder permissions.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "User is not logged in or file path is missing.")

# Create main GUI window
root = tk.Tk()
root.title("Surveillance System")

# Ensure icon file exists before setting it
icon_path = "./img/my_logo.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    messagebox.showerror("Error", f"Icon file {icon_path} not found.")

root.geometry("600x400")

# Create a frame to hold the images
frame = tk.Frame(root)
frame.pack(anchor="nw", padx=10, pady=10)

# Load and display the logo image
logo_path = "./img/logo.png"
logo_photo = load_and_process_image(logo_path, (50, 50))
if logo_photo:
    logo_label = tk.Label(frame, image=logo_photo)
    logo_label.logo_photo = logo_photo
    logo_label.grid(row=0, column=0, padx=(10, 0))

profile_options = ["Personal Information", "Account Management", "Feedback", "logout"]
profile_window = ProfileWindow(frame, "./img/profile.png", profile_options, check_login)

footer_label = tk.Label(root, bg="orange", fg="black", font=("Arial", 14))
footer_label.pack(side="bottom", fill="x")

line_canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=2, bg="white", highlightthickness=0)
line_canvas.place(x=0, y=60)

create_buttons(root, button_click)

root.update_idletasks()  # Update the GUI

root.after(100, lambda: LoginPage(root))

root.mainloop()
