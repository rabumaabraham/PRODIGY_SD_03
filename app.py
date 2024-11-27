import tkinter as tk
from tkinter import messagebox, ttk
import os
import json


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")  # Light gray background

        # Data storage
        self.file_name = "contacts.json"
        self.contacts = self.load_contacts()

        # Header
        header = tk.Label(
            root,
            text="Contact Management System",
            font=("Arial", 18, "bold"),
            bg="#343a40",  # Dark gray
            fg="white",
            pady=10,
        )
        header.pack(fill=tk.X)

        # Buttons
        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Contact",
            font=("Arial", 12),
            bg="#20c997",  # Teal
            fg="white",
            width=15,
            command=self.add_contact_window,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="View Contacts",
            font=("Arial", 12),
            bg="#20c997",  # Teal
            fg="white",
            width=15,
            command=self.view_contacts_window,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Exit",
            font=("Arial", 12),
            bg="#dc3545",  # Red
            fg="white",
            width=15,
            command=root.quit,
        ).grid(row=0, column=2, padx=5)

        # Footer
        footer = tk.Label(
            root,
            text="Developed by Rabuma",
            font=("Arial", 10, "italic"),
            bg="#343a40",  # Dark gray
            fg="white",
            pady=10,
        )
        footer.pack(side=tk.BOTTOM, fill=tk.X)

    def load_contacts(self):
        """Load contacts from a file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file)
        return {}

    def save_contacts(self):
        """Save contacts to a file."""
        with open(self.file_name, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, name, phone, email):
        """Add a new contact."""
        if name in self.contacts:
            messagebox.showerror("Error", "Contact already exists!")
            return False
        self.contacts[name] = {"phone": phone, "email": email}
        self.save_contacts()
        return True

    def delete_contact(self, name):
        """Delete a contact."""
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()
            return True
        return False

    def edit_contact(self, name, phone, email):
        """Edit an existing contact."""
        if name in self.contacts:
            self.contacts[name] = {"phone": phone, "email": email}
            self.save_contacts()
            return True
        return False

    def add_contact_window(self):
        """Open the add contact window."""
        win = tk.Toplevel(self.root)
        win.title("Add Contact")
        win.geometry("400x300")
        win.resizable(False, False)
        win.config(bg="#f8f9fa")

        tk.Label(win, text="Name:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        name_entry = tk.Entry(win, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(win, text="Phone:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        phone_entry = tk.Entry(win, font=("Arial", 12))
        phone_entry.pack(pady=5)

        tk.Label(win, text="Email:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        email_entry = tk.Entry(win, font=("Arial", 12))
        email_entry.pack(pady=5)

        def save_new_contact():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            if name and phone and email:
                if self.add_contact(name, phone, email):
                    messagebox.showinfo("Success", "Contact added successfully!")
                    win.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add contact.")
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(
            win,
            text="Save Contact",
            font=("Arial", 12),
            bg="#20c997",  # Teal
            fg="white",
            command=save_new_contact,
        ).pack(pady=20)

    def view_contacts_window(self):
        """Open the view contacts window."""
        win = tk.Toplevel(self.root)
        win.title("Contact List")
        win.geometry("500x350")
        win.resizable(False, False)
        win.config(bg="#f8f9fa")

        # Table
        cols = ("Name", "Phone", "Email")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for name, details in self.contacts.items():
            tree.insert("", "end", values=(name, details["phone"], details["email"]))

        # Action Buttons
        btn_frame = tk.Frame(win, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        def delete_selected():
            selected_item = tree.selection()
            if selected_item:
                contact_name = tree.item(selected_item, "values")[0]
                if self.delete_contact(contact_name):
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", f"Deleted contact: {contact_name}")
                else:
                    messagebox.showerror("Error", "Failed to delete contact.")
            else:
                messagebox.showerror("Error", "No contact selected.")

        def edit_selected():
            selected_item = tree.selection()
            if selected_item:
                contact_name = tree.item(selected_item, "values")[0]
                details = self.contacts[contact_name]

                edit_win = tk.Toplevel(win)
                edit_win.title("Edit Contact")
                edit_win.geometry("400x300")
                edit_win.config(bg="#f8f9fa")

                tk.Label(edit_win, text="Name:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
                name_entry = tk.Entry(edit_win, font=("Arial", 12))
                name_entry.insert(0, contact_name)
                name_entry.pack(pady=5)

                tk.Label(edit_win, text="Phone:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
                phone_entry = tk.Entry(edit_win, font=("Arial", 12))
                phone_entry.insert(0, details["phone"])
                phone_entry.pack(pady=5)

                tk.Label(edit_win, text="Email:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
                email_entry = tk.Entry(edit_win, font=("Arial", 12))
                email_entry.insert(0, details["email"])
                email_entry.pack(pady=5)

                def save_edited_contact():
                    new_name = name_entry.get().strip()
                    new_phone = phone_entry.get().strip()
                    new_email = email_entry.get().strip()
                    if new_name and new_phone and new_email:
                        if self.edit_contact(new_name, new_phone, new_email):
                            tree.item(selected_item, values=(new_name, new_phone, new_email))
                            edit_win.destroy()
                            messagebox.showinfo("Success", "Contact updated successfully!")
                        else:
                            messagebox.showerror("Error", "Failed to edit contact.")
                    else:
                        messagebox.showerror("Error", "All fields are required!")

                tk.Button(
                    edit_win,
                    text="Save Changes",
                    font=("Arial", 12),
                    bg="#20c997",  # Teal
                    fg="white",
                    command=save_edited_contact,
                ).pack(pady=20)

        tk.Button(btn_frame, text="Delete Contact", font=("Arial", 12), bg="#dc3545", fg="white", command=delete_selected).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Contact", font=("Arial", 12), bg="#ffc107", fg="black", command=edit_selected).grid(row=0, column=1, padx=5)


# Run the GUI
root = tk.Tk()
app = ContactManager(root)
root.mainloop()
