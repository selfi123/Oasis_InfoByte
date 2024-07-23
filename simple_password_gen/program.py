import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length=int(length_entry.get())
        if length<1:
            messagebox.showerror("Error", "Password length must be at least 1.")
            return
        uppercase=upp_var.get()
        digits=d_var.get()
        special=s_var.get()

        if not (uppercase or digits or special):
            messagebox.showerror("Select a character type! ")
            return

        letters=string.ascii_lowercase
        if uppercase:
            letters+=string.ascii_uppercase
        if digits:
            letters+=string.digits
        if special:
            letters+=string.punctuation

        password=''.join(random.choice(letters) for i in range(length))
        password_entry.delete(0,tk.END)
        password_entry.insert(0,password)
    except ValueError:
        messagebox.showerror("Error! , Enter a number !!")

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())

root=tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x300")

tk.Label(root,text="Password Length:").pack(pady=5)
length_entry=tk.Entry(root)
length_entry.pack(pady=5)

upp_var=tk.BooleanVar()
d_var=tk.BooleanVar()
s_var=tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase Letters", variable=upp_var).pack(pady=2)
tk.Checkbutton(root, text="Include Digits", variable=d_var).pack(pady=2)
tk.Checkbutton(root, text="Include Special Characters", variable=s_var).pack(pady=2)

generate_button=tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=20)

tk.Label(root,text="Generated Password:").pack(pady=5)
password_entry=tk.Entry(root, width=50)
password_entry.pack(pady=5)

copy_button=tk.Button(root,text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=20)

root.mainloop()
