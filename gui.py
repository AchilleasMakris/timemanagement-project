import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import *  # Import all functions from main.py

# Set up CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Διαχείριση Ελεύθερου Χρόνου")
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

def show_initial_login_menu():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Διαχείριση Ελεύθερου Χρόνου - Πλατφόρμα Σύνδεσης", font=("Arial", 20))
    title_label.pack(pady=20)

    button_frame = ctk.CTkFrame(root, fg_color="transparent")
    button_frame.pack(pady=10)

    login_button = ctk.CTkButton(button_frame, text="Σύνδεση", command=show_login_fields)
    login_button.pack(side="left", padx=5, pady=20)
    register_button = ctk.CTkButton(button_frame, text="Δημιουργία Χρήστη", command=show_register_fields)
    register_button.pack(side="left", padx=5, pady=20)


def show_login_fields():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Σύνδεση Χρήστη", font=("Arial", 20))
    title_label.pack(pady=20)

    username_label = ctk.CTkLabel(root, text="Όνομα χρήστη:")
    username_label.pack(pady=5)
    username_entry = ctk.CTkEntry(root, width=200)
    username_entry.pack()

    password_label = ctk.CTkLabel(root, text="Κωδικός χρήστη:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(root, width=200, show="*")
    password_entry.pack()

    def login():
        global current_user
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        Επιτυχία, result = connect_user(username, password)
        if Επιτυχία:
            current_user = username
            messagebox.showinfo("Επιτυχία", "Επιτυχής Σύνδεση.")
            show_main_menu()
        else:
            messagebox.showerror("Error", result)

    login_button = ctk.CTkButton(root, text="Είσοδος", command=login)
    login_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_initial_login_menu)
    back_button.pack(pady=10)


def show_register_fields():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Δημιουργία Χρήστη", font=("Arial", 20))
    title_label.pack(pady=20)

    username_label = ctk.CTkLabel(root, text="Όνομα χρήστη:")
    username_label.pack(pady=5)
    username_entry = ctk.CTkEntry(root, width=200)
    username_entry.pack()

    password_label = ctk.CTkLabel(root, text="Κωδικός χρήστη:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(root, width=200, show="*")
    password_entry.pack()

    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        Επιτυχία, message = register_user(username, password, password)
        if Επιτυχία:
            messagebox.showinfo("Επιτυχία", message)
            show_initial_login_menu()
        else:
            messagebox.showerror("Error", message)

    register_button = ctk.CTkButton(root, text="Δημιουργία Χρήστη", command=register)
    register_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_initial_login_menu)
    back_button.pack(pady=10)

# Main Menu Frame
def show_main_menu():
    clear_window()
    title_label = ctk.CTkLabel(root, text=f"Καλωσόρισες, {current_user}", font=("Arial", 20))
    title_label.pack(pady=20)

    options = [
        ("Διαχείρηση ελεύθερου χρόνου", show_manage_free_time_frame),
        ("Προσθήκη δραστηριότητας", show_add_task_frame),
        ("Επεξεργασία δραστηριότητας", show_edit_task_frame),
        ("Διαγραφή δραστηριότητας", show_delete_task_frame),
        ("Ταξινόμιση κατά σημαντικότητα", lambda: show_sorted_activities_frame(current_user)),
        ("Εμφάνιση δραστηριοτήτων", show_all_tasks_frame),
        ("Μέσος χρόνος δραστηριοτήτων", show_average_time_frame),
        ("Διάγραμμα Πίτας", show_pie_chart_frame),
        ("Ραβδόγραμμα", show_bar_chart_frame),
        ("Έξοδος", root.quit)
    ]
    for text, command in options:
        button = ctk.CTkButton(root, text=text, command=command, width=250)
        button.pack(pady=10)




# Implemented Functions
def show_manage_free_time_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Διαχείρηση ελεύθερου χρόνου", font=("Arial", 20))
    title_label.pack(pady=20)

    user = next(u for u in users if u["username"] == current_user)
    current_free_time = user["user_total_free_hours"]
    free_time_label = ctk.CTkLabel(root, text=f"Υπολειπόμενος ελεύθερος: {current_free_time} ώρες.")
    free_time_label.pack(pady=10)

    user_total_free_hours_label = ctk.CTkLabel(root, text="Δώσε τον ελεύθερο χρόνο που έχεις για αυτή την εβδομάδα σε ώρες:")
    user_total_free_hours_label.pack(pady=5)
    user_total_free_hours_entry = ctk.CTkEntry(root, width=200)
    user_total_free_hours_entry.pack()

    def update_free_time():
        try:
            # Get the input from the entry widget
            input_value = user_total_free_hours_entry.get().strip()
            # Convert it to a float
            user_total_free_hours = float(input_value)
            if user_total_free_hours < 0:
                raise ValueError("Δεν γίνεται να βάλετε αρνητικό αριθμό.")
            success, message = set_free_time(current_user, user_total_free_hours, activities, users)
            if success:
                messagebox.showinfo("Επιτυχία", message)
                show_main_menu()
            else:
                messagebox.showerror("Σφάλμα", message)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Λάθος εισαγωγή, παρακαλώ δώστε θετικό αριθμό.")

    update_button = ctk.CTkButton(root, text="Ενημέρωση", command=update_free_time)
    update_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

def show_add_task_frame():
    user = [u for u in users if u["username"] == current_user][0]
    if (user["user_total_free_hours"] == 0):
        clear_window()
        show_manage_free_time_frame()
        return # Σταματάει εδώ αν δεν έχει ελεύθερες ώρες
  
    clear_window()
    title_label = ctk.CTkLabel(root, text="Προσθήκη νέας δραστηριότητας", font=("Arial", 20))
    title_label.pack(pady=20)

    name_label = ctk.CTkLabel(root, text="Όνομα Δραστηριότητας:")
    name_label.pack(pady=5)
    name_entry = ctk.CTkEntry(root, width=200)
    name_entry.pack()

    duration_label = ctk.CTkLabel(root, text="Διάρκεια (Ώρες):")
    duration_label.pack(pady=5)
    duration_entry = ctk.CTkEntry(root, width=200)
    duration_entry.pack()

    importance_label = ctk.CTkLabel(root, text="Σημαντικότητα (1-10):")
    importance_label.pack(pady=5)
    importance_entry = ctk.CTkEntry(root, width=200)
    importance_entry.pack()

    # Type Toggle
    type_label = ctk.CTkLabel(root, text="Τύπος Δραστηριότητας:")
    type_label.pack(pady=5)

    selected_type = {"value": None}

    button_frame = ctk.CTkFrame(root, fg_color="transparent")
    button_frame.pack(pady=5)

    def select_type(choice):
        selected_type["value"] = choice
        if choice == "Υποχρέωση":
            ypoxrewsh_button.configure(fg_color="#1f6aa5")
            hobby_button.configure(fg_color="transparent")
        else:
            hobby_button.configure(fg_color="#1f6aa5")
            ypoxrewsh_button.configure(fg_color="transparent")

    ypoxrewsh_button = ctk.CTkButton(button_frame, text="Υποχρέωση", width=100, command=lambda: select_type("Υποχρέωση"))
    ypoxrewsh_button.pack(side="left", padx=5)

    hobby_button = ctk.CTkButton(button_frame, text="Χόμπι", width=100, command=lambda: select_type("Χόμπι"))
    hobby_button.pack(side="left", padx=5)

    # Add Activity Logic
    def add_task():
        name = name_entry.get().strip()
        duration = duration_entry.get().strip()
        importance = importance_entry.get().strip()
        task_type = selected_type["value"]

        if name and duration and importance and task_type:
            # Ελεγχος: το όνομα δεν μπορεί να είναι κενό, να περιέχει αριθμούς ή να μην έχει γράμματα
            if not name or not any(char.isalpha() for char in name):
                messagebox.showerror("Σφάλμα", "Το όνομα της δραστηριότητας δεν μπορεί να είναι κενό ή να μην περιέχει γράμματα.")
                return
            try:
                duration = float(duration)
                importance = int(importance)
                if not (1 <= importance <= 10):
                    raise ValueError("Η σημαντικότητα πρέπει να είναι μεταξύ 1-10")
                Επιτυχία, message, _ = add_activity(current_user, name, duration, importance, task_type, activities, users)
                if Επιτυχία:
                    messagebox.showinfo("Επιτυχία", message)
                    show_main_menu()
                else:
                    messagebox.showerror("Σφάλμα", message)
            except ValueError as e:
                messagebox.showerror("Σφάλμα", str(e))
        else:
            messagebox.showerror("Σφάλμα", "Απαιτούνται όλα τα πεδία.")

    add_button = ctk.CTkButton(root, text="Προσθήκη δραστηριότητας", command=add_task)
    add_button.pack(pady=10)

    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=10)

def show_all_tasks_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Όλες οι δραστηριότητες", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        no_tasks_label = ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.")
        no_tasks_label.pack(pady=10)
    else:
        for task in user_tasks:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            task_label = ctk.CTkLabel(root, text=task_str)
            task_label.pack(pady=5)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=20)

def show_sorted_activities_frame(username):
    clear_window()
    title_label = ctk.CTkLabel(root, text="Οι δραστηριότητες ταξινομίθηκας κατα συμαντικότητα", font=("Arial", 20))
    title_label.pack(pady=20)
    user_activities = [a for a in activities if a["username"] == username]
    if not user_activities:
        no_tasks_label = ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.")
        no_tasks_label.pack(pady=10)
    else:
        sorted_activities = sorted(user_activities, key=lambda x: x["Σημαντικότητα"], reverse=True)
        for task in sorted_activities:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            task_label = ctk.CTkLabel(root, text=task_str)
            task_label.pack(pady=5)
    back_button = ctk.CTkButton(root, text="Πίσω", command=show_main_menu)
    back_button.pack(pady=20)

def show_edit_task_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Επεξεργασία Δραστηριότηας", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
        ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=20)
        return

    task_names = [task["Δραστηριότητα"] for task in user_tasks]
    task_combobox = ctk.CTkComboBox(root, values=task_names)
    task_combobox.pack(pady=10)

    name_entry = ctk.CTkEntry(root, width=200)
    duration_entry = ctk.CTkEntry(root, width=200)
    importance_entry = ctk.CTkEntry(root, width=200)

    selected_type = ctk.StringVar(value="")  # To store the selected type

    def select_type(choice):
        selected_type.set(choice)
        if choice == "Υποχρέωση":
            ypoxrewsh_button.configure(fg_color="#1f6aa5")
            hobby_button.configure(fg_color="transparent")
        else:
            hobby_button.configure(fg_color="#1f6aa5")
            ypoxrewsh_button.configure(fg_color="transparent")

    def load_task_details():
        selected_task = task_combobox.get()
        for task in user_tasks:
            if task["Δραστηριότητα"] == selected_task:
                name_entry.delete(0, "end")
                name_entry.insert(0, task["Δραστηριότητα"])
                duration_entry.delete(0, "end")
                duration_entry.insert(0, str(task["Διάρκεια"]))
                importance_entry.delete(0, "end")
                importance_entry.insert(0, str(task["Σημαντικότητα"]))
                select_type(task["Τύπος"])  # Pre-select the type and update colors
                break

    ctk.CTkButton(root, text="Φόρτωση δραστηριότητας", command=load_task_details).pack(pady=10)
    ctk.CTkLabel(root, text="Όνομα δραστηριότητας:").pack(pady=5)
    name_entry.pack()
    ctk.CTkLabel(root, text="Διάρκεια (hours):").pack(pady=5)
    duration_entry.pack()
    ctk.CTkLabel(root, text="Συμαντικότητα (1-10):").pack(pady=5)
    importance_entry.pack()
    ctk.CTkLabel(root, text="Τύπος:").pack(pady=5)

    # Frame to hold the buttons side by side
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=5)

    ypoxrewsh_button = ctk.CTkButton(button_frame, text="Υποχρέωση", width=100, command=lambda: select_type("Υποχρέωση"))
    ypoxrewsh_button.pack(side="left", padx=5)

    hobby_button = ctk.CTkButton(button_frame, text="Χόμπι", width=100, command=lambda: select_type("Χόμπι"))
    hobby_button.pack(side="left", padx=5)

    def save_changes():
        selected_task = task_combobox.get()
        new_name = name_entry.get().strip() or None
        new_duration_str = duration_entry.get().strip()
        new_duration = float(new_duration_str) if new_duration_str else None
        new_importance_str = importance_entry.get().strip()
        new_importance = int(new_importance_str) if new_importance_str and 1 <= int(new_importance_str) <= 10 else None
        new_type = selected_type.get()

        if new_importance_str and (not new_importance or not (1 <= new_importance <= 10)):
            messagebox.showerror("Σφάλμα", "Ο βαθμός σημαντικότητας πρέπει να είναι 1-10")
            return
        if new_type not in ["Υποχρέωση", "Χόμπι"]:
            messagebox.showerror("Σφάλμα", "Ο τύπος δραστηριότητας πρέπει να είναι Υποχρέωση ή Χόμπι")
            return

        Επιτυχία, message = modify_activity(current_user, selected_task, new_onoma=new_name, new_diarkeia=new_duration, new_grade=new_importance, new_type=new_type, activities=activities, users=users)
        if Επιτυχία:
            messagebox.showinfo("Επιτυχία", message)
            show_main_menu()
        else:
            messagebox.showerror("Σφάλμα", message)

    ctk.CTkButton(root, text="Αποθήκευση αλλαγών", command=save_changes).pack(pady=10)
    ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=10)
    
def show_delete_task_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Διαγραφή δραστηριότητας", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
        ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=20)
        return

    task_names = [task["Δραστηριότητα"] for task in user_tasks]
    task_combobox = ctk.CTkComboBox(root, values=task_names)
    task_combobox.pack(pady=10)

    def delete_task():
        selected_task = task_combobox.get()
        Επιτυχία, message = delete_activity(current_user, selected_task, activities, users)
        if Επιτυχία:
            messagebox.showinfo("Επιτυχία", message)
            show_main_menu()
        else:
            messagebox.showerror("Σφάλμα", message)

    ctk.CTkButton(root, text="Διαγραφή Δραστηριότητας", command=delete_task).pack(pady=10)
    ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=10)

def show_average_time_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Μέσος χρόνος δραστηριοτήτων", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    if user_tasks:
        average_time = sum(task["Διάρκεια"] for task in user_tasks) / len(user_tasks)
        ctk.CTkLabel(root, text=f"Μέσος χρόνος των δραστηριοτήτων: {average_time:.2f} ώρες").pack(pady=10)
    else:
        ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
    ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=20)

def show_pie_chart_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Διάγραμμα Πίτας", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    user = next(u for u in users if u["username"] == current_user)
    user_total_free_hours = user["user_total_free_hours"]

    if user_tasks or user_total_free_hours > 0:
        # Δημιουργία figure για το γράφημα
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = [activity['Δραστηριότητα'] for activity in user_tasks]
        sizes = [float(activity['Διάρκεια']) for activity in user_tasks]
        if user_total_free_hours > 0:
            labels.append("Ελεύθερος χρόνος")
            sizes.append(user_total_free_hours)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("Κατανομή Χρόνου")

        # Ενσωμάτωση του figure στο Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        ctk.CTkLabel(root, text="Δεν βρέθηκαν δεδομένα.").pack(pady=10)
    ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=20)

def show_bar_chart_frame():
    clear_window()
    title_label = ctk.CTkLabel(root, text="Ραβδόγραμμα", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    user = next(u for u in users if u["username"] == current_user)
    user_total_free_hours = user["user_total_free_hours"]

    if user_tasks:
        # Δημιουργία figure για το γράφημα
        fig, ax = plt.subplots(figsize=(6, 4))
        names = [activity['Δραστηριότητα'] for activity in user_tasks]
        hours = [float(activity['Διάρκεια']) for activity in user_tasks]
        colors = plt.get_cmap('tab10').colors
        bars = ax.bar(names, hours, color=colors[:len(names)])
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval} ώρες", ha='center', va='bottom')
        ax.axhline(y=user_total_free_hours, color='r', linestyle='--', label='Ελεύθερος Χρόνος')
        if len(names) > 0:
            ax.text(len(names)-0.5, user_total_free_hours + 0.5, f"Ελεύθερος Χρόνος: {user_total_free_hours} ώρες", color='r', va='bottom')
        ax.legend()
        ax.set_xlabel("Δραστηριότητες")
        ax.set_ylabel("Ώρες")
        ax.set_title("Ώρες ανά Δραστηριότητα")
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Ενσωμάτωση του figure στο Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        ctk.CTkLabel(root, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
    ctk.CTkButton(root, text="Πίσω", command=show_main_menu).pack(pady=20)

# Start the application
if __name__ == "__main__":
    show_initial_login_menu()
    root.mainloop()