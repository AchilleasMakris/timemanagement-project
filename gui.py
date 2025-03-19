import customtkinter
from tkinter import *
from CTkMessagebox import CTkMessagebox
from main import *

# Set initial appearance mode to light
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

current_user = None

app = customtkinter.CTk()
app.geometry("1000x600")
app.title("Time Management System")

# Load users from CSV when the application starts
load_users_from_csv()  # Call the function to load users

# Function to clear the window for new frames
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


frame = customtkinter.CTkFrame(master=app, width=350, height=250, corner_radius=10)
frame.pack(padx=20, pady=20)


switch_var = customtkinter.StringVar(value="off")

def switch_event():
    if switch_var.get() == 'on':
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

switch_1 = customtkinter.CTkSwitch(master=app, text="Display Mode", command=switch_event, variable=switch_var, onvalue="on", offvalue="off")

# Place the switch on top right side.
switch_1.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)


username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=200, height=30, corner_radius=10)
username_entry.place(relx=0.5, rely=0.2, anchor=CENTER)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", width=200, height=30,show="*", corner_radius=10)
password_entry.place(relx=0.5, rely=0.4, anchor=CENTER)

# Place the Login button
login = customtkinter.CTkButton(master=frame,text="Login", width=100, height=30, corner_radius=10, command=select_user)
login.place(relx=0.35, rely=0.6, anchor=CENTER)

# Place the Register button next to the Login button
register = customtkinter.CTkButton(master=frame, text="Register", width=100, height=30, corner_radius=10, command=create_new_user)
register.place(relx=0.65, rely=0.6, anchor=CENTER)

def select_user():
    global current_user

    username = username_entry.get() 
    password = password_entry.get()
    
    # Check if the username exists and the password matches
    if username in users and users[username]["password"] == hash_password(password):
        current_user = username
        CTkMessagebox(title="Connected!", message=f"Welcome, {current_user}!", icon="check")
    else:
        CTkMessagebox(title="Error", message="Invalid username or password.", icon="cancel")

app.mainloop()