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

            # Έλεγχος του ονόματος και αφαίρεση κενών για να γίνει 1 λέξη
            if not name.replace(" ", "").isalpha():
                raise ValueError("Λάθος όνομα του Task, παρακαλώ γράψτε μια λέξη.")
            
            hours = float(input("Δώσε την εβδομαδιαία διάρκεια σε ώρες: "))
            # Έλεγχος αν ο χρήστης βάλει παραπάνω απο τις διαθέσιμες ώρες της εβδομάδας
            if not (0 <= hours <= 168):
                raise ValueError("Λάθος αριθμός χρόνου του στόχου.")
            if total_hours + hours > 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            

            importance = int(input("Δώσε τον βαθμό σημαντικότητας του στόχου: "))

            #Έλεγχος αν ο χρήστης έβαλε σωστή τιμή
            if not (1 <= importance <= 10):
                raise ValueError("Ο αριθμός πρέπει να είναι απο 1 - 10")

        except ValueError:
            print("Λάθος εισαγωγή, παρακαλώ βάλτε αριθμούς για τις ώρες και την συμαντικότητα.")
            continue

        free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))

        # Έλεγχος του διαθέσιμου χρόνου της εβδομάδας
        #TODO Να το κάνω Global και όχι σε κάθε νέο τασκ να το ξανά ζητάει!
        if not 1 <= free_time <= 168:
            raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            
        tasks.append({"name": name, "hours": hours, "importance": importance})
        total_hours += hours
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        break;
    #Επιστρέφουμε το total_hours για να παρει την νεα τιμη
    return total_hours


def task_edit():
    # Αν δεν υπάρχουν Tasks τότε δεν μπορεί να γίνει και Edit.
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return

    print("Επέλεξε το όνομα του Task που θέλεις να τροποποιήσεις: ")
    # Έλεγχος και εκτύπωση του Task List, i+1 γιατί είναι 0-Indexed
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        # -1 Για να γίνει σωστά η μετατροπή σε 0-Indexed
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις τροποποίηση: ")) - 1
        # Έλεγχος αν είναι μέσα στα όρια.
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    #Επιλογή του Task τροποποίησης.
    current_task = tasks[task_index]

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
        
def task_del():
    if not tasks:
        print("Δεν υπάρχουν στόχοι για διαγραφή.")
        return

    print("Επέλεξε το όνομα του Task που θέλεις να διαγράψεις: ")
    # Έλεγχος και εκτύπωση του Task List, i+1 γιατί είναι 0-Indexed
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        # -1 Για να γίνει σωστά η μετατροπή σε 0-Indexed
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις διαγράψεις: ")) - 1
        # Έλεγχος αν είναι μέσα στα όρια.
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    #Επιλογή του Task και διαγραφή
    tasks.pop(task_index)

#Infinite Loop μέχρι την Manual έξοδο του χρήστη με τον αριθμό 4 ή Ctrl+C
while True:
    display_menu()
    user_input = int(input("Επέλεξε έναν αριθμό απο το 1-4: "))
    if(user_input == 1):
        total_hours = task_add(tasks, total_hours)
    if(user_input == 2):
        task_edit()
    if(user_input == 3):
        task_del()
    if(user_input == 4):
        break

    #testT