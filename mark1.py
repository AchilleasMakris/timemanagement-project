""""

# Time management
# Εισαγωγή tkinter

# Μενού εισαγωγής
    # 1 Συνάρτηση: Εισαγωγή
        # α) Υποχρεώσεις ή β) Δραστηριότητες
        # Διάρκεια δραστηριότητας , δεν μπορεί να υπερβαίνει τον συνολικό ελεύθερο χρόνο (<= Ελεύθερος χρόνος) , τις 168 ώρες της εβδομάδας και να είναι αρνητική ή χαρακτήρας.
        # Βαθμός σημαντικότητας (1-10)
        # Συνολικός ελεύθερος χρόνος μέσα στην εβδομάδα, η εβδομάδα έχει 168 ώρες (<=168)

    # 2 Συνάρτηση: Εμφάνιση όλων των δραστηριοτήτων


    # 3 Συνάρτηση: Τροποποίηση
        # Αλλαγή διάρκειας δραστηριότητας
        # Αλλαγή βαθμού σημαντικότητας
        # ΑΝ υπάρξει τροποίηση στην διάρκεια τότε 
            # Έλεγχος επάρκειας συνολικού ελεύθερου χρόνου
            # Επανυπολογισμός του συνολικού ελεύθερου χρόνου



    # 4 Συνάρτηση: Διαγραφή
        # Επιλογή δραστηριότητας προς διαγραφή 
        # Αν υπάρχει:
            # Διαγραφή και επανυπολογισμός του συνολικού ελεύθερου χρόνου.


    # 5 Συνάρτηση: Έξοδος
        # Αν επιλογή  = 4 τότε: Έξοδος.

# Έξοδος

Το κανω exe:
pyinstaller main.py --onefile -w(για να μην εχει το terminal οταν εχω gui)
"""

# Αρχικοποιήσεις
weekly_hours = 168
total_hours = 0 

# Λίστες απο dictionaries για κάθε τύπο δραστηριότητας.
activities = []
ypoxrewseis = []
hobby = []




# Μενού:
def display_menu():
    print("\n","-" * 10 , "Time Management" , "-" * 10 , "\n")
    print("1. Εισαγωγή νέας δραστηριότητας")
    print("2. Εμφάνιση όλων των δραστηριοτήτων")
    print("3. Τροποποίηση δραστηριοτήτων")
    print("4. Διαγραφη δραστηριότητας")
    print("5. Έξοδος")

# Eπιλογή λειτουργίας
def epilogi():
    while True:
        try:
            epilogi = input("Επέλεξε μια απο τις παραπάνω λειτουργείες: ").strip()
            epilogi = int(epilogi)
            if 1<= epilogi <= 5:
                return epilogi
                break
            else:
                print ("Mή έγκυρη τιμή.")
        except ValueError:
            print ("Mή έγκυρη τιμή.")

# Προσθήκη δραστηριότητας
def add_activity(total_hours , activities):
    
    while True:
        
    # Eπιλογή τύπου δραστηριότητας, 1 για Υποχρέωση ή 2 για Χόμπι.
        while True:
            try:
                choice = int(input(("Πληκτρολογείστε 1 για Υποχρέωση ή 2 για Χόμπι: ")))
                if choice in [1,2]:
                    break
                print("Η επιλογή δεν υπάρχει. Παρακαλώ προσπαθήστε ξανά.")
            except ValueError:
                print("Μη έγκυρη είσοδος.")
        
            

    # Εισαγωγή ονόματος, αφαιρώ τα κενά space πρίν και μετά το όνομα. 
        onoma = input("Δώστε το όνομα της δραστηριότητας: ").strip()
            
        """"
        Έλεγχος ονόματος, αν δωθεί το κενό τότε το διαγράφω με την strip επομένως onoma = False και μπαίνω στην επανάληψη
        ή αν κανένα απο τα στοιχεία του ονόματος δεν είναι χαρακτήρας.
        """
        while not onoma or not any(char.isalpha() for char in onoma):
            onoma = input("Το όνομα της δραστηριότητας δεν μπορεί να είναι κενό ή αριθμός, παρακαλώ επανεισάγετε το όνομα: ").strip()
            
     
    #Εισαγωγή διάρκειας δραστηριότητας

        # αν οι συνολικές διαθέσιμες ώρες είναι 0 , εισαγωγή των ωρών πρώτα
        if total_hours == 0:
            while True:
                try:
                    total_hours = input("Παρακαλώ εισάγετε τις συνολικές ώρες που έχετε διαθέσιμες για αυτήν την εβδομάδα: ").strip()
                    total_hours = float(total_hours)
                    if total_hours and 0 <= total_hours <= 168:
                        break
                    else:
                        print("Οι συνολικές διαθέσιμές ώρες δεν μπορούν να είναι αρνητικός αριθμός ή περισσότερες από τις 168 ώρες της εβδομάδας.")
                except ValueError:
                    print ("Μή έγκυρη είσοδος. Παρακαλώ εισάγετε τον αριθμό των διαθέσιμων ωρών.")

        # Εισαγωγή διάρκειας με έλεγχο ορθότητας (Δεν μπορεί να υπερβαίνει τον συνολικό ελεύθερο χρόνο, τις 168 ώρες της εβδομάδας και να είναι αρνητική ή χαρακτήρας).
        while True:
            try:
                diarkeia = input ("Δώστε την διάρκεια της δραστηριότητας σε ώρες: ").strip()
                diarkeia = float(diarkeia)
                if diarkeia and 0 < diarkeia <= total_hours and diarkeia + total_hours <= weekly_hours:
                    total_hours -= diarkeia
                    break
                else:
                    print(f"Η διάρκεια πρέπει να είναι θετικός αριθμός και δεν μπορεί να ξεπερνάει τις {total_hours} διαθέσιμες ώρες ή τις 168 ώρες της εβδομάδας.")
            except ValueError:
                print("Μή έγκυρη είσοδος, παρακαλώ εισάγετε έναν αριθμό ωρών.")

    # Eισαγωγή σημαντικότητας
        while True:
            try:    
                grade = input("Δώστε τον βαθμό σημαντικότητας (1-10): ").strip()
                grade = int(grade)
                if grade and 1 <= grade <= 10:
                    break
                else:
                    print("Παρακαλώ δώστε έναν βαθμό απο το 1 εώς το 10.")
            except ValueError:
                print("Μή έγκυρη τιμή.")
        
    # Εισαγωγή του στοιχείου στην λίστα με τα dictionaries
        # Αποθήκευση ως dictionary με όνομα activity
        activity = {
            "Δραστηριότητα" : onoma,
            "Διάρκεια" : diarkeia,
            "Σημαντικότητα" : grade
        }

        # Προσθήκη του dictionary στην λίστα 
        activities.append(activity)
        
        return total_hours         

# Εμφάνιση όλων των αποθηκευμένων δραστηριοτήτων
def display_activities(activities):
    if not activities:
        print("\nΔεν βρέθηκαν δραστηριότητες.\n")
    else:
        print("\nΟι δραστηριότητες που έχετε να κάνετε αυτή την εβδομάδα είναι: \n")
        for drastiriotita in activities:
            print (f"{drastiriotita['Δραστηριότητα']} : Διάρκεια: {drastiriotita['Διάρκεια']} ώρες | Βαθμός σημαντικότητας: {drastiriotita['Σημαντικότητα']}")

# Τροποποίηση
def modify(activities):
    
    if not activities:
        print ("Δεν υπάρχουν δραστηριότητες για τροποποίηση.")
        return
    
    # Εμφάνιση και επιλογή διαθέσιμων δραστηριοτήτων
    print ("\nΕπιλέξτε μία απο τις διαθέσιμες δραστηριότητες για τροποποίηση: \n")
    for activity in activities:
        print (f"{activity['Δραστηριότητα']}")
    
    # Έξωτερικός βρόγχος 
    while True:
        
        # Επιλογή του χρήστη 
        choice = input().strip()

        # Αν η επιλογή είναι έγκυρη  
        if any(activity["Δραστηριότητα"] == choice for activity in activities):
            
            print("\nΔυνατότητες τροποποίησης: \n")
            print("1. Τροποποίηση ονόματος δραστηριότητας")
            print("2. Τροποποίηση διάρκειας δραστηριότητας")
            print("3. Τροποποίηση βαθμού σημαντικότητας δραστηριότητας")
            print("4. Ακύρωση\n")
            
            # Έλεγχος εγκυρότητας επιλογής
            while True:
                dynatotita = epilogi()
                if 1 <= dynatotita <=4:
                    break
                else:
                    print("Παρακαλώ επιλέξτε μια απο τις διαθέσιμες ενέργειες.")
            



            break    
        # Αν η επιλογή δεν είναι έγκυρη      
        else:
            print ("\nH δραστηριότητα που επιλέξατε δεν υπάρχει, παρακαλώ επιλέξτε μια από τις παρακάτω: \n")
            for activity in activities:
                print (f"{activity['Δραστηριότητα']}")
        


            








    


# Κυρίως πρόγραμμα
def main():
    global total_hours

    while True:

        display_menu()
        leitourgia = epilogi()
        if leitourgia == 1:
            total_hours = add_activity(total_hours , activities)
        elif leitourgia == 2:
            display_activities(activities)
        elif leitourgia == 3:
            modify(activities)
        elif leitourgia == 4:
            pass
        else:
            print("\nΈξοδος απο το πρόγραμμα.\n")
            break

main()