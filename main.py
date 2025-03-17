# Use pip install matplotlib to install the library
import matplotlib.pyplot as plt
# hashlib για να αποθηκεύουμε νέους χρήστες με κωδικό πρόσβασης
import hashlib
# getpass για να κρυφούν οι κωδικοί πρόσβασης με ****
import getpass
# csv για διάβσμα CSV Αρχείων
import csv

users = {}  # Λεξικό για την αποθήκευση χρηστών και των στόχων τους
tasks = []  # Λίστα που αποθηκεύει όλους τους στόχους
total_hours = 0.0  # Μεταβλητή που αποθηκεύει τον συνολικό αριθμό ωρών που έχουν ανατεθεί στους στόχους
free_time = 0  # Αρχικοποιούμε τον ελεύθερο χρόνο σε 0
free_time_set = False

def hash_password(password):
    """
    Κρυπτογραφεί έναν κωδικό πρόσβασης χρησιμοποιώντας τον αλγόριθμο SHA-256.
    
    Args:
        password (str): Ο κωδικός πρόσβασης που εισάγει ο χρήστης.

    Returns:
        str: Η κρυπτογραφημένη τιμή (hash) του κωδικού πρόσβασης.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def input_or_update_free_time(current_user):
    """
    Επιτρέπει στον χρήστη να εισαγάγει ή να ενημερώσει τον διαθέσιμο ελεύθερο χρόνο του.
    Ελέγχει αν η είσοδος είναι έγκυρη και αν η νέα τιμή είναι αρκετή για τα υπάρχοντα tasks.
    """
    # Υπολογισμός του τρέχοντος συνόλου ωρών από τα tasks
    current_tasks = users[current_user]['tasks']
    total_task_hours = sum(task['hours'] for task in current_tasks)
    
    while True:
        try:
            free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
            
            # Έλεγχος εγκυρότητας δεδομένων
            if not 1 <= free_time <= 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            
            # Έλεγχος αν το νέο free_time είναι μικρότερο από τις υπάρχουσες ώρες tasks
            if free_time < total_task_hours:
                print(f"Σφάλμα: Έχεις ήδη {total_task_hours} ώρες σε tasks. "
                      f"Το νέο ελεύθερο χρόνο πρέπει να είναι τουλάχιστον {total_task_hours} ώρες.")
                continue
            
            users[current_user]['free_time'] = free_time
            print(f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες.")
            save_users_to_csv()  # Αποθήκευση αμέσως μετά την ενημέρωση
            break
        
        except ValueError:
            print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")

def input_or_update_free_time(current_user):
    """
    Επιτρέπει στον χρήστη να εισαγάγει ή να ενημερώσει τον διαθέσιμο ελεύθερο χρόνο του.
    Ελέγχει αν η είσοδος είναι έγκυρη και ενημερώνει το προφίλ του χρήστη.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    while True:
        try:
            free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
            
            # Έλεγχος εγκυρότητας δεδομένων
            if not 1 <= free_time <= 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            
            users[current_user]['free_time'] = free_time
            print(f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες.")
            break
        
        except ValueError:
            print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")


def create_new_user():
    """
    Δημιουργεί έναν νέο χρήστη, ζητώντας όνομα χρήστη και κωδικό πρόσβασης.
    Ο κωδικός αποθηκεύεται με κρυπτογράφηση για μεγαλύτερη ασφάλεια.

    Returns:
        None
    """
    username = input("Δώσε το όνομα χρήστη: ").strip()

    # Έλεγχος αν ο χρήστης υπάρχει ήδη
    if username in users:
        print("Ο χρήστης υπάρχει ήδη.")
        return
    
    # Ζητάμε τον κωδικό πρόσβασης και τον αποθηκεύουμε κρυπτογραφημένο
    password = getpass.getpass("Δώσε τον κωδικό πρόσβασης: ").strip()
    password_hash = hash_password(password)
    
    # Αρχικοποίηση του χρήστη με κενή λίστα στόχων και προεπιλεγμένο ελεύθερο χρόνο
    users[username] = {"password": password_hash, "tasks": [], "free_time": 168.0}
    print(f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς.")


def select_user():
    username = input("Δώσε το όνομα χρήστη: ").strip()
    if username in users:
        password = getpass.getpass("Δώσε τον κωδικό πρόσβασης: ").strip()
        if users[username]["password"] == hash_password(password):
            print("Επιτυχής σύνδεση.")
            # Υπολογισμός του συνολικού χρόνου των tasks
            total_task_hours = sum(task["hours"] for task in users[username]["tasks"])
            # Υπολογισμός του υπόλοιπου ελεύθερου χρόνου
            remaining_free_time = users[username]["free_time"] - total_task_hours
            print(f"Ο υπόλοιπος ελεύθερος χρόνος σου είναι: {remaining_free_time} ώρες")
            return username
        else:
            print("Λάθος κωδικός πρόσβασης.")
            return None
    else:
        print("Ο χρήστης δεν βρέθηκε.")
        return None
    

def display_menu():
    """
    Εμφανίζει το μενού επιλογών στον χρήστη για τη διαχείριση του χρόνου και των στόχων του.

    Η συνάρτηση:
    - Εκτυπώνει μια λίστα με τις διαθέσιμες επιλογές που μπορεί να εκτελέσει ο χρήστης.
    - Παρέχει λειτουργίες όπως η προσθήκη, τροποποίηση, διαγραφή και ταξινόμηση στόχων.
    - Επιτρέπει την προβολή γραφημάτων και τον υπολογισμό του μέσου χρόνου των tasks.

    Returns:
        None
    """
    print("\n--- Time Management ---")
    print("1. Εισαγωγή/Ενημέρωση Ελεύθερου Χρόνου")
    print("2. Προσθήκη νέου στόχου")
    print("3. Τροποίηση στόχου")
    print("4. Διαγραφή στόχου")
    print("5. Ταξινόμηση κατά σημαντικότητα")
    print("6. Εκτύπωση όλων των στόχων")
    print("7. Μέσος όρος χρόνου των Task")
    print("8. Γράφημα Πίτας")
    print("9. Γράφημα Στηλών")
    print("10. Έξοδος")

def task_add(tasks, total_hours, current_user):
    """
    Προσθέτει έναν νέο στόχο (task) στη λίστα των στόχων του χρήστη, διασφαλίζοντας ότι:
    - Ο χρήστης έχει ορίσει ελεύθερο χρόνο.
    - Ο νέος στόχος δεν υπερβαίνει τον διαθέσιμο χρόνο.
    - Το όνομα του στόχου είναι μοναδικό και έγκυρο.
    - Η χρονική διάρκεια και η σημαντικότητα του στόχου βρίσκονται εντός επιτρεπτών ορίων.

    Args:
        tasks (list): Η λίστα με τα tasks του χρήστη.
        total_hours (float): Συνολικός αριθμός ωρών που έχουν ήδη κατανεμηθεί σε tasks.
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        float: Ο ενημερωμένος συνολικός αριθμός ωρών μετά την προσθήκη του νέου στόχου.
    """

    # Έλεγχος αν ο χρήστης έχει ορίσει τον διαθέσιμο ελεύθερο χρόνο του
    if users[current_user]['free_time'] == 168.0:  # Αν η τιμή είναι η προεπιλεγμένη, δεν έχει οριστεί ακόμα
        print("Πρέπει πρώτα να ορίσεις τον ελεύθερο χρόνο σου για την εβδομάδα.")
        input_or_update_free_time(current_user)

    # Ανάκτηση του διαθέσιμου ελεύθερου χρόνου του χρήστη
    free_time = users[current_user]['free_time']

    while True:
        try:
            # Ζητάμε από τον χρήστη να εισαγάγει το όνομα του στόχου
            name = input("Δώσε το όνομα του στόχου: ").strip()

            # Έλεγχος αν το όνομα υπάρχει ήδη στη λίστα των tasks
            if any(task['name'] == name for task in tasks):
                raise ValueError("Το όνομα του στόχου υπάρχει ήδη. Παρακαλώ επιλέξτε διαφορετικό όνομα.")

            # Έλεγχος εγκυρότητας ονόματος (δεν επιτρέπονται κενά και μη αλφαβητικοί χαρακτήρες)
            if not name.replace(" ", "").isalpha():
                raise ValueError("Λάθος όνομα του Task, παρακαλώ γράψτε μια λέξη.")

            # Ζητάμε από τον χρήστη να εισαγάγει τον αριθμό των ωρών
            hours = float(input("Δώσε την εβδομαδιαία διάρκεια σε ώρες: "))

            # Έλεγχος αν οι ώρες βρίσκονται στο επιτρεπτό εύρος [0, 168]
            if not (0 <= hours <= 168):
                raise ValueError("Λάθος αριθμός χρόνου του στόχου.")

            # Έλεγχος αν το νέο task ξεπερνά τις 168 ώρες συνολικά
            if total_hours + hours > 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")

            # Έλεγχος αν το νέο task ξεπερνά τον διαθέσιμο ελεύθερο χρόνο του χρήστη
            if total_hours + hours > free_time:
                remaining_free_time = free_time - total_hours
                print(f"Δεν μπορείς να ξεπεράσεις τον ελεύθερο χρόνο σου των {free_time} ωρών!")
                print(f"Έχεις ακόμη {remaining_free_time} ώρες ελεύθερου χρόνου διαθέσιμες.")
                break  # Διακοπή της διαδικασίας αν δεν υπάρχει επαρκής ελεύθερος χρόνος

            # Ζητάμε από τον χρήστη να ορίσει τον βαθμό σημαντικότητας του στόχου
            importance = int(input("Δώσε τον βαθμό σημαντικότητας του στόχου (1-10): "))

            # Έλεγχος αν ο βαθμός σημαντικότητας είναι εντός των αποδεκτών ορίων
            if not (1 <= importance <= 10):
                raise ValueError("Ο αριθμός πρέπει να είναι από 1 έως 10.")

        except ValueError as e:
            print(e)  # Εκτύπωση του μηνύματος σφάλματος που προέκυψε
            continue  # Επανεκκίνηση της διαδικασίας εισαγωγής του task

        # Προσθήκη του νέου στόχου στη λίστα
        tasks.append({"name": name, "hours": hours, "importance": importance})

        # Ενημέρωση του συνολικού αριθμού ωρών που έχουν κατανεμηθεί σε tasks
        total_hours += hours

        # Υπολογισμός και εμφάνιση του υπολειπόμενου ελεύθερου χρόνου
        remaining_free_time = free_time - total_hours
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        print(f"Απομένουν {remaining_free_time} ώρες ελεύθερου χρόνου.")

        # Αποθήκευση των tasks του χρήστη στο αρχείο CSV
        save_tasks_to_csv(current_user)

        break  # Έξοδος από τον βρόχο, καθώς το task προστέθηκε με επιτυχία

    return total_hours  # Επιστροφή του ενημερωμένου συνολικού αριθμού ωρών


def task_edit(current_user):
    """
    Επιτρέπει στον χρήστη να τροποποιήσει έναν υπάρχοντα στόχο (task), αλλάζοντας:
    - Το όνομα του στόχου.
    - Τη χρονική του διάρκεια (ώρες ανά εβδομάδα).
    - Τον βαθμό σημαντικότητας.

    Διασφαλίζεται ότι:
    - Ο χρήστης έχει τουλάχιστον έναν στόχο πριν επιχειρήσει την τροποποίηση.
    - Η νέα χρονική διάρκεια είναι έγκυρη (0-168 ώρες).
    - Η σημαντικότητα του στόχου είναι εντός των επιτρεπτών ορίων (1-10).
    
    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """

    global total_hours  # Επιτρέπει την τροποποίηση της συνολικής διάρκειας των tasks

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν υπάρχουν tasks για επεξεργασία
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return

    # Εμφάνιση των διαθέσιμων tasks για επιλογή
    print("Επέλεξε το Task που θέλεις να τροποποιήσεις: ")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        # Ζητάμε από τον χρήστη να επιλέξει έναν αριθμό task από τη λίστα
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις τροποποίηση: ")) - 1

        # Έλεγχος αν η επιλογή είναι έγκυρη (ο αριθμός είναι εντός των ορίων της λίστας)
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε έναν αριθμό από τη λίστα.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    # Ανάκτηση του task που επιλέχθηκε
    current_task = tasks[task_index]

    # Αφαίρεση των παλιών ωρών του task από το total_hours (πριν γίνει η τροποποίηση)
    total_hours -= current_task['hours']

    # Ζητάμε από τον χρήστη να εισαγάγει νέο όνομα για το task
    new_name = input("Δώστε το νέο όνομα του Task: ").strip()
    if new_name.replace(" ", "").isalpha():
        current_task['name'] = new_name  # Ενημέρωση του ονόματος του task
    else:
        print("Μη αποδεκτό όνομα. Η αλλαγή δεν πραγματοποιήθηκε.")

    try:
        # Ζητάμε από τον χρήστη να εισαγάγει τη νέα διάρκεια σε ώρες
        new_hours = float(input("Παρακαλώ, δώστε τις εβδομαδιαίες ώρες: "))

        # Έλεγχος αν οι νέες ώρες είναι εντός των επιτρεπτών ορίων
        if 0 <= new_hours <= 168:
            current_task['hours'] = new_hours  # Ενημέρωση των ωρών του task
        else:
            raise ValueError("Άκυρη εισαγωγή ώρας. Η τιμή πρέπει να είναι από 0 έως 168.")
    except ValueError:
        print("Άκυρη εισαγωγή ώρας, παρακαλώ προσπαθήστε ξανά.")
        return

    try:
        # Ζητάμε από τον χρήστη να εισαγάγει τη νέα σημαντικότητα του task
        new_importance = int(input("Δώσε τον βαθμό σημαντικότητας του Task (1-10): "))

        # Έλεγχος αν η νέα σημαντικότητα είναι εντός των επιτρεπτών ορίων
        if 1 <= new_importance <= 10:
            current_task['importance'] = new_importance  # Ενημέρωση της σημαντικότητας του task
        else:
            raise ValueError("Άκυρη τιμή σημαντικότητας. Η τιμή πρέπει να είναι από 1 έως 10.")
    except ValueError:
        print("Άκυρη τιμή σημαντικότητας, παρακαλώ προσπαθήστε ξανά.")
        return

    # Προσθήκη των νέων ωρών στο total_hours μετά την τροποποίηση
    total_hours += current_task['hours']
    print("Η τροποποίηση ολοκληρώθηκε επιτυχώς.")

    # Αποθήκευση των ενημερωμένων tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)


def task_del(current_user):
    """
    Διαγράφει έναν επιλεγμένο στόχο (task) από τη λίστα των στόχων του χρήστη.
    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν διαθέσιμοι στόχοι πριν επιτρέψει τη διαγραφή.
    - Εμφανίζει τη λίστα των tasks ώστε ο χρήστης να επιλέξει ποιο θα διαγράψει.
    - Διασφαλίζει ότι η επιλογή είναι έγκυρη.
    - Ενημερώνει τη συνολική κατανομή του χρόνου αφαιρώντας τις ώρες του διαγραμμένου task.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """

    global total_hours  # Επιτρέπει την τροποποίηση της συνολικής διάρκειας των tasks

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν υπάρχουν tasks για διαγραφή
    if not tasks:
        print("Δεν υπάρχουν στόχοι για διαγραφή.")
        return

    # Εμφάνιση της λίστας των διαθέσιμων tasks
    print("Επέλεξε το Task που θέλεις να διαγράψεις: ")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        # Ζητάμε από τον χρήστη να επιλέξει έναν αριθμό task από τη λίστα
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να διαγράψεις: ")) - 1

        # Έλεγχος αν η επιλογή είναι έγκυρη (ο αριθμός είναι εντός των ορίων της λίστας)
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε έναν αριθμό από τη λίστα.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return

    # Αφαίρεση των ωρών του διαγραφόμενου task από το total_hours
    total_hours -= tasks[task_index]['hours']

    # Διαγραφή του επιλεγμένου task από τη λίστα
    deleted_task = tasks.pop(task_index)  # Χρησιμοποιούμε pop για να μπορούμε να δείξουμε ποιο task διαγράφηκε
    print(f"Το Task '{deleted_task['name']}' διαγράφηκε επιτυχώς.")

    # Αποθήκευση των ενημερωμένων tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)


def sort_by_importance(current_user):
    """
    Ταξινομεί τη λίστα των στόχων (tasks) του χρήστη με βάση τον βαθμό σημαντικότητας (importance) 
    σε φθίνουσα σειρά, ώστε οι πιο σημαντικοί στόχοι να εμφανίζονται πρώτοι.

    Η συνάρτηση:
    - Ανακτά τη λίστα των tasks του χρήστη.
    - Ταξινομεί τα tasks με βάση τη σημαντικότητά τους (μεγαλύτερη προς μικρότερη).
    - Εμφανίζει τη νέα ταξινομημένη λίστα των tasks.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Ενημερωτικό μήνυμα για την ταξινόμηση
    print("\nΈγινε η ταξινόμηση με βάση του πόσο σημαντικό είναι το κάθε Task.\n")

    # Ταξινόμηση της λίστας των tasks κατά σημαντικότητα σε φθίνουσα σειρά (από το 10 προς το 1)
    tasks.sort(key=lambda x: x['importance'], reverse=True)

    # Εμφάνιση της ταξινομημένης λίστας των tasks
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']} (Importance: {task['importance']}, Hours: {task['hours']})")


def show_all(current_user):
    tasks = users[current_user]["tasks"]
    if not tasks:
        print("Δεν υπάρχουν στόχοι.")
        return
    print("\n--- Όλοι οι στόχοι ---")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")
    total_task_hours = sum(task["hours"] for task in tasks)
    remaining_free_time = users[current_user]["free_time"] - total_task_hours
    print(f"Υπόλοιπος ελεύθερος χρόνος: {remaining_free_time} ώρες")
    

def average_time(current_user):
    """
    Υπολογίζει και εμφανίζει τον μέσο όρο του χρόνου που αφιερώνεται σε κάθε στόχο (task) 
    του συνδεδεμένου χρήστη.

    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν tasks. Αν όχι, εμφανίζει μήνυμα και τερματίζει.
    - Υπολογίζει το συνολικό χρόνο που έχει αφιερωθεί σε όλα τα tasks.
    - Υπολογίζει και εμφανίζει τον μέσο όρο χρόνου ανά task.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν υπάρχουν καταχωρημένα tasks
    if not tasks:
        print("\nΔεν έχουν υποβληθεί Tasks.\n")
        return

    # Υπολογισμός του συνολικού αριθμού ωρών αφιερωμένων σε όλα τα tasks
    total_hours = sum(task['hours'] for task in tasks)

    # Υπολογισμός του μέσου όρου χρόνου ανά task
    average = total_hours / len(tasks)

    # Εμφάνιση του υπολογισμένου μέσου όρου
    print(f"Ο μέσος όρος των Tasks της εβδομάδας είναι: {average:.2f} ώρες")


def calculate_total_hours(tasks):
    """
    Υπολογίζει το συνολικό αριθμό ωρών που έχουν κατανεμηθεί σε όλα τα tasks.

    Args:
        tasks (list): Λίστα από λεξικά που περιέχουν τα tasks του χρήστη.

    Returns:
        float: Ο συνολικός αριθμός ωρών που αφιερώνονται στα tasks.
    """
    return sum(task['hours'] for task in tasks)


def plot_pie_chart(tasks, free_time):
    """
    Δημιουργεί ένα γράφημα πίτας που απεικονίζει την κατανομή του χρόνου στα tasks του χρήστη.

    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν διαθέσιμα tasks. Αν όχι, εμφανίζει σχετικό μήνυμα.
    - Δημιουργεί ένα γράφημα πίτας, όπου κάθε τομέας αντιπροσωπεύει έναν στόχο με βάση τις ώρες του.
    - Προσθέτει πληροφορίες για το συνολικό χρόνο που έχει διατεθεί και τον υπολειπόμενο ελεύθερο χρόνο.

    Args:
        tasks (list): Λίστα από λεξικά που περιέχουν τα tasks του χρήστη.
        free_time (float): Ο συνολικός διαθέσιμος ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """

    # Υπολογισμός του συνολικού χρόνου που έχει κατανεμηθεί σε tasks
    total_hours = calculate_total_hours(tasks)

    # Έλεγχος αν υπάρχουν tasks για να δημιουργηθεί το γράφημα
    if not tasks:
        print("Δεν υπάρχουν στόχοι για να δημιουργηθεί το γράφημα.")
        return
    
    # Δημιουργία λιστών με τα ονόματα των tasks και τις αντίστοιχες ώρες
    labels = [task['name'] for task in tasks]
    sizes = [task['hours'] for task in tasks]

    # Ορισμός μεγέθους του διαγράμματος
    plt.figure(figsize=(8, 8))
    
    # Τροποποίηση του autopct ώστε να εμφανίζει τόσο το ποσοστό όσο και τις πραγματικές ώρες
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}%\n({val} ώρες)'
        return my_autopct
    
    # Δημιουργία του γραφήματος πίτας
    plt.pie(sizes, labels=labels, autopct=make_autopct(sizes), startangle=140)
    
    # Διατήρηση της αναλογίας του κύκλου
    plt.axis('equal')
    
    # Ορισμός τίτλου γραφήματος
    plt.title('Κατανομή Χρόνου στους Στόχους')

    # Προσθήκη κειμένου που δείχνει το συνολικό διαθέσιμο χρόνο και τον υπολειπόμενο ελεύθερο χρόνο
    plt.text(-1.5, 1.0, f"Συνολικός Χρόνος: {total_hours} ώρες", fontsize=12, color='blue', ha='left')
    plt.text(-1.5, 0.8, f"Ελεύθερος Χρόνος: {free_time - total_hours} ώρες", fontsize=12, color='green', ha='left')

    # Εμφάνιση του γραφήματος
    plt.show()


def plot_bar_chart(tasks, free_time):
    """
    Δημιουργεί ένα γράφημα στήλης που απεικονίζει την κατανομή του χρόνου στα tasks του χρήστη.

    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν διαθέσιμα tasks. Αν όχι, εμφανίζει σχετικό μήνυμα και τερματίζει την εκτέλεση.
    - Δημιουργεί ένα γράφημα στήλης όπου κάθε μπάρα αντιπροσωπεύει έναν στόχο και τις ώρες που έχουν διατεθεί σε αυτόν.
    - Προσθέτει πληροφορίες για το συνολικό χρόνο που έχει διατεθεί και τον υπολειπόμενο ελεύθερο χρόνο.

    Args:
        tasks (list): Λίστα από λεξικά που περιέχουν τα tasks του χρήστη.
        free_time (float): Ο συνολικός διαθέσιμος ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """

    # Υπολογισμός του συνολικού χρόνου που έχει κατανεμηθεί σε tasks
    total_hours = calculate_total_hours(tasks)

    # Έλεγχος αν υπάρχουν tasks για να δημιουργηθεί το γράφημα
    if not tasks:
        print("Δεν υπάρχουν στόχοι για να δημιουργηθεί το γράφημα.")
        return

    # Δημιουργία λιστών με τα ονόματα των στόχων και τις αντίστοιχες ώρες
    x = [task['name'] for task in tasks]  # Ονόματα των στόχων
    y = [task['hours'] for task in tasks]  # Ώρες που αφιερώνονται σε κάθε στόχο

    # Ορισμός του μεγέθους του γραφήματος
    plt.figure(figsize=(10, 6))

    # Δημιουργία γραφήματος στήλης
    plt.bar(x, y, color='b')  
    plt.title('Κατανομή Χρόνου ανά Στόχο')
    plt.xlabel('Όνομα Στόχου')
    plt.ylabel('Ώρες')
    
    # Ρύθμιση των ετικετών του άξονα X για καλύτερη αναγνωσιμότητα
    plt.xticks(rotation=45, ha='right')

    # Προσθήκη πλέγματος στον άξονα Y για βελτίωση της αναγνωσιμότητας των δεδομένων
    plt.grid(axis='y')

    # Προσθήκη πληροφοριών σχετικά με τον συνολικό χρόνο και τον υπολειπόμενο ελεύθερο χρόνο
    plt.text(-1.5, max(y) + 1.3, f"Συνολικός Χρόνος: {total_hours} ώρες", fontsize=12, color='blue')
    plt.text(-1.5, max(y) + 1.1, f"Ελεύθερος Χρόνος: {free_time - total_hours} ώρες", fontsize=12, color='green')

    # Αυτόματη προσαρμογή για να μην κόβονται οι ετικέτες των αξόνων
    plt.tight_layout()

    # Εμφάνιση του γραφήματος
    plt.show()

def save_users_to_csv(filename='users.csv'):
    """
    Αποθηκεύει τα δεδομένα των χρηστών σε ένα αρχείο CSV.

    Η συνάρτηση:
    - Δημιουργεί ή αντικαθιστά το αρχείο CSV με τα στοιχεία των χρηστών.
    - Για κάθε χρήστη, αποθηκεύει το όνομα χρήστη, τον κωδικό πρόσβασης (hashed) και τον διαθέσιμο ελεύθερο χρόνο.

    Args:
        filename (str): Το όνομα του αρχείου CSV όπου θα αποθηκευτούν τα δεδομένα. 
                        Προεπιλεγμένη τιμή: 'users.csv'.

    Returns:
        None
    """

    # Άνοιγμα του αρχείου σε λειτουργία εγγραφής ('w'), με ορισμό newline='' για αποφυγή κενών γραμμών στα Windows
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Εγγραφή των δεδομένων κάθε χρήστη στο αρχείο CSV
        for username, data in users.items():
            writer.writerow([username, data['password'], data['free_time']])


def load_users_from_csv(filename='users.csv'):
    """
    Φορτώνει τα δεδομένα των χρηστών από ένα αρχείο CSV και τα αποθηκεύει στη μεταβλητή users.

    Η συνάρτηση:
    - Διαβάζει το αρχείο CSV γραμμή προς γραμμή.
    - Αν η γραμμή περιέχει τρεις τιμές (όνομα χρήστη, κωδικό πρόσβασης και διαθέσιμο ελεύθερο χρόνο), 
      τις καταχωρεί κανονικά.
    - Αν η γραμμή περιέχει μόνο δύο τιμές (όνομα χρήστη και κωδικό πρόσβασης), 
      ορίζει έναν προεπιλεγμένο ελεύθερο χρόνο (168.0 ώρες).
    - Αν το αρχείο δεν βρεθεί, εμφανίζει σχετικό μήνυμα και δεν φορτώνει δεδομένα.

    Args:
        filename (str): Το όνομα του αρχείου CSV από το οποίο θα φορτωθούν τα δεδομένα. 
                        Προεπιλεγμένη τιμή: 'users.csv'.

    Returns:
        None
    """
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) == 3:
                    username, password_hash, free_time = row
                    users[username] = {
                        "password": password_hash,
                        "tasks": [],
                        "free_time": float(free_time)
                    }
                elif len(row) == 2:
                    # Αν λείπει ο ελεύθερος χρόνος, ορίζεται μια προεπιλεγμένη τιμή 168.0 ώρες
                    username, password_hash = row
                    users[username] = {
                        "password": password_hash,
                        "tasks": [],
                        "free_time": 168.0  
                    }

    except FileNotFoundError:
        print("Το αρχείο χρηστών δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def save_tasks_to_csv(filename='tasks.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for username in users:
            for task in users[username]['tasks']:
                writer.writerow([username, task['name'], task['hours'], task['importance']])


def load_tasks_from_csv(filename='tasks.csv'):
    try:
        # Καθαρισμός των tasks όλων των χρηστών πριν τη φόρτωση
        for username in users:
            users[username]['tasks'] = []
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    username, name, hours, importance = row
                    if username in users:
                        users[username]['tasks'].append({
                            "name": name,
                            "hours": float(hours),
                            "importance": int(importance)
                        })
    except FileNotFoundError:
        print("Το αρχείο στόχων δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def main():
    global total_hours
    load_users_from_csv()
    load_tasks_from_csv()

    while True:
        print("\n--- Καλώς ήρθατε στο Time Management ---")
        print("1. Εγγραφή νέου χρήστη")
        print("2. Σύνδεση")
        print("3. Έξοδος")

        choice = input("Επέλεξε μια επιλογή (1-3): ").strip()

        if choice == '1':
            create_new_user()
            save_users_to_csv()
        elif choice == '2':
            current_user = select_user()
            if current_user:
                total_hours = calculate_total_hours(users[current_user]['tasks'])
                
                while True:
                    display_menu()
                    try:
                        user_input = int(input("Επέλεξε έναν αριθμό από το 1-10: "))
                    except ValueError:
                        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
                        continue

                    if user_input == 1:
                        input_or_update_free_time(current_user)
                    elif user_input == 10:
                        break
                    elif user_input == 2:
                        total_hours = task_add(users[current_user]['tasks'], total_hours, current_user)
                    elif user_input == 3:
                        task_edit(current_user)
                    elif user_input == 4:
                        task_del(current_user)
                    elif user_input == 5:
                        sort_by_importance(current_user)
                    elif user_input == 6:
                        show_all(current_user)
                    elif user_input == 7:
                        average_time(current_user)
                    elif user_input == 8:
                        plot_pie_chart(users[current_user]['tasks'], users[current_user]['free_time'])
                    elif user_input == 9:
                        plot_bar_chart(users[current_user]['tasks'], users[current_user]['free_time'])
                    else:
                        print("Παρακαλώ επέλεξε έναν αριθμό από 1 έως 10.")
        elif choice == '3':
            save_users_to_csv()
            save_tasks_to_csv()
            break
        else:
            print("Παρακαλώ επέλεξε μια έγκυρη επιλογή.")

    save_users_to_csv()
    if 'current_user' in locals():
        save_tasks_to_csv(current_user)

if __name__ == "__main__":
    main()  # Καλέστε μόνο τη main, όχι τις load_ συναρτήσεις ξανά