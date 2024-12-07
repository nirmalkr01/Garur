import os
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image

def import_data(root):
    # Define the base directory where images will be saved
    base_dir = r"E:\-SINGH PRODUCTION_\sidhhi chemicals\project1_camera based\images"

    # Function to select an image file and save it
    def select_file_and_save():
        # Select an image file
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png"), ("JPEG files", "*.jpeg")])
        if file_path:
            try:
                # Open selected image using PIL
                image = Image.open(file_path)

                # Ask user for the image name to save
                image_name = simpledialog.askstring("Image Name", "Enter image name:")
                if image_name:
                    # Get the current user's email from root
                    if hasattr(root, 'current_user_email'):
                        current_email = root.current_user_email
                    else:
                        messagebox.showerror("Error", "User email not found.")
                        return

                    # Create the full path for the user's folder
                    user_folder_path = os.path.join(base_dir, current_email)

                    # Create the user's folder if it doesn't exist
                    if not os.path.exists(user_folder_path):
                        os.makedirs(user_folder_path)

                    # Save the image with the provided name in the user's folder
                    image_extension = os.path.splitext(file_path)[1]  # Get the original image extension
                    save_path = os.path.join(user_folder_path, f"{image_name}{image_extension}")
                    image.save(save_path)

                    messagebox.showinfo("Success", f"Image '{image_name}' saved in your folder.")

                else:
                    messagebox.showwarning("Warning", "No image name entered.")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

            # Enable the main window to be minimized again
            root.resizable(True, True)
        else:
            messagebox.showwarning("Warning", "No image file selected.")

    # Disable the minimize button of the main window temporarily
    root.resizable(False, True)

    # Open file dialog to select image and save
    select_file_and_save()

def open_import_window(root):
    import_data(root)
