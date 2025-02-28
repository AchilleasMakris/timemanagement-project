tasks = []  # Λίστα που αποθηκεύει όλους τους στόχους
total_hours = 0.0  # Μεταβλητή που αποθηκεύει τον συνολικό αριθμό ωρών που έχουν ανατεθεί στους στόχους
free_time_flag = False  # Σημαία που δείχνει αν ο ελεύθερος χρόνος έχει οριστεί
free_time = 0  # Αρχικοποιούμε τον ελεύθερο χρόνο σε 0

def display_menu():
    # Εμφανίζει το μενού επιλογών στον χρήστη
    print("\n--- Time Management ---")
    print("1. Προσθήκη νέου στόχου")
    print("2. Τροποποίηση στόχου")
    print("3. Διαγραφή στόχου")
    print("4. Ταξινόμιση κατά σημαντικότητα")
    print("5. Εκτύπωση όλων των στόχων")
    print("6. Μέσος όρος χρόνου των Task")
    print("7. Έξοδος")

def task_add(tasks, total_hours):
    global free_time, free_time_flag  # Δηλώνουμε τις μεταβλητές ως global για να τις τροποποιούμε

    # Αν το free_time δεν έχει ρυθμιστεί, ζητάμε από τον χρήστη να το εισάγει
    if not free_time_flag:
        while True:
            try:
                free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
                if not 1 <= free_time <= 168:  # Έλεγχος αν οι ώρες είναι μέσα στο όριο
                    raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
                free_time_flag = True  # Το flag τίθεται σε True όταν ο χρήστης δώσει σωστό ελεύθερο χρόνο
                break
            except ValueError:
                print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")

    # Λούπα για την προσθήκη νέου στόχου
    while True:
        try:
            name = input("Δώσε το όνομα του στόχου: ").strip()

            # Έλεγχος αν το όνομα είναι αποδεκτό (μία λέξη χωρίς κενά)
            if not name.replace(" ", "").isalpha():
                raise ValueError("Λάθος όνομα του Task, παρακαλώ γράψτε μια λέξη.")

            hours = float(input("Δώσε την εβδομαδιαία διάρκεια σε ώρες: "))
            # Έλεγχος αν οι ώρες είναι εντός του εύρους [0, 168]
            if not (0 <= hours <= 168):
                raise ValueError("Λάθος αριθμός χρόνου του στόχου.")
            if total_hours + hours > 168:  # Έλεγχος αν οι συνολικές ώρες ξεπερνούν τις 168
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")

            # Έλεγχος αν οι ώρες με το νέο task ξεπερνούν τον ελεύθερο χρόνο
            if total_hours + hours > free_time:
                remaining_free_time = free_time - total_hours  # Υπολογισμός του υπολειπόμενου ελεύθερου χρόνου
                print(f"Δεν μπορείς να ξεπεράσεις τον ελεύθερο χρόνο σου των {free_time} ωρών!")
                print(f"Έχεις ακόμη {remaining_free_time} ώρες ελεύθερου χρόνου διαθέσιμες.")
                break  # Διακόπτουμε την προσθήκη του στόχου αν ξεπερνάει τον ελεύθερο χρόνο

            importance = int(input("Δώσε τον βαθμό σημαντικότητας του στόχου: "))
            # Έλεγχος αν ο βαθμός σημαντικότητας είναι εντός του εύρους [1, 10]
            if not (1 <= importance <= 10):
                raise ValueError("Ο αριθμός πρέπει να είναι απο 1 - 10")

        except ValueError:
            print("Λάθος εισαγωγή, παρακαλώ βάλτε αριθμούς για τις ώρες και την σημαντικότητα.")
            continue

        # Προσθήκη του στόχου στη λίστα
        tasks.append({"name": name, "hours": hours, "importance": importance})
        total_hours += hours  # Ενημέρωση του συνολικού αριθμού ωρών
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        remaining_free_time = free_time - total_hours  # Υπολογισμός του υπολειπόμενου ελεύθερου χρόνου
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
        if task_index < 0 or task_index >= len(tasks):  # Έλεγχος αν ο αριθμός είναι έγκυρος
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    current_task = tasks[task_index]

    # Ζητάμε από τον χρήστη να τροποποιήσει το όνομα, τις ώρες και τη σημαντικότητα
    new_name = input("Δώστε το νέο όνομα του Task: ")
    if(new_name.replace(" ", "").isalpha()):
        current_task['name'] = new_name
    else:
        print("Μη αποδεκτό όνομα.")

    new_hours = float(input("Παρακαλώ, δώστε τις εβδομαδιαίες ώρες: "))
    if 0 <= new_hours <= 168:  # Έλεγχος αν οι νέες ώρες είναι εντός του εύρους [0, 168]
        current_task['hours'] = new_hours
    else:
        print("Άκυρη εισαγωγή ώρας, παρακαλώ προσπαθήστε ξανά.")

    new_importance = int(input("Δώσε τον βαθμό σημαντικότητας του Task: "))
    if 1 <= new_importance <= 10:  # Έλεγχος αν η νέα σημαντικότητα είναι εντός του εύρους [1, 10]
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
        if task_index < 0 or task_index >= len(tasks):  # Έλεγχος αν ο αριθμός είναι έγκυρος
            print("Άκυρη επιλογή, παρακαλώ δώστε τον αριθμό του Task.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    tasks.pop(task_index)  # Διαγραφή του επιλεγμένου στόχου

def sort_by_importance():
    print("\nΈγινε η ταξινόμιση με βάση του πόσο σημαντικό είναι το κάθε Task.\n")
    tasks.sort(key=lambda x: x['importance'], reverse=True)  # Ταξινόμηση των tasks κατά σημαντικότητα (φθίνουσα σειρά)
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']} (Importance: {task['importance']}, Hours: {task['hours']})")

def show_all():
    # Ελέγχουμε αν δεν υπάρχουν tasks στον κατάλογο
    if not tasks:
        print("Δεν υπάρχουν στόχοι.")  # Εκτυπώνουμε μήνυμα αν δεν υπάρχουν tasks
        return  # Επιστρέφουμε για να σταματήσει η συνάρτηση εδώ αν είναι κενό το tasks[]

    print("\n--- Όλοι οι στόχοι ---")  # Εμφανίζουμε τίτλο για να ξέρει ο χρήστης ότι ακολουθεί η λίστα των tasks
    # Διατρέχουμε όλα τα tasks με την μέθοδο enumerate για να έχουμε και τον αριθμό του task (i) και τα δεδομένα του task (task)
    for i, task in enumerate(tasks):
        # Εκτυπώνουμε τα δεδομένα του κάθε task με τις πληροφορίες του (όνομα, ώρες και σημαντικότητα)
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")

def avarage_time():
    if not tasks:
        print("\nΔεν έχουν υποβληθεί Tasks.\n")
    else:    
        global total_hours
        avarage = total_hours / len(tasks)
        print(f"Ο μέσος όρος των Tasks της εβδομάδας είναι:", avarage, "ώρες")

# Κύριος βρόχος του προγράμματος που εκτελεί το μενού και τις επιλογές του χρήστη
while True:
    display_menu()  # Εμφανίζουμε το μενού επιλογών
    user_input = int(input("Επέλεξε έναν αριθμό απο το 1-5: "))  # Ζητάμε από τον χρήστη να κάνει μια επιλογή
    if user_input == 1:
        total_hours = task_add(tasks, total_hours)  # Καλούμε τη συνάρτηση για προσθήκη στόχου
    elif user_input == 2:
        task_edit()  # Καλούμε τη συνάρτηση για τροποποίηση στόχου
    elif user_input == 3:
        task_del()  # Καλούμε τη συνάρτηση για διαγραφή στόχου
    elif user_input == 4:
        sort_by_importance()  # Καλούμε τη συνάρτηση για ταξινόμηση κατά σημαντικότητα
    elif user_input == 5:
        show_all()  # Καλούμε τη συνάρτηση για εμφάνιση όλων των στόχων
    elif user_input == 6:
        avarage_time()
    elif user_input == 7:
        break  # Τερματίζουμε το πρόγραμμα όταν επιλεγεί η έξοδος
