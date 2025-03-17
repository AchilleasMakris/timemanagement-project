# Use pip install matplotlib to install the library
import matplotlib.pyplot as plt
# hashlib για να αποθηκεύουμε νέους χρήστες με κωδικό πρόσβασης
import hashlib
# getpass για να κρυφούν οι κωδικοί πρόσβασης με ****
import getpass
import csv

users = {}  # Λεξικό για την αποθήκευση χρηστών και των στόχων τους
tasks = []  # Λίστα που αποθηκεύει όλους τους στόχους
total_hours = 0.0  # Μεταβλητή που αποθηκεύει τον συνολικό αριθμό ωρών που έχουν ανατεθεί στους στόχους
free_time_flag = False  # Σημαία που δείχνει αν ο ελεύθερος χρόνος έχει οριστεί
free_time = 0  # Αρχικοποιούμε τον ελεύθερο χρόνο σε 0


def hash_password(password):
    """
    Κρυπτογραφεί έναν κωδικό πρόσβασης χρησιμοποιώντας τον αλγόριθμο SHA-256.
    
    Args:
        password (str): Ο κωδικός πρόσβασης που εισάγει ο χρήστης.

    Returns:
        str: Η κρυπτογραφημένη τιμή (hash) του κωδικού πρόσβασης.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def manage_free_time(current_user=None):
    """
    Διαχειρίζεται τον ελεύθερο χρόνο του χρήστη. Αν δοθεί current_user, ενημερώνει το λεξικό users.
    Διαφορετικά, επιστρέφει μόνο την τιμή του ελεύθερου χρόνου.

    Args:
        current_user (str, optional): Το όνομα του συνδεδεμένου χρήστη. Αν None, δεν ενημερώνεται το λεξικό.

    Returns:
        float: Ο αριθμός των ωρών που δηλώνει ο χρήστης ως διαθέσιμες.
    """
    while True:
        try:
            free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
            
            # Έλεγχος εγκυρότητας δεδομένων
            if not 1 <= free_time <= 168:
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            
            # Αν δοθεί current_user, ενημερώνουμε το λεξικό users
            if current_user:
                users[current_user]['free_time'] = free_time
                print(f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες.")
            
            return free_time
        
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
    """
    Επιτρέπει σε έναν χρήστη να συνδεθεί στο σύστημα εισάγοντας όνομα χρήστη και κωδικό πρόσβασης.
    Ελέγχει τα στοιχεία και επιστρέφει το όνομα του χρήστη αν η σύνδεση είναι επιτυχής.

    Returns:
        str or None: Το όνομα του χρήστη αν η σύνδεση είναι επιτυχής, διαφορετικά None.
    """
    username = input("Δώσε το όνομα χρήστη: ").strip()

    # Έλεγχος αν ο χρήστης υπάρχει
    if username in users:
        password = getpass.getpass("Δώσε τον κωδικό πρόσβασης: ").strip()

        # Έλεγχος αν ο κωδικός πρόσβασης είναι σωστός
        if users[username]["password"] == hash_password(password):
            print("Επιτυχής σύνδεση.")
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
        manage_free_time(current_user)

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


def task_edit(current_user, total_hours):
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
        total_hours (float): Ο τρέχων συνολικός αριθμός ωρών που έχουν ανατεθεί στους στόχους.

    Returns:
        float: Ο ενημερωμένος συνολικός αριθμός ωρών μετά την τροποποίηση.
    """

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν υπάρχουν tasks για επεξεργασία
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return total_hours  # Επιστρέφουμε την τρέχουσα total_hours χωρίς αλλαγή

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
            return total_hours  # Επιστρέφουμε την τρέχουσα total_hours χωρίς αλλαγή
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return total_hours  # Επιστρέφουμε την τρέχουσα total_hours χωρίς αλλαγή

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
        # Επαναφορά των παλιών ωρών στο total_hours
        total_hours += current_task['hours']
        return total_hours

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
        # Επαναφορά των παλιών ωρών στο total_hours
        total_hours += current_task['hours']
        return total_hours

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
        # Επαναφορά των παλιών ωρών στο total_hours
        total_hours += current_task['hours']
        return total_hours

    # Προσθήκη των νέων ωρών στο total_hours μετά την τροποποίηση
    total_hours += current_task['hours']
    print("Η τροποποίηση ολοκληρώθηκε επιτυχώς.")

    # Αποθήκευση των ενημερωμένων tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)
    
    # Επιστρέφουμε την ενημερωμένη total_hours
    return total_hours


def task_del(current_user, total_hours):
    """
    Διαγράφει έναν επιλεγμένο στόχο (task) από τη λίστα των στόχων του χρήστη.
    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν διαθέσιμοι στόχοι πριν επιτρέψει τη διαγραφή.
    - Εμφανίζει τη λίστα των tasks ώστε ο χρήστης να επιλέξει ποιο θα διαγράψει.
    - Διασφαλίζει ότι η επιλογή είναι έγκυρη.
    - Ενημερώνει τη συνολική κατανομή του χρόνου αφαιρώντας τις ώρες του διαγραμμένου task.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.
        total_hours (float): Ο τρέχων συνολικός αριθμός ωρών που έχουν ανατεθεί στους στόχους.

    Returns:
        float: Ο ενημερωμένος συνολικός αριθμός ωρών μετά τη διαγραφή.
    """

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν υπάρχουν tasks για διαγραφή
    if not tasks:
        print("Δεν υπάρχουν στόχοι για διαγραφή.")
        return total_hours

    # Εμφάνιση της λίστας των διαθέσιμων tasks
    print("Επέλεξε το Task που θέλεις να διαγράψεις: ")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")

    try:
        # Ζητάμε από τον χρήστη να επιλέξει έναν αριθμό task από τη λίστα
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να διαγράψεις: ")) - 1

        # Έλεγχος αν η επιλογή είναι έγκυρη
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε έναν αριθμό από τη λίστα.")
            return total_hours
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return total_hours

    # Αφαίρεση των ωρών του διαγραφόμενου task από το total_hours
    total_hours -= tasks[task_index]['hours']

    # Διαγραφή του επιλεγμένου task από τη λίστα
    deleted_task = tasks.pop(task_index)
    print(f"Το Task '{deleted_task['name']}' διαγράφηκε επιτυχώς.")

    # Αποθήκευση των ενημερωμένων tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)

    # Επιστροφή της ενημερωμένης total_hours
    return total_hours


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
    """
    Εμφανίζει τη λίστα με όλους τους στόχους (tasks) του συνδεδεμένου χρήστη.
    
    Η συνάρτηση:
    - Ελέγχει αν υπάρχουν καταχωρημένοι στόχοι. Αν όχι, εμφανίζει σχετικό μήνυμα.
    - Εμφανίζει τη λίστα των tasks μαζί με τις ώρες και τη σημαντικότητά τους.
    - Προαιρετικά, μπορεί να προστεθεί εμφάνιση του συνολικού διαθέσιμου ελεύθερου χρόνου.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """

    # Ανάκτηση της λίστας των tasks του χρήστη
    tasks = users[current_user]['tasks']

    # Έλεγχος αν η λίστα είναι κενή
    if not tasks:
        print("Δεν υπάρχουν στόχοι.")
        return  # Διακοπή της εκτέλεσης αν δεν υπάρχουν καταχωρημένα tasks

    # Εμφάνιση τίτλου πριν την εκτύπωση των tasks
    print("\n--- Όλοι οι στόχοι ---")

    # Διατρέχουμε όλα τα tasks χρησιμοποιώντας enumerate για αρίθμηση
    for i, task in enumerate(tasks):
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")


    print(f"Συνολικός ελεύθερος χρόνος: {users[current_user]['free_time']} ώρες")


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


# Plot pie chart
def plot_pie_chart(tasks, free_time):
    if not tasks:
        print("Δεν υπάρχουν στόχοι για απεικόνιση.")
        return
    labels = [task['name'] for task in tasks] + ["Ελεύθερος χρόνος"]
    sizes = [task['hours'] for task in tasks] + [free_time - sum(task['hours'] for task in tasks)]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Κατανομή Χρόνου")
    plt.show()

# Plot bar chart
def plot_bar_chart(tasks, free_time):
    if not tasks:
        print("Δεν υπάρχουν στόχοι για απεικόνιση.")
        return
    names = [task['name'] for task in tasks]
    hours = [task['hours'] for task in tasks]
    plt.bar(names, hours)
    plt.axhline(y=free_time, color='r', linestyle='--', label='Ελεύθερος Χρόνος')
    plt.xlabel("Στόχοι")
    plt.ylabel("Ώρες")
    plt.title("Ώρες ανά Στόχο")
    plt.legend()
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

def save_tasks_to_csv(username, filename='tasks.csv'):
    """
    Αποθηκεύει τα tasks ενός συγκεκριμένου χρήστη σε αρχείο CSV.

    Η συνάρτηση:
    - Ανοίγει το αρχείο CSV σε λειτουργία εγγραφής ('w'), αντικαθιστώντας τυχόν προηγούμενα δεδομένα.
    - Γράφει κάθε task του χρήστη ως ξεχωριστή γραμμή στο αρχείο, αποθηκεύοντας:
      - Το όνομα χρήστη
      - Το όνομα του task
      - Τις ώρες που έχουν αφιερωθεί στο task
      - Τη σημαντικότητα του task

    Args:
        username (str): Το όνομα του χρήστη του οποίου τα tasks θα αποθηκευτούν.
        filename (str): Το όνομα του αρχείου CSV στο οποίο θα γίνει η αποθήκευση. 
                        Προεπιλεγμένη τιμή: 'tasks.csv'.

    Returns:
        None
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        for username, data in users.items():
            for task in data['tasks']:
                writer.writerow([username, task['name'], task['hours'], task['importance']])


def load_tasks_from_csv(filename='tasks.csv'):
    """
    Φορτώνει τα tasks των χρηστών από ένα αρχείο CSV και τα αποθηκεύει στη δομή δεδομένων users.

    Η συνάρτηση:
    - Προσπαθεί να ανοίξει το αρχείο CSV σε λειτουργία ανάγνωσης ('r').
    - Διαβάζει κάθε γραμμή του αρχείου, η οποία περιέχει:
      - Το όνομα χρήστη
      - Το όνομα του task
      - Τις ώρες που έχουν αφιερωθεί στο task
      - Τη σημαντικότητα του task
    - Αν ο χρήστης υπάρχει ήδη στη δομή users, προσθέτει το task στη λίστα του.
    - Αν το αρχείο δεν βρεθεί, εμφανίζει κατάλληλο μήνυμα και δεν εκτελείται καμία φόρτωση.

    Args:
        filename (str): Το όνομα του αρχείου CSV από το οποίο θα διαβαστούν τα tasks.
                        Προεπιλεγμένη τιμή: 'tasks.csv'.

    Returns:
        None
    """
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            
            # Καθαρισμός των tasks για όλους τους χρήστες
            for user in users.values():
                user['tasks'] = []
            
            for row in reader:
                if len(row) == 4:
                    username, name, hours, importance = row
                    if username in users:
                        users[username]['tasks'].append({
                            "name": name,
                            "hours": float(hours),
                            "importance": int(importance)
                        })
                    else:
                        print(f"Προειδοποίηση: Ο χρήστης '{username}' δεν βρέθηκε στη βάση δεδομένων.")
                else:
                    print("Σφάλμα: Εσφαλμένη μορφή δεδομένων στο αρχείο CSV.")
    except FileNotFoundError:
        print("Το αρχείο στόχων δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def main():
    total_hours = 0.0
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
        elif choice == '2':
            current_user = select_user()
            if current_user:
                while True:
                    display_menu()
                    user_input = int(input("Επέλεξε έναν αριθμό από το 1-10: "))
                    if user_input == 1:
                        manage_free_time(current_user)
                    elif user_input == 2:
                        total_hours = task_add(users[current_user]['tasks'], total_hours, current_user)
                    elif user_input == 3:
                        total_hours = task_edit(current_user, total_hours)
                    elif user_input == 4:
                        total_hours = task_del(current_user, total_hours)
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
                    elif user_input == 10:
                        break
        elif choice == '3':
            break
        else:
            print("Παρακαλώ επέλεξε μια έγκυρη επιλογή.")

    # Αποθήκευση όλων των δεδομένων στο τέλος
    save_users_to_csv()
    save_tasks_to_csv(current_user)

if __name__ == "__main__":
    main()