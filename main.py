import csv
import matplotlib.pyplot as plt
import hashlib

 #---------------------------------------------------------Αρχικοποίηση μεταβλητών----------------------------------------------------------------

users = []                      # Λίστα με όλους τους χρήστες
activities = []                 # Λίστα με όλα τα Activities

user = {}                       # username, password, user_total_free_hours
activity = {}                   # connected_user, onoma, diarkeia, grade, type

user_ypoxrewseis = []           # Temp λίστα για αποθήκευση των Υποχρεώσεων
user_hobbies = []               # Temp λίστα για αποθήκευση των Hobbies
user_activities = []            # Temp λίστα για αποθήκευση των Activities

week_hours = 168                # Συνολικές ώρες της εβδομάδας
total_ypoxrewseis_hours = 0     # Συνολικές ώρες υποχρεώσεων του χρήστη
total_hobby_hours = 0           # Συνολικές ώρες των Hobby του χρήστη
total_activity_hours = 0        # Συνολικές ώρες ΌΛΩΝ των Activities
terminate = False               # Flag για έλεγχο τιμής

#--------------------------------------------------------- Αποθήκευση αρχείων --------------------------------------------------------------------


#--------------------------------------------------------- Διαχείριση χρηστών ------------------------------------------------------------------

# Αποθήκευση του χρήστη σε csv
def save_user_to_csv(filename="users.csv"):
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "user_total_free_hours", "backup_user_free_hours"])
        writer.writeheader()
        writer.writerows(users)

# Φόρτωση χρηστών απο csv
def load_users_from_csv(filename="users.csv"):
    users.clear()
    try:
        with open(filename, mode="r", newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    "username": row['username'],
                    "password": row['password'],
                    "user_total_free_hours": float(row.get('user_total_free_hours')),
                    "backup_user_free_hours": float(row.get('backup_user_free_hours'))
                })
    except FileNotFoundError:
        pass  # File will be created on first save
#---------------------------------------------------------- Διαχεριση δραστρηριοτήτων -----------------------------------------------------------

# Αποθήκευση δραστηριοτήτων σε csv
def save_activities_to_csv(filename="activities.csv"):
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "Δραστηριότητα", "Διάρκεια", "Σημαντικότητα", "Τύπος"])
        writer.writeheader()
        writer.writerows(activities)


# Φόρτωση δραστηριοτήτων απο csv
def load_activities_from_csv(filename="activities.csv"):
    activities.clear()
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                activities.append({
                    "username": row["username"],
                    "Δραστηριότητα": row["Δραστηριότητα"],
                    "Διάρκεια": float(row["Διάρκεια"]),
                    "Σημαντικότητα": int(row["Σημαντικότητα"]),
                    "Τύπος": row["Τύπος"]
                })
    except FileNotFoundError:
        pass
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
     # Check για κενό όνομα/κωδικό
    if not username.strip():
        return False, "Το όνομα χρήστη δεν μπορεί να είναι κενό."
    if not password.strip():
        return False, "Ο κωδικός δεν μπορεί να είναι κενός."
    if any(u["username"] == username for u in users):
        return False, "Το όνομα χρήστη χρησιμοποιείται ήδη."
    if password != password_confirm:
        return False, "Οι κωδικοί δεν είναι ίδιοι."
    password_hash = hash_password(password)
    user = {
        "username": username,
        "password": password_hash,
        "user_total_free_hours": 0.0,
        "backup_user_free_hours": 0.0
    }
    users.append(user)
    save_user_to_csv()
    return True, f"Ο χρήστης {username} δημιουργήθηκε επιτυχώς."

# Σύνδεση χρήστη
def connect_user(username, password):
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
    user_activities = []
    user_ypoxrewseis = []
    user_hobbies = []
    return user_activities, user_ypoxrewseis, user_hobbies

# Επιλογή των δραστηριοτήτων που ανήκουν στον συνδεδεμένο χρήστη
def get_user_activities(connected_user, activities, total_activity_hours, total_hobby_hours, total_ypoxrewseis_hours):
    clear_data(user_activities, user_ypoxrewseis, user_hobbies) # Το καλώ για τον καθαρισμό των λιστών
    for activity in activities:
        if activity["username"] == connected_user:
            user_activities.append(activity)
            total_activity_hours += float(activity["Διάρκεια"])
            if activity["Τύπος"] == "Υποχρέωση":
                user_ypoxrewseis.append(activity)
                total_ypoxrewseis_hours += float(activity["Διάρκεια"])
            else:
                user_hobbies.append(activity)
                total_hobby_hours += float(activity["Διάρκεια"])

    return user_activities,total_activity_hours,user_ypoxrewseis, total_ypoxrewseis_hours,user_hobbies, total_hobby_hours

# Επιλογή του διαθέσιμου χόνου που ανήκει στον συνδεδεμένο χρήστη
def get_user_total_free_hours(connected_user, users):
    while True:    
        for user in users:
            if user["username"] == connected_user:
                user_total_free_hours = float(user["user_total_free_hours"])
                if user_total_free_hours < 0 or user_total_free_hours > 168:
                    continue
            else:
                return user_total_free_hours

# Συνάρτηση εισαγωγής ονόματος δραστηριότητας ή υποχρέωσης
def name():
    """Εισάγει / τροποποιεί το όνομα της δραστηριότητας"""

    # Εισαγωγή ονόματος, αφαιρώ τα κενά space πρίν και μετά το όνομα. 
    onoma = input("Δώστε το όνομα της δραστηριότητας: ").strip()
            
    """"
        Έλεγχος ονόματος, αν δωθεί το κενό τότε το διαγράφω με την strip επομένως onoma = False και μπαίνω στην επανάληψη
        ή αν κανένα απο τα στοιχεία του ονόματος δεν είναι χαρακτήρας.
    """
    while not onoma or not any(char.isalpha() for char in onoma):
        onoma = input("Το όνομα της δραστηριότητας δεν μπορεί να είναι κενό ή αριθμός, παρακαλώ επανεισάγετε το όνομα: ").strip()
    return onoma

# Συνάρτηση εισαγωγής διάρκειας δραστηριότητας ή υποχρέωσης
def duration(user_total_free_hours):
    
    # Εισαγωγή διάρκειας με έλεγχο ορθότητας (Δεν μπορεί να υπερβαίνει τον συνολικό ελεύθερο χρόνο, τις 168 ώρες της εβδομάδας και να είναι αρνητική ή χαρακτήρας).
    while True:
        try:
            diarkeia = input("\nΔώστε την διάρκεια της δραστηριότητας σε ώρες: ").strip()
            diarkeia = float(diarkeia)
            if diarkeia and 0 < diarkeia <= user_total_free_hours:
                user_total_free_hours -= diarkeia
                # Επιστρέφει την νέα τιμή
                return diarkeia, user_total_free_hours
            else:
                if diarkeia + user_total_free_hours > week_hours:
                    print(f"\nΗ διάρκεια πρέπει να είναι θετικός αριθμός και δεν μπορεί να ξεπερνάει τις {user_total_free_hours} διαθέσιμες ώρες ή τις 168 ώρες της εβδομάδας.")
        except ValueError:
            print("\nΜή έγκυρη είσοδος, παρακαλώ εισάγετε έναν αριθμό ωρών.")
        
        try:
            user_total_free_hours = input("Παρακαλώ εισάγετε τις συνολικές ώρες που έχετε διαθέσιμες για αυτήν την εβδομάδα: ").strip()
            user_total_free_hours = float(user_total_free_hours)
            
            if 0 <= user_total_free_hours <= 168 and user_total_free_hours > total_activity_hours:
                user_total_free_hours -= total_activity_hours
                if activities:
                    print(f"\nΑφαιρέθηκαν {total_activity_hours} ώρες από τον νέο συνολικό σας χρόνο για τις ήδη υπάρχουσες δραστηριότητές σας.")
                    print(f"\nΟ νέος συνολικός ελεύθερος χρόνος σας είναι: {user_total_free_hours}.")

                return user_total_free_hours
            else:
                if total_activity_hours > user_total_free_hours:
                    print(f"\nΕισάγετε παραπάνω ώρες! Απαιτούνται {total_activity_hours} ώρες για τις ήδη υπάρχουσες δραστηριότητές σας.")
                elif total_activity_hours == user_total_free_hours:
                    print(f"Εισάγετε παραπάνω ώρες. Απαιτούνται ήδη {user_total_free_hours} για τις υπάρχουσες δραστηριότητες.")
                else:
                    print("Οι συνολικές διαθέσιμές ώρες δεν μπορούν να είναι αρνητικός αριθμός ή περισσότερες από τις 168 ώρες της εβδομάδας.")
                
        except ValueError:
            print ("Μή έγκυρη είσοδος. Παρακαλώ εισάγετε τον αριθμό των διαθέσιμων ωρών.")
# Συνάρτηση εισαγωγής βαθμού σημαντικότητας
def importance():
    while True:
        try:    
            grade = input("Δώστε τον βαθμό σημαντικότητας (1-10): ").strip()
            grade = int(grade)
            if grade and 1 <= grade <= 10:
                return grade
            else:
                print("Παρακαλώ δώστε έναν βαθμό απο το 1 εώς το 10.")
        except ValueError:
            print("Μή έγκυρη τιμή.")


# Ταξινόμηση 
def taksinomisi(current_user):
    # Clear and rebuild user_activities list for the connected user
    user_activities = [activity for activity in activities if activity["username"] == current_user]
    
    # Sort by type first (Υποχρέωση first), then by importance
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
    
    # Check if enough free time is available    -------------------
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
    activities.append(activity)
    
    # Update user's free time
    user_total_free_hours -= diarkeia
    for user in users:
        if user["username"] == connected_user:
            user["user_total_free_hours"] = user_total_free_hours
            break
    
    save_activities_to_csv()
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
    """
    for activity in activities:
        if activity["username"] == connected_user and activity["Δραστηριότητα"] == onoma:
            if new_onoma and new_onoma != onoma:
                if any(a["Δραστηριότητα"] == new_onoma and a["username"] == connected_user for a in activities):
                    return False, "Το νέο όνομα υπάρχει ήδη."
                activity["Δραστηριότητα"] = new_onoma
            
            if new_diarkeia is not None:
                old_diarkeia = activity["Διάρκεια"]
                for user in users:
                    if user["username"] == connected_user:
                        user_total_free_hours = user["user_total_free_hours"] + old_diarkeia - new_diarkeia
                        if user_total_free_hours < 0:
                            return False, "Δεν υπάρχει αρκετός ελεύθερος χρόνος για αυτή την αλλαγή."
                        user["user_total_free_hours"] = user_total_free_hours
                        break
                activity["Διάρκεια"] = new_diarkeia
            
            if new_grade is not None:
                activity["Σημαντικότητα"] = new_grade
            
            if new_type:
                activity["Τύπος"] = new_type
            
            save_activities_to_csv()
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
    """
    for activity in activities:
        if activity["username"] == connected_user and activity["Δραστηριότητα"] == onoma:
            diarkeia = activity["Διάρκεια"]
            activities.remove(activity)
            for user in users:
                if user["username"] == connected_user:
                    user["user_total_free_hours"] += diarkeia
                    break
            save_activities_to_csv()
            save_user_to_csv()
            return True, "Δραστηριότητα διαγράφηκε επιτυχώς."
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
    """
    # Input validation: free time must be >0 and <=168
    if user_total_free_hours <= 0 or user_total_free_hours > 168:
        return False, "Ο συνολικός ελεύθερος χρόνος πρέπει να είναι μεγαλύτερος του 0 και μικρότερος ή ίσος με 168."
    total_activity_hours = sum(task["Διάρκεια"] for task in activities if task["username"] == connected_user)
    # if user_total_free_hours < total_activity_hours:
    #     return False, f"Ο νέος χρόνος πρέπει να είναι τουλάχιστον {total_activity_hours} ώρες για τις υπάρχουσες δραστηριότητες."
    
    for user in users:
        if user["username"] == connected_user:
            user["user_total_free_hours"] = user_total_free_hours - total_activity_hours
            save_user_to_csv()
            return True, f"Ελεύθερος χρόνος ενημερώθηκε επιτυχώς σε: {user_total_free_hours}."


# Εμφάνιση όλων των αποθηκευμένων δραστηριοτήτων
def display_activities(user_activities):
    """Προβάλει τις αποθηκευμένες δραστηριότητες ή αν δεν υπάρχουν, ενημερώνει με κατάλληλο μήνυμα."""
    if not user_activities:
        print("\nΔεν βρέθηκαν δραστηριότητες.\n")
    else:
        print("\nΟι δραστηριότητες που έχετε να κάνετε αυτή την εβδομάδα είναι: \n")
        for drastiriotita in user_activities:
            print (f"{drastiriotita['Δραστηριότητα']} : Διάρκεια: {drastiriotita['Διάρκεια']} ώρες | Βαθμός σημαντικότητας: {drastiriotita['Σημαντικότητα']} | Τύπος: {drastiriotita['Τύπος']}")

# Εμφάνιση του συνολικού ελεύθερου χρόνου
def display_FreeTime(user_total_free_hours,user_activities):
    """Προβάλει τον διαθέσιμο ελεύθερο χρόνο"""
    
    if user_total_free_hours > 0:
        print("\nΟ συνολικός ελεύθερος χρόνος σας για αυτή την εβδομάδα είναι: ", user_total_free_hours, "ώρες.")
    else:
        if not user_activities:
            print("\nΔεν έχετε εισάγει τον διαθέσιμο ελεύθερο χρόνο σας. Παρακαλώ πατήστε το 6 για προσθήκη ελεύθερου χρόνου.")
        else:
            print("\nΔεν έχετε διαθέσιμό ελεύθερο χρόνο, παρακαλώ τροποποιήστε ή διαγράψτε κάποια δραστηριότητα για να ελευθερώσετε χρόνο ή πατήστε 6 για να προσθέσετε ελεύθερο χρόνο")

# Ενημέρωση της λίστας users
def update_users_list(connected_user, user_total_free_hours):
    for user in users:
        if connected_user == user["username"]:
            user["user_total_free_hours"] = user_total_free_hours

def plot_pie_chart(user_activities, user_total_free_hours):
    """
    Δημιουργεί ένα γράφημα πίτας που δείχνει την κατανομή του χρόνου.

    Args:
        user_activities (list): Λίστα με τις δραστηριότητες του χρήστη.
        user_total_free_hours (float): Ο εναπομείνων ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """
    # Έλεγχος αν υπάρχουν δεδομένα για απεικόνιση
    if not user_activities and user_total_free_hours <= 0:
        print("Δεν υπάρχουν δραστηριότητες ή ελεύθερος χρόνος για απεικόνιση.")
        return
    
    # Δημιουργία λιστών για ετικέτες και μεγέθη
    labels = [activity['Δραστηριότητα'] for activity in user_activities]
    sizes = [float(activity['Διάρκεια']) for activity in user_activities]
    
    # Προσθήκη ελεύθερου χρόνου αν είναι μεγαλύτερος από 0
    if user_total_free_hours > 0:
        labels.append("Ελεύθερος χρόνος")
        sizes.append(user_total_free_hours)
    
    # Προσαρμοσμένη συνάρτηση για εμφάνιση ωρών
    def autopct_format(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return f"{absolute} ώρες"
    
    # Δημιουργία γράφηματος πίτας
    plt.pie(sizes, labels=labels, autopct=lambda pct: autopct_format(pct, sizes))
    plt.title("Κατανομή Χρόνου")
    plt.show()

def plot_bar_chart(user_activities, user_total_free_hours):
    """
    Δημιουργεί ένα γράφημα στηλών που δείχνει τις ώρες ανά δραστηριότητα.

    Args:
        user_activities (list): Λίστα με τις δραστηριότητες του χρήστη.
        user_total_free_hours (float): Ο συνολικός ελεύθερος χρόνος του χρήστη.

    Returns:
        None
    """
    if not user_activities:
        print("Δεν υπάρχουν δραστηριότητες για απεικόνιση.")
        return
    
    # Εξαγωγή ονομάτων και ωρών
    names = [activity['Δραστηριότητα'] for activity in user_activities]
    hours = [float(activity['Διάρκεια']) for activity in user_activities]
    
    # Ορισμός παλέτας χρωμάτων
    colors = plt.get_cmap('tab10').colors
    
    # Δημιουργία μπαρών
    bars = plt.bar(names, hours, color=colors[:len(names)])
    
    # Προσθήκη τιμών πάνω από τις μπάρες
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval} ώρες", ha='center', va='bottom')
    
    # Προσθήκη οριζόντιας γραμμής για τον ελεύθερο χρόνο
    plt.axhline(y=user_total_free_hours, color='r', linestyle='--', label='Ελεύθερος Χρόνος')
    
    # Προσθήκη κειμένου για τον ελεύθερο χρόνο
    if len(names) > 0:
        plt.text(len(names)-0.5, user_total_free_hours + 0.5, f"Ελεύθερος Χρόνος: {user_total_free_hours} ώρες", color='r', va='bottom')
    
    # Προσθήκη λεζάντας
    plt.legend()
    
    # Τίτλοι και ετικέτες
    plt.xlabel("Δραστηριότητες")
    plt.ylabel("Ώρες")
    plt.title("Ώρες ανά Δραστηριότητα")
    
    # Περιστροφή ετικετών
    plt.xticks(rotation=45, ha='right')
    
    # Προσθήκη grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Αυτόματη προσαρμογή αποστάσεων
    plt.tight_layout()
    
    # Εμφάνιση του γραφήματος
    plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------
