import csv
import matplotlib.pyplot as plt
import hashlib

 #---------------------------------------------------------Αρχικοποίηση μεταβλητών----------------------------------------------------------------

users = []                      # Λίστα με όλους τους χρήστες - Κάθε χρήστης είναι ένα λεξικό με τα στοιχεία του
activities = []                 # Λίστα με όλες τις δραστηριότητες - Περιέχει όλες τις δραστηριότητες όλων των χρηστών

user = {}                       # Πρότυπο λεξικού για αποθήκευση στοιχείων χρήστη (username, password, user_total_free_hours)
activity = {}                   # Πρότυπο λεξικού για αποθήκευση στοιχείων δραστηριότητας (connected_user, onoma, diarkeia, grade, type)

user_ypoxrewseis = []           # Προσωρινή λίστα για αποθήκευση των Υποχρεώσεων του τρέχοντος χρήστη
user_hobbies = []               # Προσωρινή λίστα για αποθήκευση των Χόμπι του τρέχοντος χρήστη
user_activities = []            # Προσωρινή λίστα για αποθήκευση όλων των δραστηριοτήτων του τρέχοντος χρήστη

week_hours = 168                # Συνολικές ώρες της εβδομάδας (7 ημέρες x 24 ώρες)
total_ypoxrewseis_hours = 0     # Μετρητής για τις συνολικές ώρες υποχρεώσεων του χρήστη
total_hobby_hours = 0           # Μετρητής για τις συνολικές ώρες των Χόμπι του χρήστη
total_activity_hours = 0        # Μετρητής για τις συνολικές ώρες ΌΛΩΝ των δραστηριοτήτων του χρήστη
#terminate = False               # Σημαία για έλεγχο τερματισμού του προγράμματος

#--------------------------------------------------------- Αποθήκευση αρχείων --------------------------------------------------------------------


#--------------------------------------------------------- Διαχείριση χρηστών ------------------------------------------------------------------

# Αποθήκευση του χρήστη σε csv
def save_user_to_csv(filename="users.csv"):
    """
    Αποθηκεύει τη λίστα χρηστών στο αρχείο CSV.
    
    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: "users.csv"
    """
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "user_total_free_hours", "backup_user_free_hours"])
        writer.writeheader()
        writer.writerows(users)

# Φόρτωση χρηστών απο csv
def load_users_from_csv(filename="users.csv"):
    """
    Φορτώνει τους χρήστες από το αρχείο CSV.
    
    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: "users.csv"
    
    Note:
        Η εξαίρεση FileNotFoundError αγνοείται (pass) διότι το αρχείο θα δημιουργηθεί 
        κατά την πρώτη αποθήκευση αν δεν υπάρχει ήδη.
    """
    users.clear()  # Καθαρισμός της λίστας πριν τη φόρτωση νέων δεδομένων
    try:
        with open(filename, mode="r", newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    "username": row['username'],
                    "password": row['password'],
                    "user_total_free_hours": float(row.get('user_total_free_hours', 0)),  # Μετατροπή σε float
                    "backup_user_free_hours": float(row.get('backup_user_free_hours', 0))  # Προεπιλογή 0 αν είναι None
                })
    except FileNotFoundError:
        pass  # Το αρχείο θα δημιουργηθεί την πρώτη φορά που θα αποθηκευτεί χρήστης
#---------------------------------------------------------- Διαχεριση δραστρηριοτήτων -----------------------------------------------------------

# Αποθήκευση δραστηριοτήτων σε csv
def save_activities_to_csv(filename="activities.csv"):
    """
    Αποθηκεύει τη λίστα δραστηριοτήτων στο αρχείο CSV.
    
    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: "activities.csv"
    """
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "Δραστηριότητα", "Διάρκεια", "Σημαντικότητα", "Τύπος"])
        writer.writeheader()
        writer.writerows(activities)


# Φόρτωση δραστηριοτήτων απο csv
def load_activities_from_csv(filename="activities.csv"):
    """
    Φορτώνει τις δραστηριότητες από το αρχείο CSV.
    
    Args:
        filename (str): Το όνομα του αρχείου CSV. Προεπιλογή: "activities.csv"
    
    Raises:
        Exception: Σε περίπτωση σφάλματος κωδικοποίησης του αρχείου.
    
    Note:
        - Μετατρέπει τη "Διάρκεια" σε float και τη "Σημαντικότητα" σε int
        - Αγνοείται η εξαίρεση FileNotFoundError, το αρχείο θα δημιουργηθεί αργότερα
    """
    activities.clear()  # Καθαρισμός της λίστας πριν τη φόρτωση νέων δεδομένων
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                activities.append({
                    "username": row["username"],
                    "Δραστηριότητα": row["Δραστηριότητα"],
                    "Διάρκεια": float(row["Διάρκεια"]),  # Μετατροπή σε float
                    "Σημαντικότητα": int(row["Σημαντικότητα"]),  # Μετατροπή σε int
                    "Τύπος": row["Τύπος"]
                })
    except FileNotFoundError:
        pass  # Το αρχείο θα δημιουργηθεί την πρώτη φορά που θα αποθηκευτεί δραστηριότητα
    except UnicodeDecodeError:
        raise Exception("Σφάλμα αποκωδικοποίησης. Βεβαιωθείτε ότι το αρχείο είναι σε UTF-8 κωδικοποίηση.")
#-------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------ Συναρτήσεις Χρηστών ----------------------------------------------------------------------

def hash_password(password):
    """
    Κρυπτογραφεί έναν κωδικό πρόσβασης χρησιμοποιώντας τον αλγόριθμο SHA-256.
    
    Args:
        password (str): Ο κωδικός πρόσβασης που εισάγει ο χρήστης.

    Returns:
        str: Η κρυπτογραφημένη τιμή (hash) του κωδικού πρόσβασης.
    """
    return hashlib.sha256(password.encode()).hexdigest()
    
# Προσθήκη νέου χρήστη
def register_user(username, password, password_confirm):
    """
    Καταχωρεί έναν νέο χρήστη στο σύστημα.
    
    Args:
        username (str): Το όνομα χρήστη.
        password (str): Ο κωδικός πρόσβασης.
        password_confirm (str): Επιβεβαίωση του κωδικού πρόσβασης.
    
    Returns:
        tuple: (επιτυχία (bool), μήνυμα (str))
    
    Note:
        - Ελέγχει αν το όνομα χρήστη ή κωδικός είναι κενοί
        - Ελέγχει αν το όνομα χρήστη είναι ήδη σε χρήση
        - Ελέγχει αν οι κωδικοί ταιριάζουν
        - Κρυπτογραφεί τον κωδικό πριν την αποθήκευση
    """
     # Check για κενό όνομα/κωδικό
    if not username.strip():
        return False, "Το όνομα χρήστη δεν μπορεί να είναι κενό."
    if not password.strip():
        return False, "Ο κωδικός δεν μπορεί να είναι κενός."
    if any(u["username"] == username for u in users):
        return False, "Το όνομα χρήστη χρησιμοποιείται ήδη."
    if password != password_confirm:
        return False, "Οι κωδικοί δεν είναι ίδιοι."
    password_hash = hash_password(password)  # Κρυπτογράφηση του κωδικού για ασφάλεια
    user = {
        "username": username,
        "password": password_hash,
        "user_total_free_hours": 0.0,  # Αρχικοποίηση με μηδενικό ελεύθερο χρόνο
        "backup_user_free_hours": 0.0   # Αντίγραφο ασφαλείας του αρχικού ελεύθερου χρόνου
    }
    users.append(user)
    save_user_to_csv()  # Αποθήκευση της ενημερωμένης λίστας χρηστών στο CSV
    return True, f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς."

# Σύνδεση χρήστη
def connect_user(username, password):
    """
    Ελέγχει τα διαπιστευτήρια του χρήστη και τον συνδέει στο σύστημα.
    
    Args:
        username (str): Το όνομα χρήστη.
        password (str): Ο κωδικός πρόσβασης.
    
    Returns:
        tuple: (επιτυχία (bool), αποτέλεσμα (dict ή str))
        Αν επιτυχία=True, επιστρέφει το λεξικό του χρήστη
        Αν επιτυχία=False, επιστρέφει μήνυμα λάθους
    
    Note:
        - Ελέγχει για κενά πεδία
        - Συγκρίνει τον κρυπτογραφημένο κωδικό με αυτόν στη βάση
    """
    # Check για κενό όνομα/κωδικό
    if not username.strip() or not password.strip():
        return False, "Το όνομα χρήστη και ο κωδικός δεν μπορούν να είναι κενά."
    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            return True, user
    return False, "Λανθασμένα στοιχεία εισόδου."

#------------------------------------------------- Συναρτήσεις Προγράμματος ----------------------------------------------------------------------
# Clear User List
def clear_data(user_activities, user_ypoxrewseis, user_hobbies):
    """
    Καθαρίζει τις προσωρινές λίστες δραστηριοτήτων.
    
    Args:
        user_activities (list): Λίστα με όλες τις δραστηριότητες του χρήστη.
        user_ypoxrewseis (list): Λίστα με τις υποχρεώσεις του χρήστη.
        user_hobbies (list): Λίστα με τα χόμπι του χρήστη.
    
    Returns:
        tuple: Τις άδειες λίστες (user_activities, user_ypoxrewseis, user_hobbies)
    """
    user_activities = []  # Δημιουργούμε νέες κενές λίστες
    user_ypoxrewseis = []
    user_hobbies = []
    return user_activities, user_ypoxrewseis, user_hobbies

# Επιλογή των δραστηριοτήτων που ανήκουν στον συνδεδεμένο χρήστη
def get_user_activities(connected_user, activities, total_activity_hours, total_hobby_hours, total_ypoxrewseis_hours):
    """
    Φιλτράρει τις δραστηριότητες του συνδεδεμένου χρήστη και υπολογίζει τις συνολικές ώρες.
    
    Args:
        connected_user (str): Το όνομα χρήστη του συνδεδεμένου χρήστη.
        activities (list): Η λίστα με όλες τις δραστηριότητες όλων των χρηστών.
        total_activity_hours (float): Μετρητής για τις συνολικές ώρες όλων των δραστηριοτήτων.
        total_hobby_hours (float): Μετρητής για τις συνολικές ώρες των χόμπι.
        total_ypoxrewseis_hours (float): Μετρητής για τις συνολικές ώρες των υποχρεώσεων.
    
    Returns:
        tuple: (user_activities, total_activity_hours, user_ypoxrewseis, 
                total_ypoxrewseis_hours, user_hobbies, total_hobby_hours)
    
    Note:
        - Πρώτα καθαρίζει τις λίστες με την clear_data
        - Φιλτράρει τις δραστηριότητες βάσει του συνδεδεμένου χρήστη
        - Διαχωρίζει τις δραστηριότητες σε υποχρεώσεις και χόμπι
        - Ενημερώνει τους μετρητές ωρών για κάθε κατηγορία
    """
    clear_data(user_activities, user_ypoxrewseis, user_hobbies) # Καθαρισμός των λιστών
    for activity in activities:
        if activity["username"] == connected_user:
            user_activities.append(activity)  # Προσθήκη στη λίστα δραστηριοτήτων χρήστη
            total_activity_hours += float(activity["Διάρκεια"])  # Αύξηση των συνολικών ωρών
            if activity["Τύπος"] == "Υποχρέωση":
                user_ypoxrewseis.append(activity)  # Προσθήκη στις υποχρεώσεις
                total_ypoxrewseis_hours += float(activity["Διάρκεια"])  # Αύξηση ωρών υποχρεώσεων
            else:
                user_hobbies.append(activity)  # Προσθήκη στα χόμπι
                total_hobby_hours += float(activity["Διάρκεια"])  # Αύξηση ωρών χόμπι

    return user_activities,total_activity_hours,user_ypoxrewseis, total_ypoxrewseis_hours,user_hobbies, total_hobby_hours

# Επιλογή του διαθέσιμου χόνου που ανήκει στον συνδεδεμένο χρήστη
def get_user_total_free_hours(connected_user, users):
    """
    Ανακτά τον διαθέσιμο ελεύθερο χρόνο του συνδεδεμένου χρήστη.
    
    Args:
        connected_user (str): Το όνομα χρήστη του συνδεδεμένου χρήστη.
        users (list): Η λίστα με όλους τους χρήστες.
    
    Returns:
        float: Ο διαθέσιμος ελεύθερος χρόνος του χρήστη.
    
    Note:
        - Ελέγχει αν οι ώρες είναι εντός του έγκυρου εύρους (0-168 ώρες)
    """
    while True:    
        for user in users:
            if user["username"] == connected_user:
                user_total_free_hours = float(user["user_total_free_hours"])
                if user_total_free_hours < 0 or user_total_free_hours > 168:
                    continue  # Αν ο χρόνος είναι εκτός ορίων, συνεχίζουμε το loop
            else:
                return user_total_free_hours  # Επιστροφή του έγκυρου ελεύθερου χρόνου

# Συνάρτηση εισαγωγής ονόματος δραστηριότητας ή υποχρέωσης
# def name():
#     """
#     Εισάγει και επικυρώνει το όνομα μιας δραστηριότητας.
    
#     Returns:
#         str: Το έγκυρο όνομα της δραστηριότητας.
    
#     Note:
#         - Ελέγχει αν το όνομα είναι κενό ή αν δεν περιέχει κανέναν αλφαβητικό χαρακτήρα
#         - Αφαιρεί τα περιττά κενά με την strip() πριν τον έλεγχο
#     """
#     # Εισαγωγή ονόματος, αφαιρώ τα κενά space πρίν και μετά το όνομα. 
#     onoma = input("Δώστε το όνομα της δραστηριότητας: ").strip()
            
#     """"
#         Έλεγχος ονόματος, αν δωθεί το κενό τότε το διαγράφω με την strip επομένως onoma = False και μπαίνω στην επανάληψη
#         ή αν κανένα απο τα στοιχεία του ονόματος δεν είναι χαρακτήρας.
#     """
#     while not onoma or not any(char.isalpha() for char in onoma):
#         onoma = input("Το όνομα της δραστηριότητας δεν μπορεί να είναι κενό ή αριθμός, παρακαλώ επανεισάγετε το όνομα: ").strip()
#     return onoma

# Συνάρτηση εισαγωγής διάρκειας δραστηριότητας ή υποχρέωσης
# def duration(user_total_free_hours):
#     """
#     Εισάγει και επικυρώνει τη διάρκεια μιας δραστηριότητας.
    
#     Args:
#         user_total_free_hours (float): Ο διαθέσιμος ελεύθερος χρόνος του χρήστη.
    
#     Returns:
#         tuple: (diarkeia, new_user_total_free_hours) - Η διάρκεια της δραστηριότητας και
#                ο ενημερωμένος ελεύθερος χρόνος.
    
#     Note:
#         - Ελέγχει αν η διάρκεια είναι θετική και μικρότερη από τον διαθέσιμο χρόνο
#         - Χειρίζεται σφάλματα μετατροπής τιμών (ValueError)
#         - Επιτρέπει στον χρήστη να επαναπροσδιορίσει τον συνολικό ελεύθερο χρόνο του
#     """
    
#     # Εισαγωγή διάρκειας με έλεγχο ορθότητας (Δεν μπορεί να υπερβαίνει τον συνολικό ελεύθερο χρόνο, τις 168 ώρες της εβδομάδας και να είναι αρνητική ή χαρακτήρας).
#     while True:
#         try:
#             diarkeia = input("\nΔώστε την διάρκεια της δραστηριότητας σε ώρες: ").strip()
#             diarkeia = float(diarkeia)  # Μετατροπή σε αριθμό
#             if diarkeia and 0 < diarkeia <= user_total_free_hours:
#                 user_total_free_hours -= diarkeia  # Αφαίρεση της διάρκειας από τον ελεύθερο χρόνο
#                 # Επιστρέφει την διάρκεια και τον ενημερωμένο ελεύθερο χρόνο
#                 return diarkeia, user_total_free_hours
#             else:
#                 if diarkeia + user_total_free_hours > week_hours:
#                     print(f"\nΗ διάρκεια πρέπει να είναι θετικός αριθμός και δεν μπορεί να ξεπερνάει τις {user_total_free_hours} διαθέσιμες ώρες ή τις 168 ώρες της εβδομάδας.")
#         except ValueError:
#             print("\nΜή έγκυρη είσοδος, παρακαλώ εισάγετε έναν αριθμό ωρών.")
        
#         # Σε περίπτωση σφάλματος, επιτρέπουμε στον χρήστη να επαναπροσδιορίσει τον συνολικό ελεύθερο χρόνο
#         try:
#             user_total_free_hours = input("Παρακαλώ εισάγετε τις συνολικές ώρες που έχετε διαθέσιμες για αυτήν την εβδομάδα: ").strip()
#             user_total_free_hours = float(user_total_free_hours)
            
#             if 0 <= user_total_free_hours <= 168 and user_total_free_hours > total_activity_hours:
#                 user_total_free_hours -= total_activity_hours  # Αφαίρεση του χρόνου που ήδη χρησιμοποιείται
#                 if activities:
#                     print(f"\nΑφαιρέθηκαν {total_activity_hours} ώρες από τον νέο συνολικό σας χρόνο για τις ήδη υπάρχουσες δραστηριότητές σας.")
#                     print(f"\nΟ νέος συνολικός ελεύθερος χρόνος σας είναι: {user_total_free_hours}.")

#                 return user_total_free_hours
#             else:
#                 if total_activity_hours > user_total_free_hours:
#                     print(f"\nΕισάγετε παραπάνω ώρες! Απαιτούνται {total_activity_hours} ώρες για τις ήδη υπάρχουσες δραστηριότητές σας.")
#                 elif total_activity_hours == user_total_free_hours:
#                     print(f"Εισάγετε παραπάνω ώρες. Απαιτούνται ήδη {user_total_free_hours} για τις υπάρχουσες δραστηριότητες.")
#                 else:
#                     print("Οι συνολικές διαθέσιμές ώρες δεν μπορούν να είναι αρνητικός αριθμός ή περισσότερες από τις 168 ώρες της εβδομάδας.")
                
#         except ValueError:
#             print ("Μή έγκυρη είσοδος. Παρακαλώ εισάγετε τον αριθμό των διαθέσιμων ωρών.")
# Συνάρτηση εισαγωγής βαθμού σημαντικότητας
# def importance():
#     """
#     Εισάγει και επικυρώνει τον βαθμό σημαντικότητας μιας δραστηριότητας.
    
#     Returns:
#         int: Ο έγκυρος βαθμός σημαντικότητας (1-10).
    
#     Note:
#         - Ελέγχει αν η τιμή είναι ακέραιος μεταξύ 1 και 10
#         - Χειρίζεται σφάλματα μετατροπής τιμών (ValueError)
#     """
#     while True:
#         try:    
#             grade = input("Δώστε τον βαθμό σημαντικότητας (1-10): ").strip()
#             grade = int(grade)  # Μετατροπή σε ακέραιο
#             if grade and 1 <= grade <= 10:  # Έλεγχος αν είναι μεταξύ 1 και 10
#                 return grade
#             else:
#                 print("Παρακαλώ δώστε έναν βαθμό απο το 1 εώς το 10.")
#         except ValueError:
#             print("Μή έγκυρη τιμή.")


# Ταξινόμηση 
def taksinomisi(current_user):
    """
    Ταξινομεί τις δραστηριότητες του χρήστη με προτεραιότητα στις υποχρεώσεις.
    
    Args:
        current_user (str): Το όνομα χρήστη του συνδεδεμένου χρήστη.
    
    Returns:
        list: Η ταξινομημένη λίστα δραστηριοτήτων του χρήστη.
    
    Note:
        - Πρώτα φιλτράρει τις δραστηριότητες του τρέχοντος χρήστη
        - Ταξινομεί πρώτα με βάση τον τύπο (Υποχρεώσεις πρώτα) και μετά κατά σημαντικότητα (φθίνουσα)
    """
    # Clear and rebuild user_activities list for the connected user
    user_activities = []

    for activity in activities:
        if activity["username"] == current_user:
            user_activities.append(activity)
    
    # Sort by type first (Υποχρέωση first), then by importance
    # Η lambda δημιουργεί ένα tuple κριτηρίων ταξινόμησης (τύπος, αρνητική σημαντικότητα)
    # Χρησιμοποιώντας 0 για Υποχρέωση και 1 για Χόμπι, οι υποχρεώσεις τοποθετούνται πρώτα
    # Η αρνητική σημαντικότητα (-x["Σημαντικότητα"]) εξασφαλίζει φθίνουσα ταξινόμηση
    user_activities.sort(key=lambda x: (0 if x["Τύπος"] == "Υποχρέωση" else 1, -x["Σημαντικότητα"]))
    
    return user_activities

def add_activity(connected_user, onoma, diarkeia, grade, activity_type, activities, users):
    """
    Add a new activity for the connected user.
    
    Args:
        connected_user (str): Username of the current user.
        onoma (str): Name of the activity.
        diarkeia (float): Duration in hours.
        grade (int): Importance (1-5).
        activity_type (str): "Υποχρέωση" or "Χόμπι".
        activities (list): Global activities list.
        users (list): Global users list.
    
    Returns:
        tuple: (success (bool), message (str), new_free_time (float or None))
    
    Note:
        - Ελέγχει αν υπάρχει ήδη δραστηριότητα με το ίδιο όνομα
        - Δημιουργεί και προσθέτει τη νέα δραστηριότητα στη λίστα
        - Ενημερώνει τον διαθέσιμο ελεύθερο χρόνο του χρήστη
        - Αποθηκεύει τις αλλαγές στα CSV αρχεία
    """
    # Check if activity name already exists for this user
    if any(a["username"] == connected_user and a["Δραστηριότητα"] == onoma for a in activities):
        return False, "Η δραστηριότητα υπάρχει ήδη.", None
    # Get user's current free time
    for user in users:
        if user["username"] == connected_user:
            user_total_free_hours = user["user_total_free_hours"]
            break
    else:
        return False, "Ο χρήστης δεν βρέθηκε.", None
    
    # Σχόλια: Το τμήμα ελέγχου επάρκειας ελεύθερου χρόνου είναι σχολιασμένο
    # Αυτό επιτρέπει την προσθήκη δραστηριοτήτων ακόμη και αν ξεπερνάνε τον διαθέσιμο χρόνο
    #if diarkeia > user_total_free_hours:
        return False, f"Δεν υπάρχει αρκετός ελεύθερος χρόνος. Διαθέσιμος: {user_total_free_hours} ώρες.", None
    
    # Create new activity
    activity = {
        "username": connected_user,
        "Δραστηριότητα": onoma,
        "Διάρκεια": diarkeia,
        "Σημαντικότητα": grade,
        "Τύπος": activity_type
    }
    activities.append(activity)  # Προσθήκη στη λίστα δραστηριοτήτων
    
    # Update user's free time
    user_total_free_hours -= diarkeia  # Μείωση του ελεύθερου χρόνου
    for user in users:
        if user["username"] == connected_user:
            user["user_total_free_hours"] = user_total_free_hours
            break
    
    save_activities_to_csv()  # Αποθήκευση αλλαγών
    save_user_to_csv()
    return True, "Η δαστηριότητα προστέθηκε επιτυχώς.", user_total_free_hours

# Προσθήκη δραστηριότητας
def modify_activity(connected_user, onoma, activities, users, new_onoma=None, new_diarkeia=None, new_grade=None, new_type=None):
    """
    Modify an existing activity.
    
    Args:
        connected_user (str): Username of the current user.
        onoma (str): Current name of the activity to modify.
        activities (list): Global activities list.
        users (list): Global users list.
        new_onoma (str, optional): New name.
        new_diarkeia (float, optional): New duration.
        new_grade (int, optional): New importance.
        new_type (str, optional): New type.
    
    Returns:
        tuple: (success (bool), message (str))
    
    Note:
        - Ελέγχει αν το νέο όνομα υπάρχει ήδη
        - Ενημερώνει τον διαθέσιμο ελεύθερο χρόνο με βάση τη διαφορά παλιάς και νέας διάρκειας
        - Ο έλεγχος του διαθέσιμου χρόνου είναι σχολιασμένος, επιτρέποντας την αλλαγή ακόμη και αν ο χρήστης δεν έχει επαρκή ελεύθερο χρόνο
    """
    for activity in activities:
        if activity["username"] == connected_user and activity["Δραστηριότητα"] == onoma:
            if new_onoma and new_onoma != onoma:
                if any(a["Δραστηριότητα"] == new_onoma and a["username"] == connected_user for a in activities):
                    return False, "Το νέο όνομα υπάρχει ήδη."
                activity["Δραστηριότητα"] = new_onoma  # Ενημέρωση ονόματος
            
            if new_diarkeia is not None:
                old_diarkeia = activity["Διάρκεια"]
                for user in users:
                    if user["username"] == connected_user:
                        # Υπολογισμός νέου ελεύθερου χρόνου (προσθέτουμε την παλιά διάρκεια και αφαιρούμε τη νέα)
                        user_total_free_hours = user["user_total_free_hours"] + old_diarkeia - new_diarkeia
                        
                        # Σχόλιο: Το τμήμα ελέγχου του ελεύθερου χρόνου είναι σχολιασμένο
                        # if user_total_free_hours < 0:
                        #     return False, "Δεν υπάρχει αρκετός ελεύθερος χρόνος για αυτή την αλλαγή."
                        
                        user["user_total_free_hours"] = user_total_free_hours
                        break
                activity["Διάρκεια"] = new_diarkeia  # Ενημέρωση διάρκειας
            
            if new_grade is not None:
                activity["Σημαντικότητα"] = new_grade  # Ενημέρωση σημαντικότητας
            
            if new_type:
                activity["Τύπος"] = new_type  # Ενημέρωση τύπου
            
            save_activities_to_csv()  # Αποθήκευση αλλαγών
            save_user_to_csv()
            return True, "Δραστηριότητα τροποποιήθηκε επιτυχώς."
    return False, "Η δραστηριότητα δεν βρέθηκε."

def delete_activity(connected_user, onoma, activities, users):
    """
    Delete an activity for the connected user.
    
    Args:
        connected_user (str): Username of the current user.
        onoma (str): Name of the activity to delete.
        activities (list): Global activities list.
        users (list): Global users list.
    
    Returns:
        tuple: (success (bool), message (str))
    
    Note:
        - Αφαιρεί τη δραστηριότητα από τη λίστα activities
        - Προσθέτει τη διάρκειά της πίσω στον διαθέσιμο ελεύθερο χρόνο του χρήστη
        - Αποθηκεύει τις αλλαγές στα CSV αρχεία
    """
    for activity in activities:
        if activity["username"] == connected_user and activity["Δραστηριότητα"] == onoma:
            diarkeia = activity["Διάρκεια"]  # Αποθήκευση διάρκειας πριν τη διαγραφή
            activities.remove(activity)  # Αφαίρεση από τη λίστα
            for user in users:
                if user["username"] == connected_user:
                    user["user_total_free_hours"] += diarkeia  # Επιστροφή ωρών στον ελεύθερο χρόνο
                    break
            save_activities_to_csv()  # Αποθήκευση αλλαγών
            save_user_to_csv()
            return True, "Η δραστηριότητα διαγράφηκε επιτυχώς."
    return False, "Η δραστηριότητα δεν βρέθηκε."

def set_free_time(connected_user, user_total_free_hours, activities, users):
    """
    Set the total available time for the week, adjusting remaining free time.
    
    Args:
        connected_user (str): Username of the current user.
        user_total_free_hours (float): Total available time for the week.
        activities (list): Global activities list.
        users (list): Global users list.
    
    Returns:
        tuple: (success (bool), message (str))
    
    Note:
        - Ελέγχει αν ο χρόνος είναι εντός των επιτρεπτών ορίων (0-168 ώρες)
        - Υπολογίζει τις συνολικές ώρες των δραστηριοτήτων του χρήστη
        - Αποθηκεύει τον νέο διαθέσιμο ελεύθερο χρόνο (συνολικός χρόνος - ώρες δραστηριοτήτων)
        - Ο έλεγχος επάρκειας χρόνου για τις υπάρχουσες δραστηριότητες είναι σχολιασμένος
    """
    # Input validation: free time must be >0 and <=168
    if user_total_free_hours <= 0 or user_total_free_hours > 168:
        return False, "Ο συνολικός ελεύθερος χρόνος πρέπει να είναι μεγαλύτερος του 0 και μικρότερος ή ίσος με 168."
    
    # total_activity_hours = sum(task["Διάρκεια"] for task in activities if task["username"] == connected_user)
    # Σχόλιο: Ο έλεγχος επαρκούς χρόνου είναι σχολιασμένος, επιτρέποντας στον χρήστη να ορίσει λιγότερες ώρες από αυτές που απαιτούνται
    # if user_total_free_hours < total_activity_hours:
    #     return False, f"Ο νέος χρόνος πρέπει να είναι τουλάχιστον {total_activity_hours} ώρες για τις υπάρχουσες δραστηριότητες."
    
    for user in users:
        if user["username"] == connected_user:
            user["user_total_free_hours"] = user_total_free_hours - total_activity_hours  # Ενημέρωση διαθέσιμου χρόνου
            save_user_to_csv()  # Αποθήκευση αλλαγών
            return True, f"Ελεύθερος χρόνος ενημερώθηκε επιτυχώς σε: {user_total_free_hours}."


# Εμφάνιση όλων των αποθηκευμένων δραστηριοτήτων
# def display_activities(user_activities):
#     """
#     Προβάλει τις αποθηκευμένες δραστηριότητες ή αν δεν υπάρχουν, ενημερώνει με κατάλληλο μήνυμα.
    
#     Args:
#         user_activities (list): Η λίστα με τις δραστηριότητες του χρήστη.
#     """
#     if not user_activities:
#         print("\nΔεν βρέθηκαν δραστηριότητες.\n")
#     else:
#         print("\nΟι δραστηριότητες που έχετε να κάνετε αυτή την εβδομάδα είναι: \n")
#         for drastiriotita in user_activities:
#             print (f"{drastiriotita['Δραστηριότητα']} : Διάρκεια: {drastiriotita['Διάρκεια']} ώρες | Βαθμός σημαντικότητας: {drastiriotita['Σημαντικότητα']} | Τύπος: {drastiriotita['Τύπος']}")

# Εμφάνιση του συνολικού ελεύθερου χρόνου
# def display_FreeTime(user_total_free_hours,user_activities):
#     """
#     Προβάλει τον διαθέσιμο ελεύθερο χρόνο
    
#     Args:
#         user_total_free_hours (float): Ο διαθέσιμος ελεύθερος χρόνος του χρήστη.
#         user_activities (list): Η λίστα με τις δραστηριότητες του χρήστη.
    
#     Note:
#         - Εμφανίζει διαφορετικά μηνύματα ανάλογα με την κατάσταση του ελεύθερου χρόνου
#           και την ύπαρξη δραστηριοτήτων
#     """
    
#     if user_total_free_hours > 0:
#         print("\nΟ συνολικός ελεύθερος χρόνος σας για αυτή την εβδομάδα είναι: ", user_total_free_hours, "ώρες.")
#     else:
#         if not user_activities:
#             print("\nΔεν έχετε εισάγει τον διαθέσιμο ελεύθερο χρόνο σας. Παρακαλώ πατήστε το 6 για προσθήκη ελεύθερου χρόνου.")
#         else:
#             print("\nΔεν έχετε διαθέσιμό ελεύθερο χρόνο, παρακαλώ τροποποιήστε ή διαγράψτε κάποια δραστηριότητα για να ελευθερώσετε χρόνο ή πατήστε 6 για να προσθέσετε ελεύθερο χρόνο")

# Ενημέρωση της λίστας users
# def update_users_list(connected_user, user_total_free_hours):
#     """
#     Ενημερώνει τον ελεύθερο χρόνο του συγκεκριμένου χρήστη στη λίστα users.
    
#     Args:
#         connected_user (str): Το όνομα χρήστη του συνδεδεμένου χρήστη.
#         user_total_free_hours (float): Ο νέος διαθέσιμος ελεύθερος χρόνος.
#     """
#     for user in users:
#         if connected_user == user["username"]:
#             user["user_total_free_hours"] = user_total_free_hours

# def plot_pie_chart(user_activities, user_total_free_hours):
#     """
#     Δημιουργεί ένα γράφημα πίτας που δείχνει την κατανομή του χρόνου.

#     Args:
#         user_activities (list): Λίστα με τις δραστηριότητες του χρήστη.
#         user_total_free_hours (float): Ο εναπομείνων ελεύθερος χρόνος του χρήστη.

#     Returns:
#         None
    
#     Note:
#         - Χρησιμοποιεί προσαρμοσμένη συνάρτηση autopct_format για την εμφάνιση ωρών αντί ποσοστών
#         - Προσθέτει τον ελεύθερο χρόνο στο γράφημα αν είναι μεγαλύτερος του 0
#     """
#     # Έλεγχος αν υπάρχουν δεδομένα για απεικόνιση
#     if not user_activities and user_total_free_hours <= 0:
#         print("Δεν υπάρχουν δραστηριότητες ή ελεύθερος χρόνος για απεικόνιση.")
#         return
    
#     # Δημιουργία λιστών για ετικέτες και μεγέθη
#     labels = [activity['Δραστηριότητα'] for activity in user_activities]
#     sizes = [float(activity['Διάρκεια']) for activity in user_activities]
    
#     # Προσθήκη ελεύθερου χρόνου αν είναι μεγαλύτερος από 0
#     if user_total_free_hours > 0:
#         labels.append("Ελεύθερος χρόνος")
#         sizes.append(user_total_free_hours)
    
# #     Υπολογίζει το άθροισμα όλων των ωρών: sum(allvals)
# #     Μετατρέπει το ποσοστό σε δεκαδικό αριθμό: pct / 100.
# #     Πολλαπλασιάζει για να βρει τις πραγματικές ώρες: pct / 100. * sum(allvals)
# #     Μετατρέπει το αποτέλεσμα σε ακέραιο: int(pct / 100. * sum(allvals))
# #     Τέλος, επιστρέφει μια συμβολοσειρά με το αποτέλεσμα: f"{absolute} ώρες"
# #     Για παράδειγμα, αν το γράφημα πίτας δείχνει μια δραστηριότητα που καταλαμβάνει το 30% του συνολικού χρόνου και το συνολικό άθροισμα των ωρών είναι 100, η συνάρτηση θα υπολογίσει: 30 / 100 * 100 = 30 και θα εμφανίσει "30 ώρες" σε αυτό το κομμάτι της πίτας.

#     # Προσαρμοσμένη συνάρτηση για εμφάνιση ωρών αντί ποσοστού.
#     def autopct_format(pct, allvals):
#         absolute = int(pct / 100. * sum(allvals))  # Μετατροπή ποσοστού σε ώρες
#         return f"{absolute} ώρες"
    
#     # Δημιουργία γράφηματος πίτας
#     plt.pie(sizes, labels=labels, autopct=lambda pct: autopct_format(pct, sizes))
#     plt.title("Κατανομή Χρόνου")
#     plt.show()

# def plot_bar_chart(user_activities, user_total_free_hours):
#     """
#     Δημιουργεί ένα γράφημα στηλών που δείχνει τις ώρες ανά δραστηριότητα.

#     Args:
#         user_activities (list): Λίστα με τις δραστηριότητες του χρήστη.
#         user_total_free_hours (float): Ο συνολικός ελεύθερος χρόνος του χρήστη.

#     Returns:
#         None
    
#     Note:
#         - Δημιουργεί ραβδόγραμμα με τις ώρες κάθε δραστηριότητας
#         - Προσθέτει τιμές πάνω από τις μπαρες
#         - Προσθέτει οριζόντια γραμμή που δείχνει τον διαθέσιμο ελεύθερο χρόνο
#     """
#     if not user_activities:
#         print("Δεν υπάρχουν δραστηριότητες για απεικόνιση.")
#         return
    
#     # Εξαγωγή ονομάτων και ωρών
#     names = [activity['Δραστηριότητα'] for activity in user_activities]
#     hours = [float(activity['Διάρκεια']) for activity in user_activities]
    
#     # Ορισμός παλέτας χρωμάτων
#     colors = plt.get_cmap('tab10').colors  # Χρήση της προκαθορισμένης παλέτας tab10
    
#     # Δημιουργία μπαρών
#     bars = plt.bar(names, hours, color=colors[:len(names)])
    
#     # Προσθήκη τιμών πάνω από τις μπάρες
#     for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval} ώρες", ha='center', va='bottom')
    
#     # Προσθήκη οριζόντιας γραμμής για τον ελεύθερο χρόνο
#     plt.axhline(y=user_total_free_hours, color='r', linestyle='--', label='Ελεύθερος Χρόνος')
    
#     # Προσθήκη κειμένου για τον ελεύθερο χρόνο
#     if len(names) > 0:
#         plt.text(len(names)-0.5, user_total_free_hours + 0.5, f"Ελεύθερος Χρόνος: {user_total_free_hours} ώρες", color='r', va='bottom')
    
#     # Προσθήκη λεζάντας
#     plt.legend()
    
#     # Τίτλοι και ετικέτες
#     plt.xlabel("Δραστηριότητες")
#     plt.ylabel("Ώρες")
#     plt.title("Ώρες ανά Δραστηριότητα")
    
#     # Περιστροφή ετικετών για καλύτερη αναγνωσιμότητα
#     plt.xticks(rotation=45, ha='right')
    
#     # Προσθήκη grid για καλύτερη οπτικοποίηση
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
    
#     # Αυτόματη προσαρμογή αποστάσεων για βέλτιστη εμφάνιση
#     plt.tight_layout()
    
#     # Εμφάνιση του γραφήματος
#     plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------
