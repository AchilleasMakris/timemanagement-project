import matplotlib.pyplot as plt  # Για τη δημιουργία γραφημάτων (πίτας και στηλών)
import hashlib  # Για την κρυπτογράφηση κωδικών πρόσβασης με τον αλγόριθμο SHA-256
import getpass  # Για την ασφαλή εισαγωγή κωδικών πρόσβασης χωρίς εμφάνιση στην οθόνη
import csv  # Για την ανάγνωση και εγγραφή δεδομένων σε αρχεία CSV

users = {}  # Λεξικό που αποθηκεύει πληροφορίες χρηστών: κωδικούς, tasks και ελεύθερο χρόνο

def hash_password(password):
    """
    Κρυπτογραφεί έναν κωδικό πρόσβασης χρησιμοποιώντας τον αλγόριθμο SHA-256.
    
    Args:
        password (str): Ο κωδικός πρόσβασης που εισάγει ο χρήστης.

    Returns:
        str: Η κρυπτογραφημένη τιμή (hash) του κωδικού πρόσβασης.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def set_free_time(current_user, free_time_str):
    """
    Διαχειρίζεται τον ελεύθερο χρόνο του χρήστη. Αν δοθεί current_user, ενημερώνει το λεξικό users.
    Διαφορετικά, επιστρέφει μόνο την τιμή του ελεύθερου χρόνου.

    Args:
        current_user (str, optional): Το όνομα του συνδεδεμένου χρήστη. Αν None, δεν ενημερώνεται το λεξικό.

    Returns:
        float: Ο αριθμός των ωρών που δηλώνει ο χρήστης ως διαθέσιμες.
    """
    try:
        free_time = float(free_time_str)  # Μετατροπή της εισόδου σε αριθμό
        if not 1 <= free_time <= 168:
            return False, "Ο ελεύθερος χρόνος πρέπει να είναι από 1 έως 168."
        users[current_user]['free_time'] = free_time  # Αποθήκευση δεδομένων
        save_users_to_csv()  # Υποθετική συνάρτηση αποθήκευσης
        return True, f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες."
    except ValueError:
        return False, "Λάθος εισαγωγή. Πρέπει να είναι αριθμός."

def create_new_user(username, password):
    """
    Δημιουργεί έναν νέο χρήστη με το δοθέν όνομα χρήστη και κωδικό πρόσβασης.

    Args:
        username (str): Το όνομα χρήστη.
        password (str): Ο κωδικός πρόσβασης.

    Returns:
        tuple: (bool, str) - Επιτυχία και μήνυμα.
    """
    if username in users:
        return False, "Ο χρήστης υπάρχει ήδη."
    if not username or not password:
        return False, "Το όνομα χρήστη και ο κωδικός δεν μπορούν να είναι κενά."
    password_hash = hash_password(password)
    users[username] = {"password": password_hash, "tasks": [], "free_time": 0.0}
    save_users_to_csv()  # Αποθήκευση του νέου χρήστη στο αρχείο CSV
    return True, f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς."
    

def select_user():
    """
    Επιτρέπει τη σύνδεση χρήστη μέσω ονόματος και κωδικού πρόσβασης.
    Επιστρέφει το όνομα χρήστη αν η σύνδεση είναι επιτυχής.

    Returns:
        str or None: Το όνομα του χρήστη αν η σύνδεση πετύχει, αλλιώς None.
    """
    username = input("Δώσε το όνομα χρήστη: ").strip()
    if username in users:
        password = getpass.getpass("Δώσε τον κωδικό πρόσβασης: ").strip()
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
    Εμφανίζει το κύριο μενού επιλογών για τη διαχείριση του χρόνου και των στόχων.

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

def task_add(current_user, name, hours, importance):
    """
    Προσθέτει έναν νέο στόχο στη λίστα του χρήστη, ελέγχοντας τον διαθέσιμο ελεύθερο χρόνο.

    Args:
        tasks (list): Η λίστα των tasks του χρήστη.
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    free_time = users[current_user]['free_time']


  # Έλεγχος αν ο ελεύθερος χρόνος έχει οριστεί
    if free_time == 168.0:
        return False, "Πρέπει πρώτα να ορίσεις τον ελεύθερο χρόνο σου για την εβδομάδα."

    # Έλεγχος αν το όνομα υπάρχει ήδη
    if any(task['name'] == name for task in tasks):
        return False, "Το όνομα του στόχου υπάρχει ήδη. Παρακαλώ επιλέξτε διαφορετικό όνομα."
    # Επικύρωση του ονόματος
    if not name.replace(" ", "").isalpha():
        return False, "Λάθος όνομα του Task, παρακαλώ γράψτε μια λέξη."
    
    # Επικύρωση των ωρών
    if not (0 <= hours <= 168):
        return False, "Λάθος αριθμός χρόνου του στόχου. Πρέπει να είναι από 0 έως 168."
    # Υπολογισμός του τρέχοντος συνόλου ωρών
    current_total = sum(task['hours'] for task in tasks)
    if current_total + hours > 168:
        return False, "Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!"

    # Έλεγχος ελεύθερου χρόνου
    if current_total + hours > free_time:
        remaining_free_time = free_time - current_total
        return False, f"Δεν μπορείς να ξεπεράσεις τον ελεύθερο χρόνο σου των {free_time} ωρών! Έχεις ακόμη {remaining_free_time} ώρες ελεύθερου χρόνου διαθέσιμες."

    # Επικύρωση σημαντικότητας
    if not (1 <= importance <= 10):
        return False, "Ο αριθμός πρέπει να είναι από 1 έως 10."

    # Προσθήκη του στόχου και αποθήκευση
    tasks.append({"name": name, "hours": hours, "importance": importance})
    remaining_free_time = free_time - (current_total + hours)
    save_tasks_to_csv()
    return True, f"Task added: {name}, Hours: {hours}, Importance: {importance}\nΑπομένουν {remaining_free_time} ώρες ελεύθερου χρόνου."

def task_edit(current_user):
    """
    Επιτρέπει την τροποποίηση ενός υπάρχοντος στόχου (task) του χρήστη.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    if not tasks:
        print("Δεν υπάρχουν στόχοι για τροποποίηση.")
        return
    
    print("Επέλεξε το Task που θέλεις να τροποποιήσεις: ")

    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")
    print("Επέλεξε 0 για να πας στο αρχικό μενού.")
 

    try:
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να κάνεις τροποποίηση: ")) - 1
        #TODO Fix the indexing so we dont subtract 1
        # αν ο χρήστης εισάγει 0, τότε πάει στο αρχικό μενού.
        # βάλαμε -1 επειδή αφαιρούμε 1 απο το task_index....
        if task_index == -1:
            print("Επιστροφή στο αρχικό μενού.")
            return
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε έναν αριθμό από τη λίστα.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return
    current_task = tasks[task_index]
    new_name = input("Δώστε το νέο όνομα του Task: ").strip()
    if new_name.replace(" ", "").isalpha():
        current_task['name'] = new_name
    else:
        print("Μη αποδεκτό όνομα. Η αλλαγή δεν πραγματοποιήθηκε.")
        return
    try:
        new_hours = float(input("Παρακαλώ, δώστε τις εβδομαδιαίες ώρες: "))
        if 0 <= new_hours <= 168:
            current_task['hours'] = new_hours
        else:
            raise ValueError("Άκυρη εισαγωγή ώρας. Η τιμή πρέπει να είναι από 0 έως 168.")
    except ValueError:
        print("Άκυρη εισαγωγή ώρας, παρακαλώ προσπαθήστε ξανά.")
        return
    try:
        new_importance = int(input("Δώσε τον βαθμό σημαντικότητας του Task (1-10): "))
        if 1 <= new_importance <= 10:
            current_task['importance'] = new_importance
        else:
            raise ValueError("Άκυρη τιμή σημαντικότητας. Η τιμή πρέπει να είναι από 1 έως 10.")
    except ValueError:
        print("Άκυρη τιμή σημαντικότητας, παρακαλώ προσπαθήστε ξανά.")
        return
    print("Η τροποποίηση ολοκληρώθηκε επιτυχώς.")
    save_tasks_to_csv()  # Αποθήκευση των αλλαγών στο αρχείο CSV

def task_del(current_user):
    """
    Διαγράφει έναν επιλεγμένο στόχο από τη λίστα του χρήστη.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    if not tasks:
        print("Δεν υπάρχουν στόχοι για διαγραφή.")
        return
    print("Επέλεξε το Task που θέλεις να διαγράψεις: ")

    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']}")
    print("Επέλεξε 0 για να πας στο αρχικό μενού.")

    try:
        task_index = int(input("Δώσε τον αριθμό του Task που θέλεις να διαγράψεις: ")) - 1
        if task_index == -1:
            print("Επιστροφή στο αρχικό μενού.")
            return
        if task_index < 0 or task_index >= len(tasks):
            print("Άκυρη επιλογή, παρακαλώ δώστε έναν αριθμό από τη λίστα.")
            return
    except ValueError:
        print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
        return
    deleted_task = tasks.pop(task_index)
    print(f"Το Task '{deleted_task['name']}' διαγράφηκε επιτυχώς.")
    save_tasks_to_csv()  # Αποθήκευση των αλλαγών στο αρχείο CSV

def sort_by_importance(current_user):
    """
    Ταξινομεί τους στόχους του χρήστη με βάση τη σημαντικότητά τους (descending).

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    print("\nΈγινε η ταξινόμηση με βάση του πόσο σημαντικό είναι το κάθε Task.\n")
    tasks.sort(key=lambda x: x['importance'], reverse=True)
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']} (Importance: {task['importance']}, Hours: {task['hours']})")

def show_all(current_user):
    """
    Εμφανίζει όλους τους στόχους του χρήστη μαζί με τον ελεύθερο χρόνο του.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    free_time = users[current_user]['free_time']
    if not tasks:
        print("Δεν υπάρχουν στόχοι.")
        return
    print("\n--- Όλοι οι στόχοι ---")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")
    total_task_hours = sum(task['hours'] for task in tasks)  # Υπολογισμός σύνολο ωρών στόχων
    remaining_free_time = free_time - total_task_hours       # Υπολογισμός ελεύθερου χρόνου που απομένει
    print(f"Συνολικός ελεύθερος χρόνος: {free_time} ώρες")
    print(f"Ελεύθερος χρόνος που απομένει: {remaining_free_time} ώρες")

def average_time(current_user):
    """
    Υπολογίζει και εμφανίζει τον μέσο όρο των ωρών που αφιερώνονται στα tasks.

    Args:
        current_user (str): Το όνομα του συνδεδεμένου χρήστη.

    Returns:
        None
    """
    tasks = users[current_user]['tasks']
    if not tasks:
        print("\nΔεν έχουν υποβληθεί Tasks.\n")
        return
    total_hours = sum(task['hours'] for task in tasks)
    average = total_hours / len(tasks)
    print(f"Ο μέσος όρος των Tasks της εβδομάδας είναι: {average:.2f} ώρες")

def plot_pie_chart(tasks, free_time):
    """
    Δημιουργεί ένα γράφημα πίτας που δείχνει την κατανομή του χρόνου.

    Args:
        tasks (list): Λίστα με τα tasks του χρήστη.
        free_time (float): Ο συνολικός ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """
    # Έλεγχος αν υπάρχουν tasks
    if not tasks:
        print("Δεν υπάρχουν στόχοι για απεικόνιση.")
        return
    
    # Δημιουργία λιστών για ετικέτες και μεγέθη
    labels = [task['name'] for task in tasks] + ["Ελεύθερος χρόνος"]
    sizes = [task['hours'] for task in tasks] + [free_time - sum(task['hours'] for task in tasks)]
    
    # Προσαρμοσμένη συνάρτηση για εμφάνιση ωρών
    def autopct_format(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return f"{absolute} ώρες"
    
    # Δημιουργία γράφηματος πίτας
    plt.pie(sizes, labels=labels, autopct=lambda pct: autopct_format(pct, sizes))
    plt.title("Κατανομή Χρόνου")
    plt.show()

def plot_bar_chart(tasks, free_time):
    """
    Δημιουργεί ένα γράφημα στηλών που δείχνει τις ώρες ανά στόχο.

    Args:
        tasks (list): Λίστα με τα tasks του χρήστη.
        free_time (float): Ο συνολικός ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """
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
    Αποθηκεύει τα δεδομένα των χρηστών (όνομα, κωδικό, ελεύθερο χρόνο) σε αρχείο CSV.

    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: 'users.csv'.

    Returns:
        None
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, data in users.items():
            writer.writerow([username, data['password'], data['free_time']])

def load_users_from_csv(filename='users.csv'):
    """
    Φορτώνει τα δεδομένα των χρηστών από ένα αρχείο CSV στο λεξικό users.

    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: 'users.csv'.

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
    except FileNotFoundError:
        print("Το αρχείο χρηστών δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def save_tasks_to_csv(filename='tasks.csv'):
    """
    Αποθηκεύει τα tasks όλων των χρηστών σε αρχείο CSV.

    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: 'tasks.csv'.

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
    Φορτώνει τα tasks των χρηστών από ένα αρχείο CSV στο λεξικό users.

    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: 'tasks.csv'.

    Returns:
        None
    """
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
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
    except FileNotFoundError:
        print("Το αρχείο στόχων δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def main():
    """
    Κύρια συνάρτηση που εκτελεί το πρόγραμμα Time Management.
    Φορτώνει δεδομένα, εμφανίζει το μενού και διαχειρίζεται τις επιλογές του χρήστη.
    """
    load_users_from_csv()  # Φόρτωση δεδομένων χρηστών από το CSV
    load_tasks_from_csv()  # Φόρτωση tasks από το CSV
    
if __name__ == "__main__":
    main()  # Εκκίνηση του προγράμματος