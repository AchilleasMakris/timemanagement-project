import customtkinter as ctk
import tkinter.messagebox as messagebox
from main3 import *  # Import all functions from main.py

# Set up CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Time Management")
root.geometry("800x600")

current_user = None  # Track the currently logged-in user

# Load initial data
load_users_from_csv()
load_activities_from_csv()

# Function to clear the window for new frames
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Login Frame
def show_login_frame():
    global current_user
    clear_window()

    # Title
    title_label = ctk.CTkLabel(root, text="Time Management - Login", font=("Arial", 20))
    title_label.pack(pady=20)

    # Username Entry
    username_label = ctk.CTkLabel(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = ctk.CTkEntry(root, width=200)
    username_entry.pack()

    # Password Entry
    password_label = ctk.CTkLabel(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(root, width=200, show="*")
    password_entry.pack()

    # Login Function
    def login():
        global current_user
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        user = next((u for u in users if u["username"] == username and u["password"] == hash_password(password)), None)
        if user:
            current_user = username
            messagebox.showinfo("Success", "Login successful.")
            show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

    # Register Function
    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if any(u["username"] == username for u in users):
            messagebox.showerror("Error", "User already exists.")
        else:
            password_hash = hash_password(password)
            new_user = {"username": username, "password": password_hash, "user_total_free_hours": 168.0}
            users.append(new_user)
            save_users_to_csv()
            messagebox.showinfo("Success", f"User {username} created successfully.")

    # Buttons
    login_button = ctk.CTkButton(root, text="Login", command=login)
    login_button.pack(pady=10)
    register_button = ctk.CTkButton(root, text="Register", command=register)
    register_button.pack(pady=10)

# Main Menu Frame
def show_main_menu():
    clear_window()
    title_label = ctk.CTkLabel(root, text=f"Welcome, {current_user}", font=("Arial", 20))
    title_label.pack(pady=20)

    options = [
        ("Manage Free Time", show_manage_free_time_frame),
        ("Add New Task", show_add_task_frame),
        ("Edit Task", show_edit_task_frame),
        ("Delete Task", show_delete_task_frame),
        ("Sort by Importance", lambda: show_sorted_activities_frame(current_user)),
        ("Show All Tasks", show_all_tasks_frame),
        ("Average Task Time", show_average_time_frame),
        ("Pie Chart", show_pie_chart_frame),
        ("Bar Chart", show_bar_chart_frame),
        ("Exit", root.quit)
    ]
    for text, command in options:
        button = ctk.CTkButton(root, text=text, command=command, width=200)
        button.pack(pady=10)

# Implemented Functions
def show_manage_free_time_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Manage Free Time", font=("Arial", 20))
    title_label.pack(pady=20)

    user = next(u for u in users if u["username"] == current_user)
    current_free_time = user["user_total_free_hours"]

    free_time_label = ctk.CTkLabel(root, text=f"Current Free Time: {current_free_time} hours")
    free_time_label.pack(pady=10)

    new_free_time_label = ctk.CTkLabel(root, text="Set New Free Time (hours):")
    new_free_time_label.pack(pady=5)
    new_free_time_entry = ctk.CTkEntry(root, width=200)
    new_free_time_entry.pack()

    def update_free_time():
        try:
            new_free_time = float(new_free_time_entry.get().strip())
            if new_free_time < 0:
                raise ValueError
            user["user_total_free_hours"] = new_free_time
            save_users_to_csv()
            messagebox.showinfo("Success", "Free time updated successfully.")
            show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a positive number.")

    update_button = ctk.CTkButton(root, text="Update", command=update_free_time)
    update_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back", command=show_main_menu)
    back_button.pack(pady=10)

def show_add_task_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Add New Task", font=("Arial", 20))
    title_label.pack(pady=20)

    # Entry fields
    name_label = ctk.CTkLabel(root, text="Task Name:")
    name_label.pack(pady=5)
    name_entry = ctk.CTkEntry(root, width=200)
    name_entry.pack()

    duration_label = ctk.CTkLabel(root, text="Duration (hours):")
    duration_label.pack(pady=5)
    duration_entry = ctk.CTkEntry(root, width=200)
    duration_entry.pack()

    importance_label = ctk.CTkLabel(root, text="Importance (1-5):")
    importance_label.pack(pady=5)
    importance_entry = ctk.CTkEntry(root, width=200)
    importance_entry.pack()

    type_label = ctk.CTkLabel(root, text="Type:")
    type_label.pack(pady=5)
    type_entry = ctk.CTkEntry(root, width=200)
    type_entry.pack()

    def add_task():
        name = name_entry.get().strip()
        duration = duration_entry.get().strip()
        importance = importance_entry.get().strip()
        task_type = type_entry.get().strip()
        if name and duration and importance and task_type:
            try:
                duration = float(duration)
                importance = int(importance)
                if importance < 1 or importance > 5:
                    raise ValueError
                new_task = {
                    "username": current_user,
                    "Δραστηριότητα": name,
                    "Διάρκεια": duration,
                    "Σημαντικότητα": importance,
                    "Τύπος": task_type
                }
                activities.append(new_task)
                save_activities_to_csv()
                messagebox.showinfo("Success", "Task added successfully.")
                show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Ensure duration is a number and importance is 1-5.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    add_button = ctk.CTkButton(root, text="Add Task", command=add_task)
    add_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back", command=show_main_menu)
    back_button.pack(pady=10)

def show_all_tasks_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="All Tasks", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        no_tasks_label = ctk.CTkLabel(root, text="No tasks found.")
        no_tasks_label.pack(pady=10)
    else:
        for task in user_tasks:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            task_label = ctk.CTkLabel(root, text=task_str)
            task_label.pack(pady=5)
    back_button = ctk.CTkButton(root, text="Back", command=show_main_menu)
    back_button.pack(pady=20)

def show_sorted_activities_frame(username):
    clear_window()
    title_label = ctk.CTkLabel(root, text="Tasks Sorted by Importance", font=("Arial", 20))
    title_label.pack(pady=20)
    user_activities = [a for a in activities if a["username"] == username]
    if not user_activities:
        no_tasks_label = ctk.CTkLabel(root, text="No tasks found.")
        no_tasks_label.pack(pady=10)
    else:
        sorted_activities = sorted(user_activities, key=lambda x: x["Σημαντικότητα"], reverse=True)
        for task in sorted_activities:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            task_label = ctk.CTkLabel(root, text=task_str)
            task_label.pack(pady=5)
    back_button = ctk.CTkButton(root, text="Back", command=show_main_menu)
    back_button.pack(pady=20)

# Placeholder Functions (to be fully implemented as needed)
def show_edit_task_frame():
    clear_window()
    ctk.CTkLabel(root, text="Edit Task - Not Implemented", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(root, text="Back", command=show_main_menu).pack(pady=20)

def show_delete_task_frame():
    clear_window()
    ctk.CTkLabel(root, text="Delete Task - Not Implemented", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(root, text="Back", command=show_main_menu).pack(pady=20)

def show_average_time_frame():
    clear_window()
    ctk.CTkLabel(root, text="Average Task Time - Not Implemented", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(root, text="Back", command=show_main_menu).pack(pady=20)

def show_pie_chart_frame():
    clear_window()
    ctk.CTkLabel(root, text="Pie Chart - Not Implemented", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(root, text="Back", command=show_main_menu).pack(pady=20)

def show_bar_chart_frame():
    clear_window()
    ctk.CTkLabel(root, text="Bar Chart - Not Implemented", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(root, text="Back", command=show_main_menu).pack(pady=20)

# Start the application
if __name__ == "__main__":
    show_login_frame()
    root.mainloop()