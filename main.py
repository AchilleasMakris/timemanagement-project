import re

tasks = []
total_hours = 0
free_time_flag = False  # Flag για το ελεύθερο χρόνο
free_time = 0  # Αρχικοποιούμε το free_time

def display_menu():
    print("\n--- Time Management ---")
    print("1. Προσθήκη νέου στόχου")
    print("2. Τροποποίηση στόχου")
    print("3. Διαγραφή στόχου")
    print("4. Ταξινόμιση κατά σημαντικότητα")
    print("5. Εκτύπωση όλων των στόχων")
    print("6. Έξοδος")

def task_add(tasks, total_hours):
    global free_time, free_time_flag  # Δηλώνουμε τις μεταβλητές ως global για να τις τροποποιούμε γιατί αλλιώς τροποποιούντε μόνο τοπικά! 

    # Αν το free_time δεν έχει ρυθμιστεί, ζητάμε από τον χρήστη να το εισάγει
    if not free_time_flag:
        while True:
            try:
                free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
                if not 1 <= free_time <= 168:
                    raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
                free_time_flag = True  # Όταν ο χρήστης δώσει σωστά το free_time, το flag τίθεται σε True
                break
            except ValueError:
                print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")

    # Loop για την προσθήκη στόχου
    while True:
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

            # Ελέγχουμε αν ο συνολικός χρόνος (με το νέο task) υπερβαίνει τον ελεύθερο χρόνο
            if total_hours + hours > free_time:
                remaining_free_time = free_time - total_hours  # Υπολογισμός υπολειπόμενου ελεύθερου χρόνου
                print(f"Δεν μπορείς να ξεπεράσεις τον ελεύθερο χρόνο σου των {free_time} ωρών!")
                print(f"Έχεις ακόμη {remaining_free_time} ώρες ελεύθερου χρόνου διαθέσιμες.")
                break  # Διακόπτουμε το loop αν ξεπεράσει τον ελεύθερο χρόνο

            importance = int(input("Δώσε τον βαθμό σημαντικότητας του στόχου: "))
            # Έλεγχος αν ο χρήστης έβαλε σωστή τιμή
            if not (1 <= importance <= 10):
                raise ValueError("Ο αριθμός πρέπει να είναι απο 1 - 10")

        except ValueError:
            print("Λάθος εισαγωγή, παρακαλώ βάλτε αριθμούς για τις ώρες και την σημαντικότητα.")
            continue

        tasks.append({"name": name, "hours": hours, "importance": importance})
        total_hours += hours
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        remaining_free_time = free_time - total_hours  # Υπολογισμός του ελεύθερου χρόνου που απομένει
        print(f"Απομένουν {remaining_free_time} ώρες ελεύθερου χρόνου.")
        break

    return total_hours


def task_edit():
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return

    print("Επέλεξε το όνομα του Task που θέλεις να τροποποιήσεις: ")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις τροποποίηση: ")) - 1
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

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
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις διαγράψεις: ")) - 1
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    tasks.pop(task_index)

def sort_by_importance():
    print("\nΈγινε η ταξινόμιση με βάση του πόσο σημαντικό είναι το κάθε Task.\n")
    tasks.sort(key=lambda x: x['importance'], reverse=True)
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']} (Importance: {task['importance']}, Hours: {task['hours']})")

def show_all():
    if not tasks:
        print("\nΔεν υπάρχουν στόχοι.\n")
        return
    
    print("\n--- Όλοι οι στόχοι ---")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")



while True:
    display_menu()
    user_input = int(input("Επέλεξε έναν αριθμό απο το 1-5: "))
    if user_input == 1:
        total_hours = task_add(tasks, total_hours)
    elif user_input == 2:
        task_edit()
    elif user_input == 3:
        task_del()
    elif user_input == 4:
        sort_by_importance()
    elif user_input == 5:
        show_all()
    elif user_input == 6:
        break
