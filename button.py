import tkinter as tk
from PIL import Image, ImageTk

def change_to_hand_cursor(event):
    # Change the cursor to a hand cursor when hovering over the button
    event.widget.config(cursor="hand2")

def create_buttons(root, button_click):
    # Load images
    image_paths = ["./img/video.png", "./img/photo.png", "./img/vehical.png", "./img/face.png", "./img/statical.png"]
    images = [ImageTk.PhotoImage(Image.open(path).resize((160, 100), Image.LANCZOS)) for path in image_paths]
    
    # Create and display buttons
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(anchor="nw", padx=10, pady=0)
    
    button_texts = ["Surveillance", "Import_Data", "Verify_Number_Plate", "Face\nRecognition", "Statistical\nRepresentation"]
    buttons = []

    num_buttons = len(button_texts)
    num_columns = 3  # Display three buttons in each horizontal line
    num_rows = (num_buttons + num_columns - 1) // num_columns

    padx_val = 160  # Distance between buttons

    for i, text in enumerate(button_texts):
        row = i // num_columns
        col = i % num_columns

        # Create a frame for each button with image and text
        box_frame = tk.Frame(buttons_frame, bg="white", bd=1, relief="solid")
        box_frame.grid(row=row, column=col, padx=padx_val, pady=70)
        box_frame.bind("<Enter>", change_to_hand_cursor)

        # Image button
        img_button = tk.Button(box_frame, image=images[i], command=lambda t=text: button_click(t),
                               relief='raised', borderwidth=0, bg="white")
        img_button.image = images[i]  # Keep a reference to avoid garbage collection
        img_button.pack(pady=(10, 0))

        # Text label
        text_label = tk.Label(box_frame, text=text, bg="white", font=("Georgia", 12))
        text_label.pack(pady=(5, 10))

        buttons.append(box_frame)

    # Add empty Label widgets to fill any remaining grid cells
    for i in range(num_buttons, num_rows * num_columns):
        row = i // num_columns
        col = i % num_columns
        empty_label = tk.Label(buttons_frame, text="", width=20)
        empty_label.grid(row=row, column=col, padx=padx_val, pady=10, sticky="nsew")

    # Positioning the menu frame to overlap the grid of buttons
    menu_frame = tk.Frame(root)
    menu_frame.place(x=10, y=0)  # Adjust x and y coordinates as needed
