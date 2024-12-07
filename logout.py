from tkinter import messagebox

def logout(root, callback=None):
    if hasattr(root, 'current_user_email'):
        delattr(root, 'current_user_email')
        delattr(root, 'current_user_file_path')
        if callback:
            callback()
        return True
    else:
        messagebox.showerror("Error", "No user is currently logged in.")
        return False
