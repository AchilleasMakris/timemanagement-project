import customtkinter as ctk
import tkinter.messagebox as messagebox
from main import (
    hash_password, manage_free_time, create_new_user, select_user, task_add, task_edit, 
    task_del, sort_by_importance, show_all, average_time, plot_pie_chart, plot_bar_chart,
    load_users_from_csv, load_tasks_from_csv, save_users_to_csv, save_tasks_to_csv, users
)
current_user = None  # Track the currently logged-in user


# Set up customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Time Management")
root.geometry("800x600")

current_user = None  # Track the currently logged-in user

# Load initial data
load_users_from_csv()
load_tasks_from_csv()


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
        if username in users and users[username]["password"] == hash_password(password):
            current_user = username
            messagebox.showinfo("Success", "Επιτυχής σύνδεση.")
            show_main_menu()
        else:
            messagebox.showerror("Error", "Λάθος όνομα χρήστη ή κωδικός.")

    # Register Function
    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username in users:
            messagebox.showerror("Error", "Ο χρήστης υπάρχει ήδη.")
        else:
            password_hash = hash_password(password)
            users[username] = {"password": password_hash, "tasks": [], "free_time": 168.0}
            save_users_to_csv()
            messagebox.showinfo("Success", f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς.")

    # Buttons
    login_button = ctk.CTkButton(root, text="Σύνδεση", command=login)
    login_button.pack(pady=10)
    register_button = ctk.CTkButton(root, text="Εγγραφή", command=register)
    register_button.pack(pady=10)

# Main Menu Frame
def show_main_menu():
    clear_window()

    # Title
    title_label = ctk.CTkLabel(root, text=f"Welcome, {current_user}", font=("Arial", 20))
    title_label.pack(pady=20)

    # Menu Buttons
    options = [
        ("Εισαγωγή/Ενημέρωση Ελεύθερου Χρόνου", show_manage_free_time_frame),
        ("Προσθήκη Νέου Στόχου", show_add_task_frame),
        ("Τροποποίηση Στόχου", show_edit_task_frame),
        ("Διαγραφή Στόχου", show_delete_task_frame),
        ("Ταξινόμηση κατά Σημαντικότητα", lambda: sort_by_importance(current_user)),
        ("Εμφάνιση Όλων των Στόχων", show_all_tasks_frame),
        ("Μέσος Όρος Χρόνου", show_average_time_frame),
        ("Γράφημα Πίτας", show_pie_chart_frame),
        ("Γράφημα Στηλών", show_bar_chart_frame),
        ("Έξοδος", root.quit)
    ]
    for text, command in options:
        button = ctk.CTkButton(root, text=text, command=command, width=200)
        button.pack(pady=10)

# Manage Free Time Frame
def show_manage_free_time_frame():
    clear_window()

    label = ctk.CTkLabel(root, text="Διαχείριση Ελεύθερου Χρόνου", font=("Arial", 16))
    label.pack(pady=20)

    free_time_entry = ctk.CTkEntry(root, placeholder_text="Εισάγετε ώρες (1-168)", width=200)
    free_time_entry.pack(pady=10)

    def save_free_time():
        try:
            free_time = float(free_time_entry.get())
            if 1 <= free_time <= 168:
                users[current_user]['free_time'] = free_time
                save_users_to_csv()
                messagebox.showinfo("Success", f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες.")
                show_main_menu()
            else:
                messagebox.showerror("Error", "Ο χρόνος πρέπει να είναι μεταξύ 1 και 168 ωρών.")
        except ValueError:
            messagebox.showerror("Error", "Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")

    save_button = ctk.CTkButton(root, text="Αποθήκευση", command=save_free_time)
    save_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Add Task Frame
def show_add_task_frame():
    clear_window()

    label = ctk.CTkLabel(root, text="Προσθήκη Νέου Στόχου", font=("Arial", 16))
    label.pack(pady=20)

    name_entry = ctk.CTkEntry(root, placeholder_text="Όνομα στόχου", width=200)
    name_entry.pack(pady=5)
    hours_entry = ctk.CTkEntry(root, placeholder_text="Ώρες (0-168)", width=200)
    hours_entry.pack(pady=5)
    importance_entry = ctk.CTkEntry(root, placeholder_text="Σημαντικότητα (1-10)", width=200)
    importance_entry.pack(pady=5)

    def add_task():
        name = name_entry.get().strip()
        try:
            hours = float(hours_entry.get())
            importance = int(importance_entry.get())
            tasks = users[current_user]['tasks']
            free_time = users[current_user]['free_time']
            current_total = sum(task['hours'] for task in tasks)
            if any(task['name'] == name for task in tasks):
                messagebox.showerror("Error", "Ο στόχος υπάρχει ήδη.")
            elif not name.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Το όνομα πρέπει να περιέχει μόνο γράμματα.")
            elif not (0 <= hours <= 168):
                messagebox.showerror("Error", "Οι ώρες πρέπει να είναι από 0 έως 168.")
            elif current_total + hours > free_time:
                messagebox.showerror("Error", f"Υπερβαίνετε τον ελεύθερο χρόνο ({free_time} ώρες).")
            elif not (1 <= importance <= 10):
                messagebox.showerror("Error", "Η σημαντικότητα πρέπει να είναι από 1 έως 10.")
            else:
                tasks.append({"name": name, "hours": hours, "importance": importance})
                save_tasks_to_csv()
                messagebox.showinfo("Success", f"Ο στόχος {name} προστέθηκε.")
                show_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Εισάγετε έγκυρους αριθμούς για ώρες και σημαντικότητα.")

    add_button = ctk.CTkButton(root, text="Προσθήκη", command=add_task)
    add_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Edit Task Frame
def show_edit_task_frame():
    clear_window()
    tasks = users[current_user]['tasks']
    if not tasks:
        messagebox.showinfo("Info", "Δεν υπάρχουν στόχοι για τροποποίηση.")
        show_main_menu()
        return

    label = ctk.CTkLabel(root, text="Τροποποίηση Στόχου", font=("Arial", 16))
    label.pack(pady=20)

    task_list = ctk.CTkTextbox(root, width=400, height=200)
    for i, task in enumerate(tasks):
        task_list.insert("end", f"{i + 1}. {task['name']} - {task['hours']} ώρες, Σημ: {task['importance']}\n")
    task_list.pack(pady=10)
    task_list.configure(state="disabled")

    index_entry = ctk.CTkEntry(root, placeholder_text="Αριθμός στόχου", width=200)
    index_entry.pack(pady=5)
    name_entry = ctk.CTkEntry(root, placeholder_text="Νέο όνομα", width=200)
    name_entry.pack(pady=5)
    hours_entry = ctk.CTkEntry(root, placeholder_text="Νέες ώρες", width=200)
    hours_entry.pack(pady=5)
    importance_entry = ctk.CTkEntry(root, placeholder_text="Νέα σημαντικότητα", width=200)
    importance_entry.pack(pady=5)

    def edit_task():
        try:
            index = int(index_entry.get()) - 1
            if 0 <= index < len(tasks):
                name = name_entry.get().strip()
                hours = float(hours_entry.get())
                importance = int(importance_entry.get())
                if name.replace(" ", "").isalpha() and 0 <= hours <= 168 and 1 <= importance <= 10:
                    tasks[index] = {"name": name, "hours": hours, "importance": importance}
                    save_tasks_to_csv()
                    messagebox.showinfo("Success", "Ο στόχος τροποποιήθηκε.")
                    show_main_menu()
                else:
                    messagebox.showerror("Error", "Ελέγξτε τα δεδομένα (όνομα: γράμματα, ώρες: 0-168, σημ: 1-10).")
            else:
                messagebox.showerror("Error", "Άκυρος αριθμός στόχου.")
        except ValueError:
            messagebox.showerror("Error", "Εισάγετε έγκυρους αριθμούς.")

    edit_button = ctk.CTkButton(root, text="Τροποποίηση", command=edit_task)
    edit_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Delete Task Frame
def show_delete_task_frame():
    clear_window()
    tasks = users[current_user]['tasks']
    if not tasks:
        messagebox.showinfo("Info", "Δεν υπάρχουν στόχοι για διαγραφή.")
        show_main_menu()
        return

    label = ctk.CTkLabel(root, text="Διαγραφή Στόχου", font=("Arial", 16))
    label.pack(pady=20)

    task_list = ctk.CTkTextbox(root, width=400, height=200)
    for i, task in enumerate(tasks):
        task_list.insert("end", f"{i + 1}. {task['name']} - {task['hours']} ώρες, Σημ: {task['importance']}\n")
    task_list.pack(pady=10)
    task_list.configure(state="disabled")

    index_entry = ctk.CTkEntry(root, placeholder_text="Αριθμός στόχου για διαγραφή", width=200)
    index_entry.pack(pady=5)

    def delete_task():
        try:
            index = int(index_entry.get()) - 1
            if 0 <= index < len(tasks):
                deleted_task = tasks.pop(index)
                save_tasks_to_csv()
                messagebox.showinfo("Success", f"Ο στόχος '{deleted_task['name']}' διαγράφηκε.")
                show_main_menu()
            else:
                messagebox.showerror("Error", "Άκυρος αριθμός στόχου.")
        except ValueError:
            messagebox.showerror("Error", "Εισάγετε έναν έγκυρο αριθμό.")

    delete_button = ctk.CTkButton(root, text="Διαγραφή", command=delete_task)
    delete_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Show All Tasks Frame
def show_all_tasks_frame():
    clear_window()
    tasks = users[current_user]['tasks']
    free_time = users[current_user]['free_time']

    label = ctk.CTkLabel(root, text="Όλοι οι Στόχοι", font=("Arial", 16))
    label.pack(pady=20)

    textbox = ctk.CTkTextbox(root, width=600, height=400)
    if not tasks:
        textbox.insert("end", "Δεν υπάρχουν στόχοι.\n")
    else:
        for i, task in enumerate(tasks):
            textbox.insert("end", f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, "
                                  f"Σημαντικότητα: {task['importance']}\n")
        total_task_hours = sum(task['hours'] for task in tasks)
        remaining_free_time = free_time - total_task_hours
        textbox.insert("end", f"\nΣυνολικός ελεύθερος χρόνος: {free_time} ώρες\n")
        textbox.insert("end", f"Ελεύθερος χρόνος που απομένει: {remaining_free_time} ώρες\n")
    textbox.pack(pady=10)
    textbox.configure(state="disabled")

    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Average Time Frame
def show_average_time_frame():
    clear_window()
    tasks = users[current_user]['tasks']

    label = ctk.CTkLabel(root, text="Μέσος Όρος Χρόνου", font=("Arial", 16))
    label.pack(pady=20)

    textbox = ctk.CTkTextbox(root, width=400, height=100)
    if not tasks:
        textbox.insert("end", "Δεν υπάρχουν στόχοι.\n")
    else:
        total_hours = sum(task['hours'] for task in tasks)
        average = total_hours / len(tasks)
        textbox.insert("end", f"Ο μέσος όρος των στόχων είναι: {average:.2f} ώρες\n")
    textbox.pack(pady=10)
    textbox.configure(state="disabled")

    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

# Pie Chart Frame
def show_pie_chart_frame():
    clear_window()
    tasks = users[current_user]['tasks']
    free_time = users[current_user]['free_time']
    plot_pie_chart(tasks, free_time)
    show_main_menu()

# Bar Chart Frame
def show_bar_chart_frame():
    clear_window()
    tasks = users[current_user]['tasks']
    free_time = users[current_user]['free_time']
    plot_bar_chart(tasks, free_time)
    show_main_menu()

# Start the application
if __name__ == "__main__":
    show_login_frame()
    root.mainloop()