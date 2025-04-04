import hashlib
import csv

# Λεξικό για την αποθήκευση των χρηστών
users = {}

# Συνάρτηση για την κρυπτογράφηση κωδικών πρόσβασης
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Συνάρτηση για τη δημιουργία νέου χρήστη
def create_user(username, password):
    if username in users:
        return False, "Ο χρήστης υπάρχει ήδη."
    if not username or not password:
        return False, "Το όνομα χρήστη και ο κωδικός δεν μπορούν να είναι κενά."
    password_hash = hash_password(password)
    users[username] = {
        "password": password_hash,
        "free_time": 0.0,
        "obligations": [],  # Λίστα για τις υποχρεώσεις
        "activities": []    # Λίστα για τις δραστηριότητες ελεύθερου χρόνου
    }
    return True, "Ο χρήστης δημιουργήθηκε επιτυχώς."

# Συνάρτηση για τη σύνδεση χρήστη
def login_user(username, password):
    username = username.strip()
    password = password.strip()
    print(f"Login attempt: username='{username}', password={'*' * len(password)}")
    if username not in users:
        print("User not found")
        return False, "User does not exist."
    stored_hash = users[username]["password"]
    if stored_hash == hash_password(password):
        print("Login successful")
        return True, "Login successful."
    print("Login failed: incorrect password")
    return False, "Incorrect password."

# Συνάρτηση για τον ορισμό ελεύθερου χρόνου
def set_free_time(username, free_time_str):
    try:
        free_time = float(free_time_str)
        if not 0 <= free_time <= 168:
            return False, "Ο ελεύθερος χρόνος πρέπει να είναι από 0 έως 168 ώρες."
        users[username]["free_time"] = free_time
        return True, "Ο ελεύθερος χρόνος ενημερώθηκε επιτυχώς."
    except ValueError:
        return False, "Παρακαλώ εισάγετε έναν έγκυρο αριθμό."

# Συνάρτηση για την επικύρωση του ονόματος του task
def validate_task_name(username, name, task_type):
    tasks = users[username]["obligations"] if task_type == "υποχρεωση" else users[username]["activities"]
    if any(task["name"] == name for task in tasks):
        return False, "Το όνομα του task υπάρχει ήδη σε αυτή την κατηγορία."
    if not name.replace(" ", "").isalpha():
        return False, "Το όνομα του task πρέπει να περιέχει μόνο γράμματα."
    return True, ""

# Συνάρτηση για την επικύρωση των ωρών
def validate_hours(username, hours):
    try:
        hours = float(hours)
        if not 0 < hours <= 168:
            return False, "Οι ώρες πρέπει να είναι μεταξύ 1 και 168."
        current_total = sum(task["hours"] for task in users[username]["obligations"] + users[username]["activities"])
        free_time = users[username]["free_time"]
        if current_total + hours > free_time:
            return False, f"Δεν μπορείτε να ξεπεράσετε τον ελεύθερο χρόνο σας ({free_time} ώρες)."
        return True, ""
    except ValueError:
        return False, "Παρακαλώ εισάγετε έναν έγκυρο αριθμό για τις ώρες."

# Συνάρτηση για την επικύρωση της σημαντικότητας
def validate_importance(importance):
    try:
        importance = int(importance)
        if not 1 <= importance <= 10:
            return False, "Η σημαντικότητα πρέπει να είναι από 1 έως 10."
        return True, ""
    except ValueError:
        return False, "Παρακαλώ εισάγετε έναν έγκυρο αριθμό για τη σημαντικότητα."

def validate_task_type(task_type):
    if task_type == "1":
        return True, "υποχρεωση"
    elif task_type == "2":
        return True, "δραστηριοτητα ελευθερου χρονου"
    else:
        return False, "Άκυρος τύπος task. Επιλέξτε '1' για υποχρέωση ή '2' για δραστηριότητα ελεύθερου χρόνου."

# Συνάρτηση για την προσθήκη task
def add_task(username, name, hours, importance, task_type):
    if users[username]["free_time"] == 0.0:
        return False, "Πρέπει πρώτα να ορίσετε τον ελεύθερο χρόνο σας."
    
    valid_type, task_category = validate_task_type(task_type)
    if not valid_type:
        return False, task_category  # Επιστρέφει το μήνυμα σφάλματος αν ο τύπος είναι άκυρος
    
    valid_name, msg = validate_task_name(username, name, task_category)
    if not valid_name:
        return False, msg
    
    valid_hours, msg = validate_hours(username, hours)
    if not valid_hours:
        return False, msg
    
    valid_importance, msg = validate_importance(importance)
    if not valid_importance:
        return False, msg
    
    task = {"name": name, "hours": float(hours), "importance": int(importance)}
    
    if task_category == "υποχρεωση":
        users[username]["obligations"].append(task)
    else:
        users[username]["activities"].append(task)
    
    return True, "Το task προστέθηκε επιτυχώς."

def task_edit(username, task_type, task_index, new_name=None, new_hours=None, new_importance=None):
    # Επιλογή της κατάλληλης λίστας tasks με βάση τον τύπο
    if task_type == "1":
        tasks = users[username]["obligations"]
        task_category = "υποχρεωση"
    elif task_type == "2":
        tasks = users[username]["activities"]
        task_category = "δραστηριοτητα ελευθερου χρονου"
    else:
        return False, "Άκυρος τύπος task."

    # Έλεγχος αν ο δείκτης είναι έγκυρος
    if task_index < 0 or task_index >= len(tasks):
        return False, "Άκυρος αριθμός task."

    task = tasks[task_index]

    # Τροποποίηση του ονόματος, αν δόθηκε νέο
    if new_name is not None:
        valid_name, msg = validate_task_name(username, new_name, task_category)
        if not valid_name:
            return False, msg
        task["name"] = new_name

    # Τροποποίηση των ωρών, αν δόθηκαν νέες
    if new_hours is not None:
        valid_hours, msg = validate_hours(username, new_hours)
        if not valid_hours:
            return False, msg
        task["hours"] = float(new_hours)

    # Τροποποίηση της σημαντικότητας, αν δόθηκε νέα
    if new_importance is not None:
        valid_importance, msg = validate_importance(new_importance)
        if not valid_importance:
            return False, msg
        task["importance"] = int(new_importance)

    return True, "Το task τροποποιήθηκε επιτυχώς."

def task_delete(username, task_type, task_index):
    # Επιλογή της κατάλληλης λίστας tasks με βάση τον τύπο
    if task_type == "1":
        tasks = users[username]["obligations"]
    elif task_type == "2":
        tasks = users[username]["activities"]
    else:
        return False, "Άκυρος τύπος task."

    # Έλεγχος αν ο δείκτης είναι έγκυρος
    if task_index < 0 or task_index >= len(tasks):
        return False, "Άκυρος αριθμός task."

    # Διαγραφή του task
    del tasks[task_index]
    return True, "Το task διαγράφηκε επιτυχώς."
# Συνάρτηση για την ταξινόμηση tasks (υποχρεώσεις πρώτα, μετά δραστηριότητες)
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
                        "free_time": float(free_time),
                        "obligations": [],  # Προσθέστε αυτή τη γραμμή
                        "activities": []    # Προσθέστε αυτή τη γραμμή
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
            for task in data['obligations']:
                writer.writerow([username, task['name'], task['hours'], task['importance'], 'obligation'])
            for task in data['activities']:
                writer.writerow([username, task['name'], task['hours'], task['importance'], 'activity'])

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
                user['obligations'] = []  # Αρχικοποίηση υποχρεώσεων
                user['activities'] = []    # Αρχικοποίηση δραστηριοτήτων
            for row in reader:
                if len(row) == 5:
                    username, name, hours, importance, task_type = row
                    if username in users:
                        task = {
                            "name": name,
                            "hours": float(hours),
                            "importance": int(importance)
                        }
                        if task_type == 'obligation':
                            users[username]['obligations'].append(task)
                        elif task_type == 'activity':
                            users[username]['activities'].append(task)
    except FileNotFoundError:
        print("Το αρχείο στόχων δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def main():
    load_users_from_csv()
    load_tasks_from_csv()
    current_user = None
    
    while True:
        if current_user is None:
            print("\n1. Δημιουργία νέου χρήστη")
            print("2. Σύνδεση χρήστη")
            print("3. Έξοδος")
            choice = input("Επιλέξτε: ")
            if choice == '1':
                username = input("Όνομα χρήστη: ")
                password = input("Κωδικός: ")
                success, msg = create_user(username, password)
                print(msg)
            elif choice == '2':
                username = input("Όνομα χρήστη: ")
                password = input("Κωδικός: ")
                success, msg = login_user(username, password)
                if success:
                    current_user = username
                print(msg)
            elif choice == '3':
                save_users_to_csv()
                print("Αποθήκευση και έξοδος.")
                break
        else:
            print("\n1. Ορισμός ελεύθερου χρόνου")
            print("2. Προσθήκη task")
            print("3. Τροποποίηση task")
            print("4. Διαγραφή task")
            print("5. Αποσύνδεση")
            choice = input("Επιλέξτε: ")
            if choice == '1':
                free_time = input("Ελεύθερος χρόνος (ώρες): ")
                success, msg = set_free_time(current_user, free_time)
                print(msg)
            elif choice == '2':
                name = input("Όνομα task: ")
                hours = input("Ώρες: ")
                importance = input("Σημαντικότητα (1-10): ")
                task_type = input("Τύπος task (πατήστε '1' για υποχρέωση ή '2' για δραστηριότητα ελεύθερου χρόνου): ")
                success, msg = add_task(current_user, name, hours, importance, task_type)
                print(msg)
            elif choice == '3':
                # Επιλογή κατηγορίας task
                task_type = input("Επιλέξτε κατηγορία task ('1' για υποχρέωση, '2' για δραστηριότητα ελεύθερου χρόνου): ")
                if task_type == "1":
                    tasks = users[current_user]["obligations"]
                elif task_type == "2":
                    tasks = users[current_user]["activities"]
                else:
                    print("Άκυρος τύπος task.")
                    continue
                
                # Εμφάνιση tasks για επιλογή
                if not tasks:
                    print("Δεν υπάρχουν tasks σε αυτή την κατηγορία.")
                    continue
                for i, task in enumerate(tasks, start=1):  # Ξεκινάμε από το 1
                    print(f"{i}. {task['name']} ({task['hours']} ώρες, σημαντικότητα: {task['importance']})")
                
                # Επιλογή task και νέα δεδομένα
                task_index = int(input("Επιλέξτε τον αριθμό του task που θέλετε να τροποποιήσετε: "))
                if task_index < 1 or task_index > len(tasks):  # Ελέγχουμε αν είναι εντός ορίων
                    print("Άκυρος αριθμός task.")
                    continue
                
                # Μετατροπή του task_index σε 0-index
                task_index -= 1
                
                new_name = input("Νέο όνομα task (αφήστε κενό για να μην αλλάξει): ")
                new_hours = input("Νέες ώρες (αφήστε κενό για να μην αλλάξει): ")
                new_importance = input("Νέα σημαντικότητα (αφήστε κενό για να μην αλλάξει): ")
                
                # Κλήση της task_edit
                success, msg = task_edit(current_user, task_type, task_index,
                                         new_name if new_name else None,
                                         new_hours if new_hours else None,
                                         new_importance if new_importance else None)
                print(msg)
            elif choice == '4':
                # Επιλογή κατηγορίας task
                task_type = input("Επιλέξτε κατηγορία task ('1' για υποχρέωση, '2' για δραστηριότητα ελεύθερου χρόνου): ")
                if task_type == "1":
                    tasks = users[current_user]["obligations"]
                elif task_type == "2":
                    tasks = users[current_user]["activities"]
                else:
                    print("Άκυρος τύπος task.")
                    continue
                
                # Εμφάνιση tasks για επιλογή
                if not tasks:
                    print("Δεν υπάρχουν tasks σε αυτή την κατηγορία.")
                    continue
                for i, task in enumerate(tasks, start=1):  # Ξεκινάμε από το 1
                    print(f"{i}. {task['name']} ({task['hours']} ώρες, σημαντικότητα: {task['importance']})")
                
                # Επιλογή task για διαγραφή
                task_index = int(input("Επιλέξτε τον αριθμό του task που θέλετε να διαγράψετε: "))
                if task_index < 1 or task_index > len(tasks):  # Ελέγχουμε αν είναι εντός ορίων
                    print("Άκυρος αριθμός task.")
                    continue
                
                # Μετατροπή του task_index σε 0-index
                task_index -= 1
                
                # Κλήση της task_delete
                success, msg = task_delete(current_user, task_type, task_index)
                print(msg)
            elif choice == '5':
                current_user = None
                save_users_to_csv()
                save_tasks_to_csv()
                print("Αποσύνδεση επιτυχής.")

if __name__ == "__main__":
    main()