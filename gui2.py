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
root.geometry("1600x900")

current_user = None  # Track the currently logged-in user

# Load initial data
load_users_from_csv()
load_activities_from_csv()

# Function to clear the window for new frames
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Login Frame (unchanged)
def show_login_frame():
    global current_user
    clear_window()

    title_label = ctk.CTkLabel(root, text="Διαχείριση Ελεύθερου Χρόνου - Πλατφόρμα Σύνδεσης", font=("Arial", 20))
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
        success, result = connect_user(username, password)
        if success:
            current_user = username
            messagebox.showinfo("Επιτυχία", "Επιτυχής Σύνδεση.")
            show_main_menu()
        else:
            messagebox.showerror("Error", result)

    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        success, message = register_user(username, password, password)
        if success:
            messagebox.showinfo("Επιτυχία", message)
        else:
            messagebox.showerror("Error", message)

    button_frame = ctk.CTkFrame(root, fg_color="transparent")
    button_frame.pack(pady=10)

    login_button = ctk.CTkButton(button_frame, text="Σύνδεση", command=login)
    login_button.pack(side="left", padx=5, pady=20)
    register_button = ctk.CTkButton(button_frame, text="Εγγραφή", command=register)
    register_button.pack(side="left", padx=5, pady=20)

# Main Menu with Tabs (updated)
def show_main_menu():
    global tabview, all_tasks_frame, sorted_tasks_frame, pie_chart_frame, bar_chart_frame, edit_combobox, delete_combobox
    clear_window()
    title_label = ctk.CTkLabel(root, text=f"Καλωσόρισες, {current_user}", font=("Arial", 20))
    title_label.pack(pady=20)

    tabview = ctk.CTkTabview(root, height=50, corner_radius=10)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)

    tab_names = [
        "Διαχείριση\nΕλεύθερου Χρόνου",
        "Προσθήκη\nΔραστηριότητας",
        "Επεξεργασία\nΔραστηριότητας",
        "Διαγραφή\nΔραστηριότητας",
        "Ταξινόμηση\nκατά Σημαντικότητα",
        "Εμφάνιση\nΔραστηριοτήτων",
        "Μέσος Χρόνος\nΔραστηριοτήτων",
        "Διάγραμμα\nΠίτας",
        "Ραβδόγραμμα"
    ]

    for name in tab_names:
        tabview.add(name)

    # Configure tab button appearance to match "Χόμπι" and "Υποχρέωση" buttons
    tabview._segmented_button.configure(
        font=("Arial", 16, "bold"),           # Bold font for modern look
        corner_radius=10,                     # Rounded corners
        border_width=2,                       # Subtle border for definition
        text_color="white",                   # White text for contrast
        fg_color="#1f6aa5",                   # Selected tab color matching "Χόμπι" and "Υποχρέωση"
        unselected_color="#2b2b2b",           # Solid dark gray instead of transparent
        selected_hover_color="#2a85c9",       # Slightly darker blue on hover when selected
        unselected_hover_color="#555555"      # Gray hover effect for unselected tabs
    )

    # Populate each tab
    populate_manage_free_time_tab(tabview.tab("Διαχείριση\nΕλεύθερου Χρόνου"))
    populate_add_task_tab(tabview.tab("Προσθήκη\nΔραστηριότητας"))
    populate_edit_task_tab(tabview.tab("Επεξεργασία\nΔραστηριότητας"))
    populate_delete_task_tab(tabview.tab("Διαγραφή\nΔραστηριότητας"))
    populate_sorted_tasks_tab(tabview.tab("Ταξινόμηση\nκατά Σημαντικότητα"))
    populate_all_tasks_tab(tabview.tab("Εμφάνιση\nΔραστηριοτήτων"))
    populate_average_time_tab(tabview.tab("Μέσος Χρόνος\nΔραστηριοτήτων"))
    populate_pie_chart_tab(tabview.tab("Διάγραμμα\nΠίτας"))
    populate_bar_chart_tab(tabview.tab("Ραβδόγραμμα"))

    # Set command for tab selection
    tabview.configure(command=on_tab_selected)

    # Exit button
    exit_button = ctk.CTkButton(root, text="Έξοδος", command=root.quit, font=("Arial", 14, "bold"), height=40, corner_radius=10)
    exit_button.pack(pady=10)
# Remaining functions (unchanged)
def populate_manage_free_time_tab(tab):
    title_label = ctk.CTkLabel(tab, text="Διαχείριση ελεύθερου χρόνου", font=("Arial", 20))
    title_label.pack(pady=20)

    user = next(u for u in users if u["username"] == current_user)
    free_time_label = ctk.CTkLabel(tab, text=f"Υπολειπόμενος ελεύθερος: {user['user_total_free_hours']} ώρες.")
    free_time_label.pack(pady=10)

    user_total_free_hours_label = ctk.CTkLabel(tab, text="Δώσε τον ελεύθερο χρόνο που έχεις για αυτή την εβδομάδα σε ώρες:")
    user_total_free_hours_label.pack(pady=5)
    user_total_free_hours_entry = ctk.CTkEntry(tab, width=200)
    user_total_free_hours_entry.pack()

    def update_free_time():
        try:
            user_total_free_hours = float(user_total_free_hours_entry.get().strip())
            if user_total_free_hours < 0:
                raise ValueError("Δεν γίνεται να βάλετε αρνητικό αριθμό.")
            success, message = set_free_time(current_user, user_total_free_hours, activities, users)
            if success:
                messagebox.showinfo("Επιτυχία", message)
                free_time_label.configure(text=f"Υπολειπόμενος ελεύθερος: {user['user_total_free_hours']} ώρες.")
            else:
                messagebox.showerror("Σφάλμα", message)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Λάθος εισαγωγή, παρακαλώ δώστε θετικό αριθμό.")

    update_button = ctk.CTkButton(tab, text="Ενημέρωση", command=update_free_time)
    update_button.pack(pady=10)

def populate_add_task_tab(tab):
    title_label = ctk.CTkLabel(tab, text="Προσθήκη νέας δραστηριότητας", font=("Arial", 20))
    title_label.pack(pady=20)

    name_label = ctk.CTkLabel(tab, text="Όνομα Δραστηριότητας:")
    name_label.pack(pady=5)
    name_entry = ctk.CTkEntry(tab, width=200)
    name_entry.pack()

    duration_label = ctk.CTkLabel(tab, text="Διάρκεια (Ώρες):")
    duration_label.pack(pady=5)
    duration_entry = ctk.CTkEntry(tab, width=200)
    duration_entry.pack()

    importance_label = ctk.CTkLabel(tab, text="Σημαντικότητα (1-10):")
    importance_label.pack(pady=5)
    importance_entry = ctk.CTkEntry(tab, width=200)
    importance_entry.pack()

    type_label = ctk.CTkLabel(tab, text="Τύπος Δραστηριότητας:")
    type_label.pack(pady=5)

    selected_type = {"value": None}

    button_frame = ctk.CTkFrame(tab, fg_color="transparent")
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

    def add_task():
        name = name_entry.get().strip()
        duration = duration_entry.get().strip()
        importance = importance_entry.get().strip()
        task_type = selected_type["value"]
        if name and duration and importance and task_type:
            try:
                duration = float(duration)
                importance = int(importance)
                if not (1 <= importance <= 10):
                    raise ValueError("Η σημαντικότητα πρέπει να είναι μεταξύ 1-10")
                success, message, _ = add_activity(current_user, name, duration, importance, task_type, activities, users)
                if success:
                    messagebox.showinfo("Επιτυχία", message)
                    name_entry.delete(0, "end")
                    duration_entry.delete(0, "end")
                    importance_entry.delete(0, "end")
                    selected_type["value"] = None
                    ypoxrewsh_button.configure(fg_color="transparent")
                    hobby_button.configure(fg_color="transparent")
                else:
                    messagebox.showerror("Σφάλμα", message)
            except ValueError as e:
                messagebox.showerror("Σφάλμα", str(e))
        else:
            messagebox.showerror("Σφάλμα", "Απαιτούνται όλα τα πεδία.")

    add_button = ctk.CTkButton(tab, text="Προσθήκη δραστηριότητας", command=add_task)
    add_button.pack(pady=10)

def populate_edit_task_tab(tab):
    global edit_combobox
    title_label = ctk.CTkLabel(tab, text="Επεξεργασία Δραστηριότητας", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    task_names = [task["Δραστηριότητα"] for task in user_tasks] if user_tasks else ["Καμία δραστηριότητα"]
    edit_combobox = ctk.CTkComboBox(tab, values=task_names)
    edit_combobox.pack(pady=10)

    name_entry = ctk.CTkEntry(tab, width=200)
    duration_entry = ctk.CTkEntry(tab, width=200)
    importance_entry = ctk.CTkEntry(tab, width=200)

    selected_type = StringVar(value="")

    def select_type(choice):
        selected_type.set(choice)
        if choice == "Υποχρέωση":
            ypoxrewsh_button.configure(fg_color="#1f6aa5")
            hobby_button.configure(fg_color="transparent")
        else:
            hobby_button.configure(fg_color="#1f6aa5")
            ypoxrewsh_button.configure(fg_color="transparent")

    def load_task_details():
        selected_task = edit_combobox.get()
        for task in user_tasks:
            if task["Δραστηριότητα"] == selected_task:
                name_entry.delete(0, "end")
                name_entry.insert(0, task["Δραστηριότητα"])
                duration_entry.delete(0, "end")
                duration_entry.insert(0, str(task["Διάρκεια"]))
                importance_entry.delete(0, "end")
                importance_entry.insert(0, str(task["Σημαντικότητα"]))
                select_type(task["Τύπος"])
                break

    ctk.CTkButton(tab, text="Φόρτωση δραστηριότητας", command=load_task_details).pack(pady=10)
    ctk.CTkLabel(tab, text="Όνομα δραστηριότητας:").pack(pady=5)
    name_entry.pack()
    ctk.CTkLabel(tab, text="Διάρκεια (hours):").pack(pady=5)
    duration_entry.pack()
    ctk.CTkLabel(tab, text="Σημαντικότητα (1-10):").pack(pady=5)
    importance_entry.pack()
    ctk.CTkLabel(tab, text="Τύπος:").pack(pady=5)

    button_frame = ctk.CTkFrame(tab)
    button_frame.pack(pady=5)

    ypoxrewsh_button = ctk.CTkButton(button_frame, text="Υποχρέωση", width=100, command=lambda: select_type("Υποχρέωση"))
    ypoxrewsh_button.pack(side="left", padx=5)
    hobby_button = ctk.CTkButton(button_frame, text="Χόμπι", width=100, command=lambda: select_type("Χόμπι"))
    hobby_button.pack(side="left", padx=5)

    def save_changes():
        selected_task = edit_combobox.get()
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

        success, message = modify_activity(current_user, selected_task, new_onoma=new_name, new_diarkeia=new_duration, new_grade=new_importance, new_type=new_type, activities=activities, users=users)
        if success:
            messagebox.showinfo("Επιτυχία", message)
            update_edit_combobox()
        else:
            messagebox.showerror("Σφάλμα", message)

    ctk.CTkButton(tab, text="Αποθήκευση αλλαγών", command=save_changes).pack(pady=10)

def populate_delete_task_tab(tab):
    global delete_combobox
    title_label = ctk.CTkLabel(tab, text="Διαγραφή δραστηριότητας", font=("Arial", 20))
    title_label.pack(pady=20)

    user_tasks = [task for task in activities if task["username"] == current_user]
    task_names = [task["Δραστηριότητα"] for task in user_tasks] if user_tasks else ["Καμία δραστηριότητα"]
    delete_combobox = ctk.CTkComboBox(tab, values=task_names)
    delete_combobox.pack(pady=10)

    def delete_task():
        selected_task = delete_combobox.get()
        success, message = delete_activity(current_user, selected_task, activities, users)
        if success:
            messagebox.showinfo("Επιτυχία", message)
            update_delete_combobox()
        else:
            messagebox.showerror("Σφάλμα", message)

    ctk.CTkButton(tab, text="Διαγραφή Δραστηριότητας", command=delete_task).pack(pady=10)

def populate_sorted_tasks_tab(tab):
    global sorted_tasks_frame
    title_label = ctk.CTkLabel(tab, text="Ταξινόμηση κατά σημαντικότητα", font=("Arial", 20))
    title_label.pack(pady=20)
    sorted_tasks_frame = ctk.CTkFrame(tab)
    sorted_tasks_frame.pack(fill="both", expand=True)

def populate_all_tasks_tab(tab):
    global all_tasks_frame
    title_label = ctk.CTkLabel(tab, text="Όλες οι δραστηριότητες", font=("Arial", 20))
    title_label.pack(pady=20)
    all_tasks_frame = ctk.CTkFrame(tab)
    all_tasks_frame.pack(fill="both", expand=True)

def populate_average_time_tab(tab):
    title_label = ctk.CTkLabel(tab, text="Μέσος χρόνος δραστηριοτήτων", font=("Arial", 20))
    title_label.pack(pady=20)
    average_time_frame = ctk.CTkFrame(tab)
    average_time_frame.pack(fill="both", expand=True)

    def update_average_time():
        for widget in average_time_frame.winfo_children():
            widget.destroy()
        user_tasks = [task for task in activities if task["username"] == current_user]
        if user_tasks:
            average_time = sum(task["Διάρκεια"] for task in user_tasks) / len(user_tasks)
            ctk.CTkLabel(average_time_frame, text=f"Μέσος χρόνος των δραστηριοτήτων: {average_time:.2f} ώρες").pack(pady=10)
        else:
            ctk.CTkLabel(average_time_frame, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)

    update_average_time()

def populate_pie_chart_tab(tab):
    global pie_chart_frame
    title_label = ctk.CTkLabel(tab, text="Διάγραμμα Πίτας", font=("Arial", 20))
    title_label.pack(pady=20)
    pie_chart_frame = ctk.CTkFrame(tab)
    pie_chart_frame.pack(fill="both", expand=True)

def populate_bar_chart_tab(tab):
    global bar_chart_frame
    title_label = ctk.CTkLabel(tab, text="Ραβδόγραμμα", font=("Arial", 20))
    title_label.pack(pady=20)
    bar_chart_frame = ctk.CTkFrame(tab)
    bar_chart_frame.pack(fill="both", expand=True)

# Update Functions (unchanged)
def update_all_tasks():
    for widget in all_tasks_frame.winfo_children():
        widget.destroy()
    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        ctk.CTkLabel(all_tasks_frame, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
    else:
        for task in user_tasks:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            ctk.CTkLabel(all_tasks_frame, text=task_str).pack(pady=5)

def update_sorted_tasks():
    for widget in sorted_tasks_frame.winfo_children():
        widget.destroy()
    user_tasks = [task for task in activities if task["username"] == current_user]
    if not user_tasks:
        ctk.CTkLabel(sorted_tasks_frame, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)
    else:
        sorted_tasks = sorted(user_tasks, key=lambda x: x["Σημαντικότητα"], reverse=True)
        for task in sorted_tasks:
            task_str = f"{task['Δραστηριότητα']} - Duration: {task['Διάρκεια']} hours, Importance: {task['Σημαντικότητα']}, Type: {task['Τύπος']}"
            ctk.CTkLabel(sorted_tasks_frame, text=task_str).pack(pady=5)

def update_pie_chart():
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()
    user_tasks = [task for task in activities if task["username"] == current_user]
    user = next(u for u in users if u["username"] == current_user)
    user_total_free_hours = user["user_total_free_hours"]
    if user_tasks or user_total_free_hours > 0:
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = [activity['Δραστηριότητα'] for activity in user_tasks]
        sizes = [float(activity['Διάρκεια']) for activity in user_tasks]
        if user_total_free_hours > 0:
            labels.append("Ελεύθερος χρόνος")
            sizes.append(user_total_free_hours)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("Κατανομή Χρόνου")
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        ctk.CTkLabel(pie_chart_frame, text="Δεν βρέθηκαν δεδομένα.").pack(pady=10)

def update_bar_chart():
    for widget in bar_chart_frame.winfo_children():
        widget.destroy()
    user_tasks = [task for task in activities if task["username"] == current_user]
    user = next(u for u in users if u["username"] == current_user)
    user_total_free_hours = user["user_total_free_hours"]
    if user_tasks:
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
        canvas = FigureCanvasTkAgg(fig, master=bar_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        ctk.CTkLabel(bar_chart_frame, text="Δεν βρέθηκαν δραστηριότητες.").pack(pady=10)

def update_edit_combobox():
    user_tasks = [task for task in activities if task["username"] == current_user]
    task_names = [task["Δραστηριότητα"] for task in user_tasks] if user_tasks else ["Καμία δραστηριότητα"]
    edit_combobox.configure(values=task_names)
    if task_names[0] != "Καμία δραστηριότητα":
        edit_combobox.set(task_names[0])

def update_delete_combobox():
    user_tasks = [task for task in activities if task["username"] == current_user]
    task_names = [task["Δραστηριότητα"] for task in user_tasks] if user_tasks else ["Καμία δραστηριότητα"]
    delete_combobox.configure(values=task_names)
    if task_names[0] != "Καμία δραστηριότητα":
        delete_combobox.set(task_names[0])

def on_tab_selected():
    current_tab = tabview.get()
    if current_tab == "Εμφάνιση\nΔραστηριοτήτων":
        update_all_tasks()
    elif current_tab == "Ταξινόμηση\nκατά Σημαντικότητα":
        update_sorted_tasks()
    elif current_tab == "Διάγραμμα\nΠίτας":
        update_pie_chart()
    elif current_tab == "Ραβδόγραμμα":
        update_bar_chart()
    elif current_tab == "Επεξεργασία\nΔραστηριότητας":
        update_edit_combobox()
    elif current_tab == "Διαγραφή\nΔραστηριότητας":
        update_delete_combobox()

# Start the application
if __name__ == "__main__":
    show_login_frame()
    root.mainloop()