import re

tasks = []
total_hours = 0


def display_menu():
    print("\n--- Time Management ---")
    print("1. Προσθήκη νέου στόχου")
    print("2. Τροποποίηση στόχου")
    print("3. Διαγραφή στόχου")
    print("4. Έξοδος")


def task_add(tasks, total_hours):

    #infinite loop for try and exceptions
    while True:
        # try to input user data
        try:    
            name = input("Δώσε το όνομα του στόχου: ").strip()

            # Validate name: Must contain only letters and spaces
            if not name.replace(" ", "").isalpha():
                raise ValueError("Invalid name, please enter a word.")
            
            hours = float(input("Δώσε την εβδομαδιαία διάρκεια σε ώρες: "))

            if not (0 <= hours <= 168):
                raise ValueError("Λάθος αριθμός χρόνου του στόχου.")
            if total_hours + hours > 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            

            importance = int(input("Δώσε τον βαθμό σημαντικότητας του στόχου: "))

            if not (1 <= importance <= 10):
                raise ValueError("Importance must be a number between 1 - 10")

        except ValueError:
            print("Invalid input. Please enter numbers for hours and importance.")
            continue

            
        tasks.append({"name": name, "hours": hours, "importance": importance})
        total_hours += hours
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        break;
    #Επιστρέφουμε το total_hours για να παρει την νεα τιμη
    return total_hours


def task_edit():
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return

    print("Επέλεξε το όνομα του Task που θέλεις να τροποποιήσεις: ")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις τροποποίηση: "))
        if task_index >= len(tasks) or task < 0:
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError("Παρακαλώ εισάγετε έναν έγκυρο αριθμό."):
        return

    current_task = tasks[task_index]

    user_input = int(input())
    if(user_input == 1):
        new_name = input("Δώστε το νέο όνομα του Task: ")
        if(new_name.replace(" ", "").isalpha()):
            current_task['name'] = new_name
        else:
            print("Μη αποδεκτό όνομα.")
    
    new_hours = float(input("Παρακαλώ, δώστε τις εβδομαδιαίες ώρες: "))
    if 0 <= new_hours <= 168:
        current_task['hours'] = new_hours
    else:
        print("Άκυρη εισαγωγή ώρας, παρακαλώ προσπαθήστε ξανά.")
    
    new_importance = int(input("Δώσε τον βαθμό σημαντικότητας του Task: "))
    if 1 <= new_importance <= 10:
        current_task['importance'] = new_importance
    else:
        print("Άκυρη τιμή σημαντικότητας του Task. Παρακαλώ προσπαθήστε ξανά.")
    

while True:
    display_menu()
    user_input = int(input("Επέλεξε έναν αριθμό απο το 1-4: "))
    if(user_input == 1):
        total_hours = task_add(tasks, total_hours)
    if(user_input == 2):
        task_edit()
    if(user_input == 4):
        break
    
