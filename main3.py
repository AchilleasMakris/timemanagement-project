import csv
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

#--------------------------------------------------------- Αποθήκευση αρχείων --------------------------------------------------------------------


#--------------------------------------------------------- Διαχείριση χρηστών ------------------------------------------------------------------

# Αποθήκευση του χρήστη σε csv
def save_user_to_csv(arxeio = "users.csv"):
    """
        Αποθηκεύει τους χρήστες σε αρχείο csv καταχωρώντας το username και το password τους.
    """
    with open(arxeio, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames= ["username", "password", "user_total_free_hours"])
        writer.writeheader()
        writer.writerows(users)

# Φόρτωση χρηστών απο csv
def load_users_from_csv(arxeio = "users.csv"):
    """
        Φορτώνει τα στοιχεία χρηστών (username, password, ελύθερος χρόνος) απο το αρχείο csv.
    """
    try:
        with open (arxeio,mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({"username" : row['username'] , "password" : row['password'], "user_total_free_hours" : row['user_total_free_hours']})
    except FileNotFoundError:
        print("Το αρχείο χρηστών δεν βρέθηκε. Δημιουργεία νέου αρχείου με την προσθήκη νέου χρήστη.")


#---------------------------------------------------------- Διαχεριση δραστρηριοτήτων -----------------------------------------------------------

# Αποθήκευση δραστηριοτήτων σε csv
def save_activities_to_csv(arxeio = "activities.csv"):
    with open (arxeio, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username","Δραστηριότητα","Διάρκεια","Σημαντικότητα","Τύπος"])
        writer.writeheader()
        writer.writerows(activities)


# Φόρτωση δραστηριοτήτων απο csv
def load_activities_from_csv(arxeio = "activities.csv"):
    try:
        with open(arxeio, mode="r",newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Φόρτωμα και διαχείρηση των δραστηριοτήτων στην λίστα activities με όλες τις δραστηριότητες.
                activities.append({"username": row["username"], "Δραστηριότητα" : row["Δραστηριότητα"], "Διάρκεια" : float(row["Διάρκεια"]), "Σημαντικότητα" : int(row["Σημαντικότητα"]), "Τύπος" : row["Τύπος"]})

    except FileNotFoundError:
        print("Δημιουργία αρχείου δραστηριοτήτων.")

#-------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------ Συναρτήσεις Χρηστών ----------------------------------------------------------------------

# Προσθήκη νέου χρήστη
def register_user(users):
    """
        Δημιουργεί έναν νέο χρήστη ο οποίος αποθηκεύεται στην λίστα users καταχωρώντας το username, το password και τον διαθέσιμο χρόνο.
    """
    username = input("\nΠληκτρολογείστε το όνομα χρήστη: ").strip()
    if any(user.get("username") == username for user in users):
        print("\nΤο όνομα χρήστη χρησιμοποιείται ήδη.")
        return
    while True:
        password_test1 = input("\nΠληκτρολογείστε τον κωδικό πρόσβασης: ").strip()
        password_test2 = input("\nΕπιβεβαιώστε τον κωδικό πρόσβασης: ").strip()
        if password_test1 == password_test2:
            password = password_test1
            print("\nΟ κωδικός καταχωρήθηκε επιτυχώς.")
            break
        else:
            print("Οι κωδικοί δεν είναι ίδιοι. Παρακαλώ πληκτρολογείστε εκ νέου τον κωδικό.")

    user = {
        "username" : username,
        "password" : password,
        "user_total_free_hours" : 0
    }
    users.append(user)

    print(f"\nΟ χρήστης {username} δημιουργήθηκε επιτυχώς.")
    save_user_to_csv()


# Σύνδεση χρήστη
def connect_user(users):
    """
        Καλέι τον χρήστη να εισάγει το username και το password του. Αν τα στοιχεία αυτά(συνδυασμός username και password)
        αντιστιχούν με κάποιο dictionary στην λίστα users τότε έχω επιτυχή είσοδο και προχωράω στις κύριες λειτουργίες του προγράμματος.

        returns: username ούτως ώστε να το αποθηκεύει σε μια μεταβλητή conncected_user
    """
    username = input("Παρακαλώ πληκτρολογείστε το username σας: ").strip()
    password = input("Παρακαλώ πληκτρολογείστε τον κωδικό σας: ").strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"\nΟ χρήστης {user['username']} συνδέθηκε επιτυχώς.")
            return username
    else:
        print("\nΛανθασμένα στοιχεία εισόδου.")


#-------------------------------------------------------- Συναρτήσεις Μενού ----------------------------------------------------------------------
# Eπιλογή λειτουργίας
def epilogi(x):
    while True:
        try:
            epilogi = input("Επέλεξε μια απο τις παραπάνω λειτουργείες: ").strip()
            epilogi = int(epilogi)
            if 1<= epilogi <= x:
                return epilogi
            else:
                print ("Mή έγκυρη τιμή.")
        except ValueError:
            print ("Mή έγκυρη τιμή.")

# Login Menu
def login_menu():
    print("Time Management Login\n")
    print("1. Εγγραφή νέου χρήστη")
    print("2. Σύνδεση χρήστη")
    print("3. Έξοδος")

# Main Menu
def display_menu():
    print("\n","-" * 10 , "Time Management" , "-" * 10 , "\n")
    print("1. Εισαγωγή νέας δραστηριότητας")
    print("2. Εμφάνιση όλων των δραστηριοτήτων")
    print("3. Τροποποίηση δραστηριοτήτων")
    print("4. Διαγραφη δραστηριότητας")
    print("5. Εμφάνιση διαθέσιμου ελεύθερου χρόνου")
    print("6. Προσθήκη διαθέσιμου ελεύθερου χρόνου")
    print("7. Εμφάνιση υποχρεώσεων")
    print("8. Εμφάνιση δραστηριοτήτων ελεύθερου χρόνου")
    print("9. Έξοδος")



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

    return total_ypoxrewseis_hours, total_hobby_hours, total_activity_hours, user_activities, user_ypoxrewseis, user_hobbies


# Επιλογή του διαθέσιμου χόνου που ανήκει στον συνδεδεμένο χρήστη
def get_user_total_free_hours(connected_user, users):
    for user in users:
        if user["username"] == connected_user:
            user_total_free_hours = user["user_total_free_hours"]
    return user_total_free_hours





















#-------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    global users
    global activities

    global user_ypoxrewseis
    global user_hobbies
    global user_activities

    global week_hours
    global total_ypoxrewseis_hours
    global total_hobby_hours
    global total_activity_hours
    load_activities_from_csv()
    load_users_from_csv()

#---------------------------------------------------------- ΠΡΟΒΟΛΗ ΜΕΝΟΥ ΕΙΣΟΔΟΥ ----------------------------------------------------------------
    while True:
        login_menu()
        leitourgia = epilogi(x=3)

        # Αν ο χρήστης επιλέξει το 1 τότε γίνεται εγγραφή νέου χρήστη.
        if leitourgia == 1:
            register_user(users)

        # Αν ο χρήστης επιλέξει το 2 τότε γίνεται σύνδεση του χρήστη.
        elif leitourgia == 2:
            connected_user = connect_user(users)

#----------------------------------------------------------- ΚΥΡΙΩΣ ΠΡΟΓΡΑΜΜΑ --------------------------------------------------------------------

            # Αν ο χρήστης συνδέθηκε επιτυχώς τότε προχωράω στο κυρίως πρόγραμμα.
            if connected_user:
                print(f"Συνδεδεμένος χρήστης: {connected_user}")

                # Φόρτωση των δραστηριοτήτων που ανήκουν μόνο στον συνδεδεμένο χρήστη
                if any(user.get("username") == connected_user for user in activities):  # Αν υπάρχει έστω και μία εγγραφή με το παρόν username, τότε υπάρχουν δραστηριότητες του χρήστη
                    user_activities,total_activity_hours, user_ypoxrewseis, total_ypoxrewseis_hours, user_hobbies ,total_hobby_hours = get_user_activities(connected_user, activities, total_activity_hours, total_hobby_hours, total_ypoxrewseis_hours)

                # Φόρτωση συνολικού διαθέσιμου χρόνου που ανήκει στον συνδεδεμένο χρήστη
                user_total_free_hours = get_user_total_free_hours(connected_user, users)
                print("user total free hours = ", user_total_free_hours)
                print("-*10" + "TEST")
                print("user activities = ", user_activities)
                print("user total activities = ", total_activity_hours)
                print("user_ypoxrewseis = ", user_ypoxrewseis)
                print("total_ypoxrewseis = ", total_ypoxrewseis_hours)
                print("user_hobbies = ", user_hobbies)
                print("total_hobby = ", total_hobby_hours)

                while True:
                    display_menu()
                    leitourgia = epilogi(x=9)
                """
                    if leitourgia == 1:
                        user_total_hours, total_hobby, total_ypoxrewseis, total_activities = add_activity(user_total_hours, connected_user, user_activities, activities) #-----------Προστέθηκε τώρα
                        print("Ypoxrewseis sthn main ", user_ypoxrewseis)
                        taksinomisi(activities)
                        taksinomisi(user_ypoxrewseis)
                        taksinomisi(user_hobby)
                        save_activities_to_csv()
                        save_user_to_csv()


                    elif leitourgia == 2:
                        display_activities(user_activities)

                    elif leitourgia == 3:
                        user_total_hours, total_hobby, total_ypoxrewseis = modify(activities,total_hobby, total_ypoxrewseis)
                        taksinomisi(activities)
                        taksinomisi(user_ypoxrewseis)
                        taksinomisi(user_hobby)
                        save_activities_to_csv()
                        save_user_to_csv()

                    elif leitourgia == 4:
                        total_ypoxrewseis, total_hobby, user_total_hours, total_activities = delete_activity(activities, total_ypoxrewseis, total_hobby, user_total_hours, total_activities, user_ypoxrewseis, user_hobby)
                        save_activities_to_csv()
                        save_user_to_csv()

                    elif leitourgia == 5:
                        display_FreeTime(user_total_hours,user_activities)

                    elif leitourgia == 6:
                        user_total_hours = eleutheros_xronos(total_activities)
                        print (user_total_hours)
                        print (users)
                        update_users_list(connected_user, user_total_hours)
                        save_user_to_csv()


                    elif leitourgia == 7:

                        display_ypoxrewseis(user_ypoxrewseis,total_ypoxrewseis)

                    elif leitourgia == 8:
                        display_hobby(user_hobby, total_hobby)

                    else:
                        clear_data() # Διαγραφή των λιστών του χρήστη
                        print("\nΈξοδος χρήστη.\n")
                        break"""
#--------------------------------------------------------- ΤΕΛΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ --------------------------------------------------------------------

    # Αν ο χρήστης επιλέξει το 3 τότε γίνεται τερματισμός του προγράμματος.
        else:
            break



main()  # Εκκίνηση του προγράμματος
