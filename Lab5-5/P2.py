#Vorraluck Taladon
#683040740-0

import tkinter as tk
from tkinter import ttk, messagebox
from numpy import pad
from tkcalendar import DateEntry  # You'll need to install this: pip install tkcalendar
import re

class RegistrationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Registration")
        self.root.geometry("500x650")
        
        # Variables to store form data
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Prefer not to say")
        self.program_var = tk.StringVar(value="Computer Science")
        self.understand_var = tk.BooleanVar(value=False)
        self.dob_var = tk.StringVar()
        self.story_var = ""

        # Start with registration page
        self.current_frame = None
        self.show_registration_page()
        
    def clear_window(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_registration_page(self):
        # Clear all variables
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.gender_var.set("Prefer not to say")
        self.program_var.set("Computer Science")
        self.understand_var.set(False)
        self.dob_var.set("")
        self.comment_content = ""  # Clear saved comment content

        
        self.clear_window()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        
        # Title
        ttk.Label(
            self.current_frame,
            text="Student Registration Form",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        # Create form fields
        self.create_form_fields()

        # Clear the Text widget after it's created
        self.story_text.delete("1.0", "end")
    
    
    def create_form_fields(self):
        
        form_frame = ttk.Frame(self.current_frame)
        form_frame.pack(fill='x', pady=5)
        
        # Full Name
        ttk.Label(form_frame, text="Full Name:").pack(anchor='w', pady=(5,0))
        ttk.Entry(form_frame, textvariable=self.name_var).pack(fill='x', pady=2)

        # Email
        ttk.Label(form_frame, text="Email:").pack(anchor='w', pady=(5,0))
        ttk.Entry(form_frame, textvariable=self.email_var).pack(fill='x', pady=2)

        # Phone
        ttk.Label(form_frame, text="Phone:").pack(anchor='w', pady=(5,0))
        ttk.Entry(form_frame, textvariable=self.phone_var).pack(fill='x', pady=2)


        # Date of Birth
        # Calendar input
        ttk.Label(form_frame, text="Date of Birth:").pack(anchor='w', pady=(10,0))
        self.dob_entry = DateEntry(
            form_frame,
            width=20,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=2000,
            textvariable=self.dob_var
        )
        self.dob_entry.pack(anchor='w', pady=2)


        # Gender 
        ttk.Label(form_frame, text="Gender:").pack(anchor='w', pady=(10,0))
        gender_f = ttk.Frame(form_frame)
        gender_f.pack(fill='x')
        genders = ["Male", "Female", "Non-binary", "Prefer not to say"]
        for g in genders:
            ttk.Radiobutton(gender_f, text=g, value=g, variable=self.gender_var).pack(side='left', padx=5)

        # Program
        ttk.Label(form_frame, text="Program:").pack(anchor='w', pady=(10,0))
        self.prog_cb = ttk.Combobox(form_frame, values=["Engineering", "Computer science", "Business", "Arts", "Sciences","Chef", "Other"], 
                                   textvariable=self.program_var, state="readonly")
        self.prog_cb.pack(fill='x', pady=2)

        # Tell us a little bit about yourself 
        ttk.Label(form_frame, text="Tell us a little bit about yourself:").pack(anchor='w', pady=(10,0))
        self.story_text = tk.Text(form_frame, height=5)
        self.story_text.pack(fill='x', pady=2)

        # Accept Checkbox
        ttk.Checkbutton(form_frame, text="I accept the terms and conditions", 
                        variable=self.understand_var).pack(anchor='w', pady=10)

        # Submit Button
        ttk.Button(self.current_frame, text="Submit Registration", command=self.validate_and_submit).pack(pady=10)
    
    def validate_and_submit(self):
        # Basic validation
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter your name")
            return
        
        if not self.validate_email(self.email_var.get()):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if not self.validate_phone(self.phone_var.get()):
            messagebox.showerror("Error", "Please enter a valid phone number")
            return
        
        if not self.understand_var.get():
            messagebox.showerror("Error", "Please accept the terms and conditions.")
            return

        # save text in the comment box
        self.story_var = self.story_text.get("1.0", "end-1c")

        # If validation passes, show confirmation page
        self.show_confirmation_page()
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        pattern = r'^\d{9,10}$'
        return re.match(pattern, phone) is not None
    
    def show_confirmation_page(self):

        self.clear_window()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
        

        details = [
            ("Name:", self.name_var.get()),
            ("Email:", self.email_var.get()),
            ("Phone:", self.phone_var.get()),
            ("Date of Birth:", self.dob_var.get()),
            ("Gender:", self.gender_var.get()),
            ("Program:", self.program_var.get()),
            ("Your story:", self.story_var)
        ]

        for label, val in details:
            row = ttk.Frame(self.current_frame)
            row.pack(fill='x', pady=5)
            ttk.Label(row, text=label, font=("Helvetica", 10, "bold"), width=15).pack(side='left')
            ttk.Label(row, text=val, font=("Helvetica", 10)).pack(side='left')

        ttk.Button(self.current_frame, text="New Registration", command=self.show_registration_page).pack(pady=30)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RegistrationApp()
    app.run()