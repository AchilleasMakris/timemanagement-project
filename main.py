import matplotlib.pyplot as plt

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
    print("7. Γράφημα Πίτας")
    print("8. Γράφημα Στηλών")
    print("9. Έξοδος")

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
            
        # Χρήση του e για να μην μπερδευτεί με τα άλλα σφάλματα
        except ValueError as e:
            print(e)  # Εκτύπωση του μηνύματος σφάλματος που προκλήθηκε
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
    global total_hours  # Για να αλλάξουμε τη συνολική διάρκεια των tasks

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

def task_del():
    global total_hours  # Χρειάζεται για να ενημερώσουμε τις συνολικές ώρες

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

        #TODO PRINT TOTAL FREE TIME

def average_time():
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

def plot_pie_chart(tasks, free_time, total_hours):
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
    plt.text(-0.8, -1.2, f"Συνολικός Χρόνος: {total_hours} ώρες", fontsize=12, color='blue')
    plt.text(-0.8, -1.4, f"Ελεύθερος Χρόνος: {free_time - total_hours} ώρες", fontsize=12, color='green')

    plt.show()

def plot_bar_chart(tasks, free_time, total_hours):
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

# Κύριος βρόχος του προγράμματος που εκτελεί το μενού και τις επιλογές του χρήστη
while True:
    display_menu()  # Εμφανίζουμε το μενού επιλογών
    user_input = int(input("Επέλεξε έναν αριθμό απο το 1-9: "))  # Ζητάμε από τον χρήστη να κάνει μια επιλογή
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
        average_time()  # Καλούμε την συνάρτηση για τον υπολογισμό του μέσου όρου των ωρών των tasks
    elif user_input == 7:
        plot_pie_chart(tasks, free_time, total_hours)  # Καλούμε τη συνάρτηση για το γράφημα πίτας
    elif user_input == 8:
        plot_bar_chart(tasks, free_time, total_hours)  # Καλούμε τη συνάρτηση για το γράφημα στήλης
    elif user_input == 9:
        break  # Τερματίζουμε το πρόγραμμα όταν επιλεγεί η έξοδος
