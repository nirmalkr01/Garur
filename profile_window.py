import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import os

def change_to_hand_cursor(event):
    # Change the cursor to a hand cursor when hovering over the button
    event.widget.config(cursor="hand2")

class ProfileWindow:
    def __init__(self, parent, image_path, menu_options, check_login_callback):
        self.parent = parent
        self.image_path = image_path
        self.menu_options = menu_options
        self.check_login_callback = check_login_callback
        self.menu_open = False  # Flag to track menu state

        # Load the profile image
        self.profile_photo = self.load_image(image_path, (50, 30))

        # Create a label with the profile image
        self.profile_label = tk.Label(parent, image=self.profile_photo)
        self.profile_label.grid(row=0, column=1, padx=(1200, 0), sticky="e")  # Adjusted column position
        self.profile_label.bind("<Button-1>", self.toggle_menu)  # Bind left click event to toggle menu
        self.profile_label.bind("<Enter>", change_to_hand_cursor)

        # Create the menu frame (initially hidden)
        self.menu_frame = tk.Frame(parent, relief="raised", bd=2)
        self.menu_frame.grid(row=1, column=1, pady=(10, 0), sticky="e")  # Align with the profile label
        self.menu_frame.grid_remove()

        # Add options to the menu frame
        self.option_labels = {}
        for i, option in enumerate(self.menu_options):
            button = tk.Button(self.menu_frame, text=option, command=lambda o=option: self.update_menu_options(o))
            button.grid(row=i+1, column=0, sticky="we")
            self.option_labels[option] = button

    def load_image(self, image_path, size):
        image = Image.open(image_path).resize(size, Image.BILINEAR).convert("RGBA")
        return ImageTk.PhotoImage(image)

    def toggle_menu(self, event=None):
        self.check_login_callback()  # Check if the user is logged in
        if self.menu_open:
            self.menu_frame.grid_remove()
            self.menu_open = False
        else:
            # Clear all widgets from the menu frame and re-add the main menu options
            self.back_to_main_menu()

            # Get the coordinates of the profile label
            x = self.profile_label.winfo_rootx()  # X coordinate
            y = self.profile_label.winfo_rooty() + self.profile_label.winfo_height()  # Y coordinate

            # Place the menu frame just below the profile label
            self.menu_frame.place(x=x, y=y)
            self.menu_frame.lift()  # Ensure menu is on top
            self.menu_frame.focus_set()  # Set focus to the menu
            self.menu_frame.grid()  # Show the menu
            self.menu_open = True

    def update_menu_options(self, selected_option):
        if selected_option == "Personal Information":
            email = self.parent.master.current_user_email
            file_path = self.parent.master.current_user_file_path

            # Clear existing options
            for label in self.option_labels.values():
                label.destroy()

            # Add new options for personal information
            personal_info_options = ["Full Name", "Email Address", "Contact Number", "Address"]
            for i, option in enumerate(personal_info_options):
                label = tk.Label(self.menu_frame, text=option)
                label.grid(row=i+1, column=0, sticky="w")
                self.option_labels[option] = label

            # Add entry fields for Full Name, Email Address, Contact Number, Address
            self.full_name_entry = tk.Entry(self.menu_frame)
            self.full_name_entry.grid(row=1, column=1, sticky="w")

            self.email_entry = tk.Entry(self.menu_frame)
            self.email_entry.grid(row=2, column=1, sticky="w")
            self.email_entry.insert(0, email)
            self.email_entry.config(state="readonly")  # Make email entry read-only

            # Create a frame to contain both the country code dropdown and the contact entry
            contact_frame = tk.Frame(self.menu_frame)
            contact_frame.grid(row=3, column=1, columnspan=1, sticky="w")

            # Create the country code dropdown
            self.country_code_var = tk.StringVar(contact_frame)
            self.country_code_var.set("Select Country Code")
            country_codes = ["Afghanistan - +93", "Albania - +355", "Algeria - +213", "Andorra - +376", "Angola - +244",
                            "Argentina - +54", "Armenia - +374", "Australia - +61", "Austria - +43", "Azerbaijan - +994",
                            "Bahamas - +1", "Bahrain - +973", "Bangladesh - +880", "Barbados - +1", "Belarus - +375",
                            "Belgium - +32", "Belize - +501", "Benin - +229", "Bhutan - +975", "Bolivia - +591",
                            "Bosnia and Herzegovina - +387", "Botswana - +267", "Brazil - +55", "Brunei - +673",
                            "Bulgaria - +359", "Burkina Faso - +226", "Burundi - +257", "Cambodia - +855", "Cameroon - +237",
                            "Canada - +1", "Cape Verde - +238", "Central African Republic - +236", "Chad - +235", "Chile - +56",
                            "China - +86", "Colombia - +57", "Comoros - +269", "Congo (Brazzaville) - +242",
                            "Congo (Kinshasa) - +243", "Costa Rica - +506", "Croatia - +385", "Cuba - +53", "Cyprus - +357",
                            "Czech Republic - +420", "Denmark - +45", "Djibouti - +253", "Dominica - +1", "Dominican Republic - +1",
                            "East Timor (Timor-Leste) - +670", "Ecuador - +593", "Egypt - +20", "El Salvador - +503",
                            "Equatorial Guinea - +240", "Eritrea - +291", "Estonia - +372", "Ethiopia - +251", "Fiji - +679",
                            "Finland - +358", "France - +33", "Gabon - +241", "Gambia - +220", "Georgia - +995", "Germany - +49",
                            "Ghana - +233", "Greece - +30", "Grenada - +1", "Guatemala - +502", "Guinea - +224",
                            "Guinea-Bissau - +245", "Guyana - +592", "Haiti - +509", "Honduras - +504", "Hungary - +36",
                            "Iceland - +354", "India - +91", "Indonesia - +62", "Iran - +98", "Iraq - +964", "Ireland - +353",
                            "Israel - +972", "Italy - +39", "Ivory Coast - +225", "Jamaica - +1", "Japan - +81", "Jordan - +962",
                            "Kazakhstan - +7", "Kenya - +254", "Kiribati - +686", "Korea, North - +850", "Korea, South - +82",
                            "Kosovo - +383", "Kuwait - +965", "Kyrgyzstan - +996", "Laos - +856", "Latvia - +371",
                            "Lebanon - +961", "Lesotho - +266", "Liberia - +231", "Libya - +218", "Liechtenstein - +423",
                            "Lithuania - +370", "Luxembourg - +352", "Macedonia - +389", "Madagascar - +261", "Malawi - +265",
                            "Malaysia - +60", "Maldives - +960", "Mali - +223", "Malta - +356", "Marshall Islands - +692",
                            "Mauritania - +222", "Mauritius - +230", "Mexico - +52", "Micronesia - +691", "Moldova - +373",
                            "Monaco - +377", "Mongolia - +976", "Montenegro - +382", "Morocco - +212", "Mozambique - +258",
                            "Myanmar (Burma) - +95", "Namibia - +264", "Nauru - +674", "Nepal - +977", "Netherlands - +31",
                            "New Zealand - +64", "Nicaragua - +505", "Niger - +227", "Nigeria - +234", "Norway - +47", "Oman - +968",
                            "Pakistan - +92", "Palau - +680", "Panama - +507", "Papua New Guinea - +675", "Paraguay - +595",
                            "Peru - +51", "Philippines - +63", "Poland - +48", "Portugal - +351", "Qatar - +974", "Romania - +40",
                            "Russia - +7", "Rwanda - +250", "Saint Kitts and Nevis - +1", "Saint Lucia - +1",
                            "Saint Vincent and the Grenadines - +1", "Samoa - +685", "San Marino - +378", "Sao Tome and Principe - +239",
                            "Saudi Arabia - +966", "Senegal - +221", "Serbia - +381", "Seychelles - +248", "Sierra Leone - +232",
                            "Singapore - +65", "Slovakia - +421", "Slovenia - +386", "Solomon Islands - +677", "Somalia - +252",
                            "South Africa - +27", "South Sudan - +211", "Spain - +34", "Sri Lanka - +94", "Sudan - +249",
                            "Suriname - +597", "Swaziland - +268", "Sweden - +46", "Switzerland - +41", "Syria - +963",
                            "Taiwan - +886", "Tajikistan - +992", "Tanzania - +255", "Thailand - +66", "Togo - +228",
                            "Tonga - +676", "Trinidad and Tobago - +1", "Tunisia - +216", "Turkey - +90", "Turkmenistan - +993",
                            "Tuvalu - +688", "Uganda - +256", "Ukraine - +380", "United Arab Emirates - +971", "United Kingdom - +44",
                            "United States - +1", "Uruguay - +598", "Uzbekistan - +998", "Vanuatu - +678", "Vatican City - +39",
                            "Venezuela - +58", "Vietnam - +84", "Yemen - +967", "Zambia - +260", "Zimbabwe - +263"]
            country_code_menu = tk.OptionMenu(contact_frame, self.country_code_var, *country_codes)
            country_code_menu.grid(row=0, column=0, sticky="w")

            self.contact_number_entry = tk.Entry(contact_frame)
            self.contact_number_entry.grid(row=0, column=1, sticky="w", padx=(5, 0))
            self.contact_number_entry.config(validate="key", validatecommand=(self.parent.register(self.validate_contact), "%P"))

            self.address_entry = tk.Entry(self.menu_frame)
            self.address_entry.grid(row=4, column=1, columnspan=2, sticky="w")

            # Load existing user information if available
            if os.path.exists(file_path):
                with open(file_path, "r") as user_file:
                    user_data = json.load(user_file)
                    self.full_name_entry.insert(0, user_data.get("name", ""))
                    self.country_code_var.set(user_data.get("country_code", " "))
                    self.contact_number_entry.insert(0, user_data.get("contact", ""))
                    self.address_entry.insert(0, user_data.get("address", ""))

            # Add Submit and Back buttons
            self.submit_button = tk.Button(self.menu_frame, text="Submit", command=self.submit_personal_info_and_close_menu)
            self.submit_button.grid(row=5, column=0, pady=(10, 0), sticky="w")

            self.back_button = tk.Button(self.menu_frame, text="Back", command=self.back_to_main_menu)
            self.back_button.grid(row=5, column=1, pady=(14, 0), sticky="e")
        
        elif selected_option == "Account Management":
            # Clear existing options
            for label in self.option_labels.values():
                label.destroy()

            # Add new options for manage account
            manage_account_options = ["Save Path", "Delete Account"]
            for i, option in enumerate(manage_account_options):
                label = tk.Label(self.menu_frame, text=option)
                label.grid(row=i+1, column=0, sticky="w")
                self.option_labels[option] = label

            self.save_path_button = tk.Button(self.menu_frame, text="Save Path", command=self.change_save_path)
            self.save_path_button.grid(row=1, column=1, sticky="w")

            self.delete_account_button = tk.Button(self.menu_frame, text="Delete Account", command=self.delete_account)
            self.delete_account_button.grid(row=2, column=1, sticky="w")

            # Add Back button
            self.back_button = tk.Button(self.menu_frame, text="Back", command=self.back_to_main_menu)
            self.back_button.grid(row=3, column=1, pady=(14, 0), sticky="e")

    def validate_contact(self, value):
        # Validation function to allow only digits in the contact number entry
        if value.isdigit() or value == "":
            return True
        else:
            return False

    def submit_personal_info_and_close_menu(self):
        self.submit_personal_info()  # Submit personal info
        self.toggle_menu()  # Close the menu

    def submit_personal_info(self):
        email = self.parent.master.current_user_email
        file_path = self.parent.master.current_user_file_path

        name = self.full_name_entry.get()
        country_code = self.country_code_var.get().split(" - ")[-1]
        contact_number = self.contact_number_entry.get()
        address = self.address_entry.get()

        # Load existing user information if available
        user_data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as user_file:
                user_data = json.load(user_file)

        # Update only the relevant fields in the user data
        user_data.update({
            "email": email,
            "name": name,
            "country_code": country_code,
            "contact": contact_number,
            "address": address
        })

        # Save updated user information to JSON file
        with open(file_path, "w") as user_file:
            json.dump(user_data, user_file)

        messagebox.showinfo("Success", "Personal information updated successfully!")

    def back_to_main_menu(self):
        # Clear all widgets from the menu frame
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Re-add the main menu options
        self.option_labels = {}
        for i, option in enumerate(self.menu_options):
            button = tk.Button(self.menu_frame, text=option, command=lambda o=option: self.update_menu_options(o))
            button.grid(row=i+1, column=0, sticky="we")
            self.option_labels[option] = button

    def change_save_path(self):
        # Function to change the save path
        new_path = tk.filedialog.askdirectory()
        if new_path:
            # Get the JSON file path created at login
            file_path = self.parent.master.current_user_file_path
            # Load existing user information if available
            user_data = {}
            if os.path.exists(file_path):
                with open(file_path, "r") as user_file:
                    user_data = json.load(user_file)

            # Update the save path in user data
            user_data["save_path"] = new_path

            # Save updated user information to JSON file
            with open(file_path, "w") as user_file:
                json.dump(user_data, user_file)

            messagebox.showinfo("Success", f"Save path changed to {new_path}")

    def delete_account(self):
        # Function to delete the account
        email = self.parent.master.current_user_email
        file_path = self.parent.master.current_user_file_path

        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Success", "Account deleted successfully!")
            # Log out the user
            self.parent.master.current_user_email = None
            self.parent.master.current_user_file_path = None
            # Close the main window and show login window again
            self.parent.master.destroy()
            self.parent.master.__init__()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Profile Menu Example")

    # Placeholder callback function for checking login status
    def check_login():
        pass

    # Create an instance of ProfileWindow
    menu_options = ["Personal Information", "Manage Account"]
    profile_window = ProfileWindow(root, "profile.png", menu_options, check_login)

    root.mainloop()
