import customtkinter
from tkinter import *
from CTkMessagebox import CTkMessagebox
import main2

# Set appearance and theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

# Create main window
app = customtkinter.CTk()
app.geometry("1000x600")
app.title("Time Management System")

# Load data from CSV files
main2.load_users_from_csv()
main2.load_tasks_from_csv()

# Track the current user
current_user = None

# Function to clear the window
def clear_window():
    """Remove all widgets from the main window."""
    for widget in app.winfo_children():
        widget.destroy()

# Login frame
def show_login_frame():
    """Display the login frame with username, password fields, and buttons."""
    clear_window()
    frame = customtkinter.CTkFrame(master=app, width=350, height=250, corner_radius=10)
    frame.pack(padx=20, pady=20)
    
    # Username entry
    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=200, height=30, corner_radius=10)
    username_entry.place(relx=0.5, rely=0.2, anchor=CENTER)
    
    # Password entry
    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", width=200, height=30, show="*", corner_radius=10)
    password_entry.place(relx=0.5, rely=0.4, anchor=CENTER)
    
    # Login button
    login_button = customtkinter.CTkButton(master=frame, text="Login", width=100, height=30, corner_radius=10, 
                                          command=lambda: select_user(username_entry.get(), password_entry.get()))
    login_button.place(relx=0.35, rely=0.6, anchor=CENTER)
    
    # Register button
    register_button = customtkinter.CTkButton(master=frame, text="Register", width=100, height=30, corner_radius=10, 
                                             command=lambda: create_new_user(username_entry.get(), password_entry.get()))
    register_button.place(relx=0.65, rely=0.6, anchor=CENTER)
    
    # Appearance mode switch
    switch_var = customtkinter.StringVar(value="off")
    switch_1 = customtkinter.CTkSwitch(master=app, text="Display Mode", 
                                       command=lambda: customtkinter.set_appearance_mode("dark" if switch_var.get() == "on" else "light"), 
                                       variable=switch_var, onvalue="on", offvalue="off")
    switch_1.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

# Handle login
def select_user(username, password):
    """Attempt to log in the user and switch to main menu on success."""
    global current_user
    success, msg = main2.login_user(username, password)
    if success:
        current_user = username
        CTkMessagebox(title="Success", message=f"Welcome, {current_user}!", icon="check")
        show_main_menu()
    else:
        CTkMessagebox(title="Error", message=msg, icon="cancel")

# Handle registration
def create_new_user(username, password):
    """Attempt to register a new user and display the result."""
    success, msg = main2.create_user(username, password)
    CTkMessagebox(title="Registration", message=msg, icon="check" if success else "cancel")

# Main menu
def show_main_menu():
    """Display the main menu with options for the user."""
    try:
        clear_window()
        main_frame = customtkinter.CTkFrame(master=app, width=350, height=300, corner_radius=10)
        main_frame.pack(padx=20, pady=20)
        
        # Buttons for various actions
        free_time_button = customtkinter.CTkButton(master=main_frame, text="Set Free Time", command=show_set_free_time_frame)
        free_time_button.pack(pady=10)
        
        add_task_button = customtkinter.CTkButton(master=main_frame, text="Add Task", command=show_add_task_frame)
        add_task_button.pack(pady=10)
        
        edit_task_button = customtkinter.CTkButton(master=main_frame, text="Edit Task", command=show_edit_task_frame)
        edit_task_button.pack(pady=10)
        
        delete_task_button = customtkinter.CTkButton(master=main_frame, text="Delete Task", command=show_delete_task_frame)
        delete_task_button.pack(pady=10)
        
        logout_button = customtkinter.CTkButton(master=main_frame, text="Logout", command=logout)
        logout_button.pack(pady=10)
    except Exception as e:
        print(f"Error in show_main_menu: {e}")
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")

# Placeholder functions for main menu options
def show_set_free_time_frame():
    """Placeholder for setting free time functionality."""
    CTkMessagebox(title="Info", message="Set Free Time functionality not implemented yet.", icon="info")

def show_add_task_frame():
    """Placeholder for adding task functionality."""
    CTkMessagebox(title="Info", message="Add Task functionality not implemented yet.", icon="info")

def show_edit_task_frame():
    """Placeholder for editing task functionality."""
    CTkMessagebox(title="Info", message="Edit Task functionality not implemented yet.", icon="info")

def show_delete_task_frame():
    """Placeholder for deleting task functionality."""
    CTkMessagebox(title="Info", message="Delete Task functionality not implemented yet.", icon="info")

# Logout function
def logout():
    """Save data, clear current user, and return to login frame."""
    main2.save_users_to_csv()
    main2.save_tasks_to_csv()
    global current_user
    current_user = None
    CTkMessagebox(title="Logout", message="You have been logged out.", icon="check")
    show_login_frame()

# Start the application with the login frame
show_login_frame()
app.mainloop()