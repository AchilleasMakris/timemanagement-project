import csv
#TODO:Αν δεν έχω εισάγει δραστηριότητες και επιλέξω 3 - Τροποποίηση έχω error
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
def save_user_to_csv(arxeio = "users.csv"):
    """
        Αποθηκεύει τους χρήστες σε αρχείο csv καταχωρώντας το username και το password τους.
    """
    with open(arxeio, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames= ["username", "password", "user_total_free_hours"])
        writer.writeheader()
        writer.writerows(users)

# Φόρτωση χρηστών απο csv
def load_users_from_csv(arxeio = "users.csv"):
    """
        Φορτώνει τα στοιχεία χρηστών (username, password, ελύθερος χρόνος) απο το αρχείο csv.
    """
    try:
        with open (arxeio,mode="r", newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({"username" : row['username'] , "password" : row['password'], "user_total_free_hours" : row['user_total_free_hours']})
    except FileNotFoundError:
        print("Το αρχείο χρηστών δεν βρέθηκε. Δημιουργεία νέου αρχείου με την προσθήκη νέου χρήστη.")


#---------------------------------------------------------- Διαχεριση δραστρηριοτήτων -----------------------------------------------------------

# Αποθήκευση δραστηριοτήτων σε csv
def save_activities_to_csv(arxeio = "activities.csv"):
    with open (arxeio, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username","Δραστηριότητα","Διάρκεια","Σημαντικότητα","Τύπος"])
        writer.writeheader()
        writer.writerows(activities)


# Φόρτωση δραστηριοτήτων απο csv
def load_activities_from_csv(arxeio="activities.csv"):
    try:
        with open(arxeio, mode="r", newline="", encoding="utf-8") as file:  # Specify UTF-8 encoding
            reader = csv.DictReader(file)
            for row in reader:
                # Φόρτωμα και διαχείριση των δραστηριοτήτων στην λίστα activities με όλες τις δραστηριότητες.
                activities.append({
                    "username": row["username"],
                    "Δραστηριότητα": row["Δραστηριότητα"],
                    "Διάρκεια": float(row["Διάρκεια"]),
                    "Σημαντικότητα": int(row["Σημαντικότητα"]),
                    "Τύπος": row["Τύπος"]
                })
    except FileNotFoundError:
        print("Δημιουργία αρχείου δραστηριοτήτων.")
    except UnicodeDecodeError:
        print("Σφάλμα αποκωδικοποίησης. Βεβαιωθείτε ότι το αρχείο είναι σε UTF-8 κωδικοποίηση.")

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

    return user_activities,total_activity_hours,user_ypoxrewseis, total_ypoxrewseis_hours,user_hobbies, total_hobby_hours

# Επιλογή του διαθέσιμου χόνου που ανήκει στον συνδεδεμένο χρήστη
def get_user_total_free_hours(connected_user, users):
    for user in users:
        if user["username"] == connected_user:
            user_total_free_hours = float(user["user_total_free_hours"])
    return user_total_free_hours


# Συνάρτηση εισαγωγής ονόματος δραστηριότητας ΄ή υποχρέωσης
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
        

# Εισαγωγή συνολικού ελεύθερου χρόνου
def eleutheros_xronos(total_activity_hours):
    #TODO CHECK user_total_free_hours για temp
    """ 
        Εισάγει τον ελεύθερο χρόνο. Αν ο χρήστης επιλέξει να προσθέσει περισσότερο νέο χρόνο τότε:
        απο τον νέο χρόνο που πρόσθεσε αφαιρούνται οι ώρες που απαιτούνται για τις ήδη υπάρχουσες δραστηριότητες.
    """
    #TODO CHECK!
    #print (total_activities_hours)
    while True:
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



# Προσθήκη δραστηριότητας
def add_activity(user_total_free_hours, connected_user, user_activities, activities):

    """ Εισάγει νέα δραστηριότητα ελέγχοντας πρώτα αν δεν έχει μηδενιστεί ο ελεύθερος χρόνος (μέσω της terminate).
        Καλεί τις συναρτήσεις εισαγωγής:
        name() για: όνομα,
        duration() για: διάρκεια,
        eleutheros_xronos() για: ελεύθερο χρόνο(αν δεν έχει γίνει εισαγωγή ελεύθερου χρόνου πιο πριν),
        importance() για: βαθμό σημαντικότητας.
        Στην συνέχεια δημιουργεί dictionary για κάθε δραστηριότητα και το αποθηκεύει στην λίστα activities.
    """

    global terminate, total_ypoxrewseis, total_hobby, total_activities, total_activity_hours, total_ypoxrewseis_hours, user_hobbies, total_hobby_hours

    if user_total_free_hours > 0 and user_activities:
        terminate=False

    if terminate == False: # Αν έχω διαθέσιμο ελεύθερο χρόνο μπορώ να εισάγω νέα δραστηριότητα
        while True:

        #Eπιλογή τύπου δραστηριότητας, 1 για Υποχρέωση ή 2 για Χόμπι.
            while True:
                try:
                    choice = int(input(("Πληκτρολογείστε 1 για Υποχρέωση ή 2 για Χόμπι: ")))
                    if choice in [1,2]:
                        if choice == 1:
                            type = "Υποχρέωση"
                        else:
                            type = "Χόμπι"
                        break
                    print("Η επιλογή δεν υπάρχει. Παρακαλώ προσπαθήστε ξανά.")
                except ValueError:
                    print("Μη έγκυρη είσοδος.")



            while True:
                onoma = name()
                if any(activity["Δραστηριότητα"] == onoma for activity in user_activities):
                    print("\nΗ δραστηριότητα υπάρχει ήδη.")
                else:
                    break

        #Εισαγωγή διάρκειας δραστηριότητας

            # αν οι συνολικές διαθέσιμες ώρες είναι 0 , εισαγωγή των ωρών πρώτα
            if user_total_free_hours == 0:
                #TODO Check αν ο χρηστης βαλει λιγοτερο χρονο αποτι ειχε πριν
                user_total_free_hours = eleutheros_xronos(total_activity_hours)

            #Εισαγωγή διάρκειας δραστηριότητας
            diarkeia, user_total_free_hours = duration(user_total_free_hours) # Δέχεται το total_hours για τον εκ νέου υπολογισμό του και το στέλνει πίσω μαζί με την diarkeia με το return
            total_activity_hours += diarkeia # Υπολογισμός του συνολικού χρόνου που απαιτείται για όλες τις δραστηριότητες.

        # Eισαγωγή σημαντικότητας
            grade = importance()


        # Αν μηδενίστηκαν οι ώρες με την είσοδο της τελευταίας δραστηριότητας:
            if user_total_free_hours == 0: # Αν μηδενιστούν οι ελεύθερες ώρες τότε το terminate γινεταί True και δεν αφήνει να μπούμε εκ νέου στην λειτουργία προσθήκης δραστηριότητας
                    print("\nΜε την προσθήκη αυτής της δραστηριότητας έχει εξαντληθεί ο διαθέσιμος ελεύθερος χρόνος σας!")
                    terminate = True


        # Εισαγωγή του στοιχείου στην λίστα με τα dictionaries
            # Αποθήκευση ως dictionary με όνομα activity
            activity = {
                "username" : connected_user, # ------------------------------- Προστέθηκε τώρα
                "Δραστηριότητα" : onoma,
                "Διάρκεια" : diarkeia,
                "Σημαντικότητα" : grade,
                "Τύπος" : type
            }

            # Αν η επιλογή είναι 1 τότε προσθέτω την δραστηριότητα και στην λίστα με τις υποχρεώσεις.
            if choice == 1:
                user_ypoxrewseis.append(activity)
                total_ypoxrewseis_hours += diarkeia # Υπολογισμός του συνολικού χρόνου που απαιτείται για τις υποχρεώσεις.
            else: # Αν η επιλογή είναι 2 τότε προσθέτω την δραστηριότητα και στην λίστα με τα χόμπι.
                user_hobbies.append(activity)
                total_hobby_hours += diarkeia # Υπολογισμός του συνολικού χρόνου που απαιτείται για τα χόμπι.
            

            # Προσθήκη του dictionary στην λίστα
            user_activities.append(activity)
            activities.append(activity)
            for user in users:
                if connected_user == user["username"]:
                    user["user_total_free_hours"] = user_total_free_hours

            #save_activities_to_csv()
            return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours, total_activity_hours
    else:
        print("\nΔεν έχετε διαθέσιμό ελεύθερο χρόνο, παρακαλώ τροποποιήστε ή διαγράψτε κάποια δραστηριότητα ή επιλέξτε να προσθέσετε ελεύθερο χρόνο")
        return user_total_free_hours , total_hobby_hours, total_ypoxrewseis_hours, total_activity_hours #BUG!

    """Άν μπεί με 0 για πρώτη φορά τρέχει κανονικά την loop αφου το terminate εχει αρχικοποιηθεί σε False. Όμως το terminate γίνεται True.
        Αν μπεί για 2η συνεχόμενη φορά με 0 μέσω της επιλογής 1 απο το μενού τότε δεν επέστρεφε καμιά τιμή"""

# Εμφάνιση όλων των αποθηκευμένων δραστηριοτήτων
def display_activities(user_activities):
    """Προβάλει τις αποθηκευμένες δραστηριότητες ή αν δεν υπάρχουν, ενημερώνει με κατάλληλο μήνυμα."""
    if not user_activities:
        print("\nΔεν βρέθηκαν δραστηριότητες.\n")
    else:
        print("\nΟι δραστηριότητες που έχετε να κάνετε αυτή την εβδομάδα είναι: \n")
        for drastiriotita in user_activities:
            print (f"{drastiriotita['Δραστηριότητα']} : Διάρκεια: {drastiriotita['Διάρκεια']} ώρες | Βαθμός σημαντικότητας: {drastiriotita['Σημαντικότητα']} | Τύπος: {drastiriotita['Τύπος']}")

# Ταξινόμηση 
def taksinomisi (x):
    activities.sort(key = lambda x: x["Σημαντικότητα"], reverse=True)
    return activities

# Τροποποίηση
def modify(user_activities, total_hobby_hours, total_ypoxrewseis_hours, connected_user, users):
    
    """
        Αν δεν έχουν καταχωρηθεί δραστηριότητες η συνάρτηση εμφανίζει κατάλληλο μήνυμα και τερματίζει. Αν υπάρχουν δραστηριότητες τοτε τις εμφανίζει
        και καλεί ένα μενού επιλογών τροποποίησης. Ο χρήστης επιλέγει μια δυνατότητα με βάση το μενού. Κάθε φορά που πραγματοποιείται μια αλλαγή 
        ενημερώνεται η λίστα των δραστηριοτήτων και η συνάρτηση κλείνει και επιστρέφω στο κεντρικό μενού.
    """
    global user_total_free_hours
    if not user_activities:
        print ("\nΔεν υπάρχουν δραστηριότητες για τροποποίηση.")
        return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours
    
    # Εμφάνιση και επιλογή διαθέσιμων δραστηριοτήτων
    print ("\nΕπιλέξτε μία απο τις διαθέσιμες δραστηριότητες για τροποποίηση: \n")
    for activity in user_activities:
        print (f"{activity['Δραστηριότητα']}")
    
    # Έξωτερικός βρόγχος 
    while True:
        
        # Επιλογή του χρήστη 
        choice = input().strip()

          
        for activity in user_activities:
            
            # Αν η επιλογή του χρήστη υπάρχει τότε μπορεί να την τροποποιήσει, αλλίως ενημέρωση ότι η εισαγωγή του δεν υπάρχει
            if activity["Δραστηριότητα"] == choice:  #if any(activity["Δραστηριότητα"] == choice for activity in activities): Αυτο είναι λάθος, για κάποιο λόγο δεν "βλέπει" την πρώτη αποθηκευμένη δραστηριοτητα. Γιατί;
                
                # Μενού επιλογών τροποποίησης
                print("\nΔυνατότητες τροποποίησης: \n")
                print("1. Τροποποίηση ονόματος δραστηριότητας")
                print("2. Τροποποίηση διάρκειας δραστηριότητας")
                print("3. Τροποποίηση βαθμού σημαντικότητας δραστηριότητας")
                print("4. Ακύρωση\n")
                
                
                dynatotita = epilogi(x=4)
                
                if dynatotita == 1:
                    while True:
                        onoma = name()
                        if any(activity["Δραστηριότητα"] == onoma for activity in user_activities):
                            print("\nΗ δραστηριότητα υπάρχει ήδη. Παρακαλώ εισάγετε διαφορετικό όνομα δραστηριότητας.")
                            #return  total_hours, total_hobby, total_ypoxrewseis
                        else:
                            # Aν η δραστηριότητα που θέλω να αλλάξω είναι Υποχρέωση τότε αλλάζω το όνομα της και στην λίστα ypoxrewseis()
                            if activity["Τύπος"] == "Υποχρέωση":
                                for ypoxrewsi in user_ypoxrewseis:
                                    if activity["Δραστηριότητα"] == ypoxrewsi["Δραστηριότητα"]:
                                        ypoxrewsi["Δραστηριότητα"] = onoma
                            else: # Aν η δραστηριότητα που θέλω να αλλάξω είναι χόμπι τότε αλλάζω το όνομα της και στην λίστα hobby()
                                for xompi in user_hobbies:
                                    if activity["Δραστηριότητα"] == xompi["Δραστηριότητα"]:
                                        xompi["Δραστηριότητα"] = onoma


                            activity["Δραστηριότητα"] = onoma
                            print("\nΤο όνομα της δραστηριότητας άλλαξε σε: ", activity["Δραστηριότητα"])
                            
                            return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours
                elif dynatotita == 2:
                    # Αλλάζει το total_hours προσθέτωντας πίσω την προηγούμενη διάρκεια
                    user_total_free_hours += activity["Διάρκεια"] 
                    print("\nΟι διαθέσιμες ώρες σας είναι: " , user_total_free_hours, "ώρες.")
                    # Κλήση της duration για εισαγωγή νέας διάρκειας και υπολογισμό του total_hours εκ νέου
                    diarkeia, user_total_free_hours = duration(user_total_free_hours)

                    # Aν η δραστηριότητα που θέλω να αλλάξω είναι Υποχρέωση τότε αλλάζω την Διάρκεια της και στην λίστα ypoxrewseis()
                    if activity["Τύπος"] == "Υποχρέωση":
                        for ypoxrewsi in user_ypoxrewseis:
                            if activity["Δραστηριότητα"] == ypoxrewsi["Δραστηριότητα"]:
                                
                                total_ypoxrewseis_hours -= ypoxrewsi["Διάρκεια"]
                                
                                ypoxrewsi["Διάρκεια"] = diarkeia
                                
                                total_ypoxrewseis_hours += ypoxrewsi["Διάρκεια"]
                            
                    else: # Aν η δραστηριότητα που θέλω να αλλάξω είναι χόμπι τότε αλλάζω την Διάρκεια της και στην λίστα hobby()
                        for xompi in user_hobbies:
                            if activity["Δραστηριότητα"] == xompi["Δραστηριότητα"]:
                                total_hobby_hours -= xompi["Διάρκεια"]
                                xompi["Διάρκεια"] = diarkeia
                                total_hobby_hours += xompi["Διάρκεια"]
                    
                    # Καταχώρηση αλλαγής διάρκειας στο dict
                    activity["Διάρκεια"] = diarkeia
                    print(f'\nH διάρκεια της δραστηριότητας "{activity['Δραστηριότητα']}" άλλαξε σε: {activity['Διάρκεια']} ώρες.')
                    print("\nΟ νέος διαθέσιμος χρόνος είναι: ", user_total_free_hours)
                    for user in users:
                        if user["username"] == connected_user:
                            user["user_total_free_hours"] = user_total_free_hours
                            break
                    return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours
                
                elif dynatotita == 3:
                    activity["Σημαντικότητα"] = importance()
                    print(f'\nΟ βαθμός σημαντικότητας της δραστηριότητας "{activity["Δραστηριότητα"]}" άλλαξε σε {activity["Σημαντικότητα"]}')

                    return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours
                else:
                    print ("\nΈξοδος απο το μενού τροποποίσης.")
                    return user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours
                    
            # Αν η επιλογή δεν είναι έγκυρη      
            else:
                print ("\nH δραστηριότητα που επιλέξατε δεν υπάρχει, παρακαλώ επιλέξτε μια από τις παρακάτω: \n")
                for activity in user_activities:
                    print (f"{activity['Δραστηριότητα']}")

# Διαγραφή
def delete_activity(user_activities, total_ypoxrewseis_hours, total_hobby_hours, total_activity_hours, user_ypoxrewseis, user_hobbies, user_total_free_hours, connected_user, users):
    """
        Εμφάνιση όλων των δραστηριοτήτων μέσω της display_activities. Ο χρήστης επιλέγει κάποια, αν επιλέξει κάποια που δεν υπάρχει τότε εμφανίζεται κατάλληλο μήνυμα.
        Αν επιλέξει κάποια που υπάρχει τότε βρίσκει αν ειναι υποχρέωση ή χόμπι. Διαγράφει την δραστηριότητα απο την λίστα υποχρεώσεων ή χόμπι. Διαγράφει την δραστηριότητα
        απο την λιστα όλων των δραστηριοτήτων. Ο χρόνος της δραστηριότητας αφαιρείται απο τον συνολικό χρόνο δραστηριοτήτων και τον συνολικό χρόνο υποχρ. ή χόμπι και στο
        #TODO που είναι ο συνολικός διαθέσιμος ελεύθερος χρόνος, προστίθεται η διάρκεια της δραστηριότητας που διαγράφθηκε.
    """
    # Αν δεν έχουν καταχωρηθεί δραστηριότητες: κατάλληλο μήνυμα και επιστροφή στο main()
    if not user_activities:
        print ("\nΔεν υπάρχουν δραστηριότητες για διαγραφή.")
        return total_ypoxrewseis_hours, total_hobby_hours, user_total_free_hours, total_activity_hours
    
    # Εμφάνιση και επιλογή διαθέσιμων δραστηριοτήτων
    print ("\nΕπιλέξτε μία απο τις διαθέσιμες δραστηριότητες για διαγραφή: \n")
    for activity in user_activities:
        print (f"{activity['Δραστηριότητα']}")

    
    while True:
        # Επιλογή του χρήστη 
        choice = input().strip()

          
        for activity in user_activities:
            
            # Αν η επιλογή του χρήστη υπάρχει τότε μπορεί να την διαγράψει, αλλίως ενημέρωση ότι η εισαγωγή του δεν υπάρχει
            if activity["Δραστηριότητα"] == choice:
                
                # Αν δόθηκε υπάρχουσα δραστηριότητα τότε κρατάω την διάρκειά της

                # Aν η δραστηριότητα που θέλω να διαγράψω είναι Υποχρέωση τότε την διαγράφω και από λίστα ypoxrewseis()
                if activity["Τύπος"] == "Υποχρέωση":
                    total_ypoxrewseis_hours -= activity["Διάρκεια"]
                    for act in user_ypoxrewseis:
                        if act["Δραστηριότητα"] == choice:
                            user_ypoxrewseis.remove(act)
                    
                
                else: # Aν η δραστηριότητα που θέλω να διαγράψω είναι χόμπι τότε την διαγράφω και από λίστα hobby()
                    total_hobby_hours -= activity["Διάρκεια"]
                    for act in user_hobbies:
                        if act["Δραστηριότητα"] == choice:
                            user_hobbies.remove(act)
                
                # Διαγραφή απο την λίστα όλων των δραστηριοτήτων
                user_total_free_hours += activity["Διάρκεια"]
                total_activity_hours -= activity["Διάρκεια"]
                user_activities.remove(activity)
                activities.remove(activity)
                
                # Update User List
                for user in users:
                    if user["username"] == connected_user:
                        user["user_total_free_hours"] = user_total_free_hours
                        break
                print(f'\nΗ δραστηριότητα "{activity["Δραστηριότητα"]}" αφαιρέθηκε.')
                return total_ypoxrewseis_hours, total_hobby_hours, user_total_free_hours, total_activity_hours

            # Αν η επιλογή δεν είναι έγκυρη      
            else:
                print ("\nH δραστηριότητα που επιλέξατε δεν υπάρχει, παρακαλώ επιλέξτε μια από τις παρακάτω: \n")
                for activity in user_activities:
                    print (f"{activity['Δραστηριότητα']}")

    
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

#-------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    load_activities_from_csv()
    load_users_from_csv()
    global users
    global activities

    global user_ypoxrewseis
    global user_hobbies
    global user_activities
    global user_total_free_hours


    global week_hours
    global total_ypoxrewseis_hours
    global total_hobby_hours
    global total_activity_hours
    

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
                # print("user total free hours = ", user_total_free_hours)
                # print("-*10" + "TEST")
                # print("user activities = ", user_activities)
                # print("user total activities = ", total_activity_hours)
                # print("user_ypoxrewseis = ", user_ypoxrewseis)
                # print("total_ypoxrewseis = ", total_ypoxrewseis_hours)
                # print("user_hobbies = ", user_hobbies)
                # print("total_hobby = ", total_hobby_hours)

                while True:
                    display_menu()
                    leitourgia = epilogi(x=9)
                    
                    if leitourgia == 1:
                        user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours, total_activity_hours = add_activity(user_total_free_hours, connected_user, user_activities, activities) #-----------Προστέθηκε τώρα
                        print("Ypoxrewseis sthn main ", user_ypoxrewseis)
                        taksinomisi(user_activities)
                        taksinomisi(user_ypoxrewseis)
                        taksinomisi(user_hobbies)
                        save_activities_to_csv()
                        save_user_to_csv()

                    elif leitourgia == 2:
                        display_activities(user_activities)
                    
                    elif leitourgia == 3:
                        user_total_free_hours, total_hobby_hours, total_ypoxrewseis_hours = modify(user_activities, total_hobby_hours, total_ypoxrewseis_hours, connected_user, users)
                        taksinomisi(user_activities)
                        taksinomisi(user_ypoxrewseis)
                        taksinomisi(user_hobbies)
                        print("TEST user_total_free_hours = ", user_total_free_hours)
                        save_activities_to_csv()
                        save_user_to_csv()

                    elif leitourgia == 4:
                        total_ypoxrewseis_hours, total_hobby_hours, user_total_free_hours, total_activity_hours = delete_activity(user_activities, total_ypoxrewseis_hours, total_hobby_hours, total_activity_hours, user_ypoxrewseis, user_hobbies, user_total_free_hours, connected_user, users)
                        save_activities_to_csv()
                        save_user_to_csv()

                    elif leitourgia == 5:
                        display_FreeTime(user_total_free_hours,user_activities)

                    elif leitourgia == 6:
                        user_total_free_hours = eleutheros_xronos(total_activity_hours)
                        print (user_total_free_hours)
                        print (users)
                        update_users_list(connected_user, user_total_free_hours)
                        save_user_to_csv()
                    else:
                        save_user_to_csv()
                        save_activities_to_csv()
                        clear_data(user_activities, user_ypoxrewseis, user_hobbies) # Διαγραφή των λιστών του χρήστη
                        print("\nΈξοδος χρήστη.\n")
                        break
                   

                    """"
                    elif leitourgia == 7:

                        display_ypoxrewseis(user_ypoxrewseis,total_ypoxrewseis)

                    elif leitourgia == 8:
                        display_hobby(user_hobby, total_hobby)

                    """
#--------------------------------------------------------- ΤΕΛΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ --------------------------------------------------------------------

    # Αν ο χρήστης επιλέξει το 3 τότε γίνεται τερματισμός του προγράμματος.
        else:
            break



main()  # Εκκίνηση του προγράμματος
