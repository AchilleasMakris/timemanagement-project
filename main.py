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
    return hashlib.sha256(password.encode()).hexdigest()

def input_free_time():
    while True:
        try:
            free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
            if not 1 <= free_time <= 168:  # Έλεγχος αν οι ώρες είναι μέσα στο όριο
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            return free_time
        except ValueError:
            print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")

def input_or_update_free_time(current_user):
    while True:
        try:
            free_time = float(input("Δώσε τον ελεύθερο χρόνο που έχεις συνολικά για την εβδομάδα: "))
            if not 1 <= free_time <= 168:  # Έλεγχος αν οι ώρες είναι μέσα στο όριο
                raise ValueError("Δεν μπορείς να ξεπεράσεις τις 168 ώρες της εβδομάδας!")
            users[current_user]['free_time'] = free_time
            print(f"Ο ελεύθερος χρόνος ενημερώθηκε σε {free_time} ώρες.")
            break
        except ValueError:
            print("Λάθος εισαγωγή για τον ελεύθερο χρόνο. Πρέπει να είναι αριθμός από 1 έως 168.")

def create_new_user():
    username = input("Δώσε το όνομα χρήστη: ").strip()
    if username in users:
        print("Ο χρήστης υπάρχει ήδη.")
    else:
        password = getpass.getpass("Δώσε τον κωδικό πρόσβασης: ").strip()
        password_hash = hash_password(password)
        users[username] = {"password": password_hash, "tasks": [], "free_time": 168.0}  # Προεπιλεγμένος ελεύθερος χρόνος
        print(f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς.")

def select_user():
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
    # Εμφανίζει το μενού επιλογών στον χρήστη
    print("\n--- Time Management ---")
    print("1. Εισαγωγή/Ενημέρωση Ελεύθερου Χρόνου")
    print("2. Προσθήκη νέου στόχου")
    print("3. Τροποίηση στόχου")
    print("4. Διαγραφή στόχου")
    print("5. Ταξινόμιση κατά σημαντικότητα")
    print("6. Εκτύπωση όλων των στόχων")
    print("7. Μέσος όρος χρόνου των Task")
    print("8. Γράφημα Πίτας")
    print("9. Γράφημα Στηλών")
    print("10. Έξοδος")

def task_add(tasks, total_hours, current_user):
    # Έλεγχος αν ο ελεύθερος χρόνος έχει οριστεί
    if users[current_user]['free_time'] == 168.0:  # Αν είναι η προεπιλεγμένη τιμή, σημαίνει ότι δεν έχει οριστεί
        print("Πρέπει πρώτα να ορίσεις τον ελεύθερο χρόνο σου για την εβδομάδα.")
        input_or_update_free_time(current_user)

    free_time = users[current_user]['free_time']  # Χρησιμοποιούμε τον ελεύθερο χρόνο του χρήστη

    while True:
        try:
            name = input("Δώσε το όνομα του στόχου: ").strip()

            # Έλεγχος αν το όνομα του στόχου υπάρχει ήδη
            if any(task['name'] == name for task in tasks):
                raise ValueError("Το όνομα του στόχου υπάρχει ήδη. Παρακαλώ επιλέξτε διαφορετικό όνομα.")

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
            
        except ValueError as e:
            print(e)  # Εκτύπωση του μηνύματος σφάλματος που προκλήθηκε
            continue

        # Προσθήκη του στόχου στη λίστα
        tasks.append({"name": name, "hours": hours, "importance": importance})
        total_hours += hours  # Ενημέρωση του συνολικού αριθμού ωρών
        print(f"Task added: {name}, Hours: {hours}, Importance: {importance}")
        remaining_free_time = free_time - total_hours  # Υπολογισμός του υπολειπόμενου ελεύθερου χρόνου
        print(f"Απομένουν {remaining_free_time} ώρες ελεύθερου χρόνου.")
        
        # Αποθήκευση των tasks στο αρχείο CSV
        save_tasks_to_csv(current_user)

        break

    return total_hours

def task_edit(current_user):
    global total_hours  # Για να αλλάξουμε τη συνολική διάρκεια των tasks
    tasks = users[current_user]['tasks']

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

    # Αφαιρούμε τις παλιές ώρες από το total_hours
    total_hours -= current_task['hours']

    # Ζητάμε από τον χρήστη να τροποποιήσει το όνομα, τις ώρες και τη σημαντικότητα
    new_name = input("Δώστε το νέο όνομα του Task: ")
    if(new_name.replace(" ", "").isalpha()):
        current_task['name'] = new_name
    else:
        print("Μη αποδεκτό όνομα.")

    try:
        new_hours = float(input("Παρακαλώ, δώστε τις εβδομαδιαίες ώρες: "))
        if 0 <= new_hours <= 168:
            current_task['hours'] = new_hours
        else:
            raise ValueError("Άκυρη εισαγωγή ώρας.")
    except ValueError:
        print("Άκυρη εισαγωγή ώρας, παρακαλώ προσπαθήστε ξανά.")
        return

    try:
        new_importance = int(input("Δώσε τον βαθμό σημαντικότητας του Task: "))
        if 1 <= new_importance <= 10:
            current_task['importance'] = new_importance
        else:
            raise ValueError("Άκυρη τιμή σημαντικότητας.")
    except ValueError:
        print("Άκυρη τιμή σημαντικότητας, παρακαλώ προσπαθήστε ξανά.")
        return

    # Προσθέτουμε τις νέες ώρες στο total_hours
    total_hours += current_task['hours']
    print("Η τροποποίηση ολοκληρώθηκε επιτυχώς.")

    # Αποθήκευση των tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)

def task_del(current_user):
    global total_hours
    tasks = users[current_user]['tasks']

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

    # Αφαιρούμε τις ώρες του task από το total_hours
    total_hours -= tasks[task_index]['hours']

    # Διαγραφή του task
    del tasks[task_index]

    print("Το Task διαγράφηκε επιτυχώς.")

    # Αποθήκευση των tasks στο αρχείο CSV
    save_tasks_to_csv(current_user)

def sort_by_importance(current_user):
    tasks = users[current_user]['tasks']
    print("\nΈγινε η ταξινόμιση με βάση του πόσο σημαντικό είναι το κάθε Task.\n")
    tasks.sort(key=lambda x: x['importance'], reverse=True)  # Ταξινόμηση των tasks κατά σημαντικότητα (φθίνουσα σειρά)
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task['name']} (Importance: {task['importance']}, Hours: {task['hours']})")

def show_all(current_user):
    tasks = users[current_user]['tasks']
    # Ελέγχουμε αν δεν υπάρχουν tasks στον κατάλογο
    if not tasks:
        print("Δεν υπάρχουν στόχοι.")  # Εκτυπώνουμε μήνυμα αν δεν υπάρχουν tasks
        return  # Επιστρέφουμε για να σταματήσει η συνάρτηση εδώ αν είναι κενό το tasks[]

    print("\n--- Όλοι οι στόχοι ---")  # Εμφανίζουμε τίτλο για να ξέρει ο χρήστης ότι ακολουθεί η λίστα των tasks
    # Διατρέχουμε όλα τα tasks με την μέθοδο enumerate για να έχουμε και τον αριθμό του task (i) και τα δεδομένα του task (task)
    for i, task in enumerate(tasks):
        # Εκτυπώνουμε τα δεδομένα του κάθε task με τις πληροφορίες του (όνομα, ώρες και σημαντικότητα)
        print(f"{i + 1}. Όνομα: {task['name']}, Διάρκεια: {task['hours']} ώρες, Σημαντικότητα: {task['importance']}")

        #TODO PRINT TOTAL FREE TIME

def average_time(current_user):
    tasks = users[current_user]['tasks']
    if not tasks:
        print("\nΔεν έχουν υποβληθεί Tasks.\n")
        return
    else:
        # Αρχικοποίηση του συνόλου των ωρών
        total_hours = 0  
        for task in tasks:
            # Πρόσθεση των ωρών κάθε task
            total_hours += task['hours']  
        
        # Υπολογισμός μέσου όρου
        average = total_hours / len(tasks)  
        print(f"Ο μέσος όρος των Tasks της εβδομάδας είναι: {average:.2f} ώρες")

def calculate_total_hours(tasks):
    return sum(task['hours'] for task in tasks)

def plot_pie_chart(tasks, free_time):
    total_hours = calculate_total_hours(tasks)
    if not tasks:
        print("Δεν υπάρχουν στόχοι για να δημιουργηθεί το γράφημα.")
        return
    
    # Δημιουργούμε λίστες με τα ονόματα των στόχων και τις ώρες που αφιερώνονται σε αυτούς
    labels = [task['name'] for task in tasks]
    sizes = [task['hours'] for task in tasks]

    plt.figure(figsize=(8, 8))
    
    # Τροποποίηση του autopct για να εμφανίζει το ποσοστό και τις ώρες
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return f'{pct:.1f}%\n({val} ώρες)'
        return my_autopct
    
    # Δημιουργία γραφήματος πίτας με τις ώρες και τα ονόματα των στόχων
    plt.pie(sizes, labels=labels, autopct=make_autopct(sizes), startangle=140)
    plt.axis('equal')  # Ισότητα αξόνων για να είναι κυκλικό το γράφημα
    plt.title('Κατανομή Χρόνου στους Στόχους')

    # Προσθήκη κειμένου για το συνολικό χρόνο και τον ελεύθερο χρόνο
    plt.text(-1.5, 1.0, f"Συνολικός Χρόνος: {total_hours} ώρες", fontsize=12, color='blue', ha='left')
    plt.text(-1.5, 0.8, f"Ελεύθερος Χρόνος: {free_time - total_hours} ώρες", fontsize=12, color='green', ha='left')

    plt.show()

def plot_bar_chart(tasks, free_time):
    total_hours = calculate_total_hours(tasks)
    if not tasks:
        print("Δεν υπάρχουν στόχοι για να δημιουργηθεί το γράφημα.")
        return

    # Δημιουργούμε λίστες για τα ονόματα των στόχων και τις ώρες που αφιερώνονται σε αυτούς
    x = [task['name'] for task in tasks]  # Ονόματα στόχων
    y = [task['hours'] for task in tasks]  # Ώρες για κάθε στόχο

    plt.figure(figsize=(10, 6))
    
    # Δημιουργία γραφήματος στήλης με τις ώρες και τα ονόματα των στόχων
    plt.bar(x, y, color='b')  
    plt.title('Κατανομή Χρόνου ανά Στόχο')
    plt.xlabel('Όνομα Στόχου')
    plt.ylabel('Ώρες')
    plt.xticks(rotation=45, ha='right')  # Ρύθμιση των τιμών του άξονα x με περιστροφή για καλύτερη ανάγνωση
    plt.grid(axis='y')  # Προσθήκη γραμμών πλέγματος στον άξονα y

    # Προσθήκη κειμένου για το συνολικό χρόνο και τον ελεύθερο χρόνο
    plt.text(-1.5, max(y) + 1.3, f"Συνολικός Χρόνος: {total_hours} ώρες", fontsize=12, color='blue')
    plt.text(-1.5, max(y) + 1.1, f"Ελεύθερος Χρόνος: {free_time - total_hours} ώρες", fontsize=12, color='green')

    plt.tight_layout()  # Αυτόματη προσαρμογή για να μην κόβονται οι ετικέτες
    plt.show()

def save_users_to_csv(filename='users.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, data in users.items():
            writer.writerow([username, data['password'], data['free_time']])

def load_users_from_csv(filename='users.csv'):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    username, password_hash, free_time = row
                    users[username] = {"password": password_hash, "tasks": [], "free_time": float(free_time)}
                elif len(row) == 2:
                    # Αν λείπει ο ελεύθερος χρόνος, θέσε μια προεπιλεγμένη τιμή
                    username, password_hash = row
                    users[username] = {"password": password_hash, "tasks": [], "free_time": 168.0}  # Προεπιλεγμένος ελεύθερος χρόνος
    except FileNotFoundError:
        print("Το αρχείο χρηστών δεν βρέθηκε. Δημιουργία νέου αρχείου.")

def save_tasks_to_csv(username, filename='tasks.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for task in users[username]['tasks']:
            writer.writerow([username, task['name'], task['hours'], task['importance']])

def load_tasks_from_csv(filename='tasks.csv'):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
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
    global total_hours  # Δηλώνουμε τη μεταβλητή ως global για να μπορούμε να την τροποποιήσουμε
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
                # Αν ο χρήστης συνδεθεί επιτυχώς, εμφανίζουμε το μενού
                while True:
                    display_menu()
                    user_input = int(input("Επέλεξε έναν αριθμό από το 1-10: "))
                    if user_input == 1:
                        input_or_update_free_time(current_user)
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
                    elif user_input == 10:
                        break
        elif choice == '3':
            break
        else:
            print("Παρακαλώ επέλεξε μια έγκυρη επιλογή.")

    # Στο τέλος του προγράμματος ή μετά από αλλαγές
    save_users_to_csv()
    save_tasks_to_csv(current_user)

if __name__ == "__main__":
    # Κάλεσε αυτές τις συναρτήσεις στην αρχή και στο τέλος του προγράμματος
    load_users_from_csv()
    load_tasks_from_csv()

    main()
