import tkinter as tk
from json import JSONDecodeError
from tkinter import messagebox as mb
import random
import pyperclip as pc
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate():
    password_box.delete(0, tk.END)
    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    letters_list = [random.choice(letters) for x in range(nr_letters)]
    numbers_list = [random.choice(numbers) for x in range(nr_numbers)]
    symbols_list = [random.choice(symbols) for x in range(nr_symbols)]
    password = letters_list + numbers_list + symbols_list

    shuffled_list = random.sample(password, len(password))
    password_str = ''.join(shuffled_list)
    password_box.insert(0, password_str)

    # saving auto generated password to clipboard
    pc.copy(password_str)


# --------------------------------- SEARCH --------------------------------- #
def search():
    website_searched = website_box.get()
    with open('data.json') as data_file:
        data = json.load(data_file)
        try:
            email = data[website_searched.title()]['email']
            password = data[website_searched.title()]['password']
            mb.showinfo(message=f"Email: {email}\nPassword: {password}")
        except FileNotFoundError:
            mb.showerror(message='No Data File Found.')
        except KeyError as key:
            mb.showerror(message=f'No details for {key} exists.')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # retrieving new password entry
    website_input = website_box.get()
    email_input = email_username_box.get()
    password_input = password_box.get()
    new_data = {
        website_input: {
            'email': email_input,
            'password': password_input,
        }
    }
    # ensuring all fields are filled
    if len(website_input) == 0 or len(password_input) == 0:
        mb.showerror(message='Please do not leave any fields empty!')
    else:
        # give user confirmation
        to_save = mb.askokcancel(message=f'These are the details entered: \nWebsite: {website_input}'
                                         f'\nEmail: {email_input}\nPassword: {password_input}\nIs it okay to save?')
        if to_save:
            try:
                with open('data.json') as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open('data.json', mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            except JSONDecodeError:
                with open('data.json', mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open('data.json', mode='w') as data_file:
                    json.dump(data, data_file, indent=4)

            # clearing website and password text box
            website_box.delete(0, tk.END)
            password_box.delete(0, tk.END)
            website_box.focus()
            mb.showinfo(message='The generated password has been copied to your clipboard.')


# ---------------------------- UI SETUP ------------------------------- #
screen = tk.Tk()
screen.title('Password Manager')
screen.config(bg='white', pady=60, padx=60)

canvas = tk.Canvas(height=200, width=200, bg='white', highlightthickness=0)
logo = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(row=1, column=2)

# website text box
website_text = tk.Label(text='Website:', bg='white', fg='black')
website_text.grid(row=2, column=1)
website_box = tk.Entry(bg='white', fg='black', highlightthickness=0, insertbackground='black')
website_box.focus()
website_box.grid(row=2, column=2)

# search button
search_button = tk.Button(text='Search', highlightbackground='white', width=11, command=search)
search_button.grid(row=2, column=3)

# email/username text box
email_username = tk.Label(text='Email/Username:', bg='white', fg='black')
email_username.grid(row=3, column=1)
email_username_box = tk.Entry(bg='white', fg='black', highlightthickness=0, insertbackground='black', width=35,)
email_username_box.insert(0, '@gmail.com')
email_username_box.grid(row=3, column=2, columnspan=2)

# password text box
password_text = tk.Label(text='Password:', bg='white', fg='black')
password_text.grid(row=4, column=1)
password_box = tk.Entry(bg='white', fg='black', highlightthickness=0, insertbackground='black')
password_box.grid(row=4, column=2)

# generate password button
generate_button = tk.Button(text='Generate Password', highlightbackground='white', width=11, command=generate)
generate_button.grid(row=4, column=3)

# add button
add_button = tk.Button(text='Add', highlightbackground='white', width=33, command=save_password)
add_button.grid(row=5, column=2, columnspan=2)

tk.mainloop()
