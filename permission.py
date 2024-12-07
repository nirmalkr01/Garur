import json
from tkinter import Button, Checkbutton, IntVar, Toplevel, messagebox

def open_permission_window(root, file_path, login_window=None):
    print("Opening permission window...")
    
    # Create a pop-up window for permissions
    permission_window = Toplevel(root)
    permission_window.title("Permissions")
    permission_window.transient(root)  # Set as transient to the main window
    permission_window.grab_set()  # Grab focus so the user can't interact with the main window
    
    # Define IntVars to track checkbox states
    camera_var = IntVar(value=0)  # Default value set to 0 (no)
    storage_var = IntVar(value=0)  # Default value set to 0 (no)
    
    # Create checkboxes for camera and storage permissions
    camera_checkbox = Checkbutton(permission_window, text="Allow access to camera", variable=camera_var, onvalue=1, offvalue=0)
    storage_checkbox = Checkbutton(permission_window, text="Allow access to storage", variable=storage_var, onvalue=1, offvalue=0)
    
    camera_checkbox.pack()
    storage_checkbox.pack()
    
    def submit_permissions():
        print("Submitting permissions...")
        # Determine permission status based on checkbox selections
        camera_permission = "yes" if camera_var.get() == 1 else "no"
        storage_permission = "yes" if storage_var.get() == 1 else "no"
        
        # Read existing user data to preserve email
        with open(file_path, "r") as file:
            user_data = json.load(file)

        user_data.update({
            "camera_permission": camera_permission,
            "storage_permission": storage_permission,
            "permission": "yes" if camera_permission == "yes" and storage_permission == "yes" else "no"
        })
        
        # Save updated permission data to JSON file
        with open(file_path, "w") as file:
            json.dump(user_data, file)
        
        # Check if both permissions are granted
        if camera_permission == "yes" and storage_permission == "yes":
            messagebox.showinfo("Info", "Permissions granted. You may now proceed.")
            permission_window.destroy()  # Close permission window
            if login_window:
                login_window.destroy()  # Close login window if it exists
        else:
            messagebox.showwarning("Warning", "Both permissions are required to proceed.")
            permission_window.destroy()  # Close permission window
            if login_window:
                login_window.destroy()  # Close login window if it exists

    # Button to submit permissions
    submit_button = Button(permission_window, text="Submit", command=submit_permissions)
    submit_button.pack()
