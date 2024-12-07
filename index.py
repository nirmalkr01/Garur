# index.py
from tkinter import Tk
import gui_design
from surveillance import start_surveillance
from import_button import open_import_window
from profile_1 import Profile  # Add this import

# Create GUI
root = Tk()
root.title("Surveillance System")
root.geometry("600x400")

# Create Profile instance
profile_app = Profile(root)  # Add this line

# Assign commands to buttons
gui_design.btn_surveillance.config(command=start_surveillance)
gui_design.btn_import_data.config(command=open_import_window)
gui_design.set_profile_app(profile_app)  # Pass profile_app to gui_design

# Run the GUI
gui_design.root.mainloop()
