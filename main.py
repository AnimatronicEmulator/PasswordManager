from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_finder():
    website = website_entry.get().title()
    try:
        with open("password_doc.json", "r") as password_doc:
            data = json.load(password_doc)
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title=f"Entry for {website}", message=f"A password entry for {website} doesn't exist.")
    else:
        if website in data:
            username = data[website]["Username"]
            password = data[website]["Password"]
            messagebox.showinfo(title=f"Entry for {website}", message=f"{website}\nUsername: {username}\n"
                                                                      f"Password: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showerror(title=f"Entry for {website}", message=f"A password entry for {website} doesn't exist.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    password_list = []
    password_list.extend([random.choice(LETTERS) for _ in range(8)])
    password_list.extend([random.choice(NUMBERS) for _ in range(8)])
    password_list.extend([random.choice(SYMBOLS) for _ in range(8)])
    random.shuffle(password_list)
    randomized_password = ''.join(password_list)

    password_entry.insert(0, randomized_password)
    pyperclip.copy(randomized_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().title()
    username = email_username_entry.get()
    password = password_entry.get()

    new_entry = {website: {
        "Username": username,
        "Password": password,
    }}

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Invalid Entry", message="Please don't leave any fields empty!")

    else:
        try:
            with open("password_doc.json", "r") as password_doc:
                data = json.load(password_doc)
        except json.decoder.JSONDecodeError:
            with open("password_doc.json", "w") as password_doc:
                json.dump(new_entry, password_doc, indent=4)
        else:
            data.update(new_entry)
            with open("password_doc.json", "w") as password_doc:
                json.dump(data, password_doc, indent=4)
        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(bg="white", padx=50, pady=50)

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
padlock_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock_logo)
canvas.grid(row=0, column=0, columnspan=3)

website_label = Label(text="Website: ", bg="white")
website_label.grid(row=1, column=0, sticky="E")

website_entry = Entry(width=16, borderwidth=2, relief="sunken")
website_entry.grid(row=1, column=1, columnspan=1, sticky="W")
website_entry.focus()

search_button = Button(text="Search", command=password_finder, width=14, bg="white", borderwidth=1, relief="ridge")
search_button.grid(row=1, column=2, sticky="W")

email_username_label = Label(text="Email/Username: ", bg="white")
email_username_label.grid(row=2, column=0, sticky="E")

email_username_entry = Entry(width=35, borderwidth=2, relief="sunken")
email_username_entry.grid(row=2, column=1, columnspan=2, sticky="W")
email_username_entry.insert(0, "animatronic@protonmail.com")

password_label = Label(text="Password: ", bg="white")
password_label.grid(row=3, column=0, sticky="E")

password_entry = Entry(width=16, borderwidth=2, relief="sunken")
password_entry.grid(row=3, column=1, sticky="W")

generate_password_button = Button(text="Generate Password", command=password_generator,
                                  bg="white", borderwidth=1, relief="ridge")
generate_password_button.grid(row=3, column=2, sticky="W")

add_to_manager_button = Button(text="Add", command=save_password, width=29, bg="white", borderwidth=1, relief="ridge")
add_to_manager_button.grid(row=4, column=1, columnspan=2, sticky="SW", pady=4)

window.mainloop()
