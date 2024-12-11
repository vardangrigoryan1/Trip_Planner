import csv

accounts_file = "accounts.csv"
feedback_file = "feedback.csv"
places_file = "places.csv"

#loading accounts from the "accounts.csv" file
def load_accounts():
    accounts = {} #an empty dictionary to store accounts
    with open(accounts_file, "r") as csv_file: #opening the "accounts.csv" file in read mode ("r")
        reader = csv.DictReader(csv_file) #reading the csv as a dictionary
        for row in reader:
            username = row["username"] #getting the username
            password = row["password"] #getting the password
            accounts[username] = password #storing the username-password pair in the dictionary
    return accounts

#saving accounts to the "accounts.csv" file
def save_accounts(accounts):
    with open(accounts_file, "w", newline="") as csv_file: #opening the "accounts.csv" file in write mode ("w") with a newline="" for proper csv formatting
        writer = csv.writer(csv_file) #to write data to the csv file
        writer.writerow(["username", "password"]) #writing the header row with column names "username" and "password"
        for username, password in accounts.items(): #writing each account as a row
            writer.writerow([username, password]) #writing each username and password as a new row in the "accounts.csv" file

#checking if the password is strong overall
def is_strong_password(password):
    if len(password) < 6: #checking if the password length is less than 6 characters
        return "Password must be at least 6 characters long."
    if not any(char.islower() for char in password): #checking if the password contains at least one lowercase letter
        return "Password must contain at least one lowercase letter."
    if not any(char.isupper() for char in password): #checking if the password contains at least one uppercase letter
        return "Password must contain at least one uppercase letter."
    if not any(char.isdigit() for char in password): #checking if the password contains at least one digit
        return "Password must contain at least one digit."
    return None  #password is strong

#check if the username already exists
def is_duplicate_username(accounts, username):
    return username in accounts

#loading feedback from the "feedback.csv" file
def load_feedback():
    feedback = [] #an empty list to store feedback (feedback list)
    with open(feedback_file, "r") as csv_file: #opening the "feedback.csv" file in read mode ("r")
        reader = csv.DictReader(csv_file) #reading the csv as a dictionary
        for row in reader:
            country = row["country"] #getting the country
            user_feedback = row["user_feedback"] #getting the user_feedback
            feedback.append((country, user_feedback)) #storing/adding the tuple to the feedback list
    return feedback

#saving feedback to the feedback.csv" file
def save_feedback(feedback):
    with open(feedback_file, "w", newline="") as file: #opening the "user_feedback" file in write mode ("w") with a newline="" for proper csv formatting
        writer = csv.writer(file) #to write data to the csv file
        writer.writerow(["country", "user_feedback"]) #writing the header row with column names "country" and "user_feedback"
        for country, user_feedback in feedback: #writing each feedback as a row
            writer.writerow([country, user_feedback]) #writing each country and user_feedback as a new row in the "user_feedback" file

#loading places from the "places.csv" file
def load_places():
    places = [] #an empty list to store places (places list)
    with open(places_file, "r") as csv_file: #opening the "places.csv" file in read mode ("r")
        reader = csv.DictReader(csv_file) #reading the csv as a dictionary
        for row in reader:
            country = row["Country"] #getting the Country
            city = row["City"] #getting the City
            place_to_visit = row["Place"] #getting the Place
            places.append((country, city, place_to_visit)) #storing/adding the tuple to the places list
    return places

#function to check if a place exists for the given country
def is_there_place(country, places):
    results = list(map(lambda place: place if place[0].lower() == country.lower() else None, places)) #using map() to search for the country in places
    results = [place for place in results if place is not None] #filtering out None values
    if results: #if there are any matching results
        for place in results:
            print("City: " + place[1] +", Place to visit: " + place[2]) #print the city and place to visit
        return True #return True if places were found for the country
    return False #return False if no places were found for the country

#function to check if the country exists for the given country (similar to def is_there_place)
def is_there_country(country, places):
    results = list(map(lambda place: place if place[0].lower() == country.lower() else None, places))
    results = [place for place in results if place is not None]
    if results:
        return True
    return False

#account/profile menu function
def profile_menu(username, feedback, places):
    while True:
        print("\nWelcome, " + username + "!")
        print("1. Write Feedback About a Country")
        print("2. View my Feedback")
        print("3. Search Feedback by Country")
        print("4. Search Places to Visit by Country")
        print("5. Log Out")

        choice = input("Enter your choice: ")

        #write feedback about a country
        if choice == "1":
                while True:
                    country = input("Enter the name of the country (or type 'exit' to quit): ")

                    if country.lower() == "exit": #if user types 'exit'
                        print("Exiting...")
                        break #exit the feedback loop

                    if is_there_country(country, places): #checking if the country exists in the list
                        user_feedback = input("Enter your feedback: ")
                        feedback.append((country, username + ": " + user_feedback)) #storing/adding the feedback to the feedback list
                        save_feedback(feedback) #saving the feedback in the "feedback.csv" file
                        print("Feedback saved successfully!")
                        break #exit the loop after saving feedback
                    else: #if the country does not exist in the list
                        print("No such country: " + country + ". Please enter a valid country.")

        #view my feedback
        elif choice == "2":
            print("\nFeedback by",username)
            found_feedback = False #flag to check if feedback exists
            for country, user_feedback in reversed(feedback): #the feedback list is iterated in reverse order, in order to get the most recent feedback first
                if user_feedback.startswith(username + ":"): #checking if the feedback belongs to the user
                    found_feedback = True #feedback exists
                    print("- " + country + ": " + user_feedback.split(": ", 1)[1]) #print the feedback without the username (because we know that the username is ours)

                    option = input("Would you like to delete this feedback? (Y/N): ")
                    if option.lower() == "y": #if user chooses to delete
                        feedback.remove((country, user_feedback)) #remove the feedback from the list
                        save_feedback(feedback) #saving the updated feedback back to the "feedback.csv" file
                        print("Feedback for",country,"is deleted.") #confirmation of deleting
                    elif option.lower() == "n": #if user chooses not to delete
                        print("Feedback about",country,"is not deleted.") #feedback not deleted
                        
            if not found_feedback: #if no feedback found
                print("No feedback found.")

        #search feedback by country
        elif choice == "3":
            country = input("Enter the name of the country: ")
            search_feedback(feedback, country) #recall the search_feedback function with the given country and display the respective feedback about the entered country (or a proper message if there is no feedback for the country)
        
        #search places to visit by country
        elif choice == "4":
            while True:
                country = input("Please enter the country that you want: ")
                if is_there_place(country, places) or country == "exit": #if the user wants to exit this section
                    break
                else:
                    print("We don't have that country. Try again, or type 'exit' to exit")

        #Log Out        
        elif choice == "5":
            print("Logging out...")
            break #exit the profile menu loop
        else:
            print("Invalid choice. Please try again.")

#function for search feedback by country (fixed csv file - "places.csv")
def search_feedback(feedback, country):
    print("\nFeedback about " + country + ":")
    found = False #flag to track if any feedback is found
    for fb_country, user_feedback in feedback:
        if fb_country.lower() == country.lower(): #checking if the country matches
            print("- " + user_feedback)
            found = True #flag to True if feedback is found
    if not found:
        print("No feedback found for this country.") #in this case if there is no feedback about the entered country

#main menu function
def main_menu():
    accounts = load_accounts() #loading the "accounts.csv" file
    feedback = load_feedback() #loading the "feedback.csv" file
    places = load_places() #loading the "places.csv" file

    while True:
        print("\nMain Menu:")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Enter your choice: ")

        #sign up
        if choice == "1":
            username = input("Enter a username, or type 'exit' to exit: ")
            if username.lower() == "exit":
                print("Exiting...")
                continue #exit the username input loop if the user types 'exit'
            if is_duplicate_username(accounts, username):
                print("Username already exists. Please try again.")
                continue #re-ask the user to enter a username if it is a duplicate
            print("Password must contain 6 characters, at least one lowercase, uppercase and digit.")
            
            #limit the password attempts to 3
            for attempt_count in range(3):
                password = input("Enter a password, or type 'exit' to exit: ")
                if password.lower() == "exit":
                    print("Exiting...")
                    break #exit the password input loop if the user types 'exit'
                
                password_feedback = is_strong_password(password)
                if password_feedback:
                    print(password_feedback) #show the issue and prompt again
                else:
                    break #password is strong, proceed
            
            else: #this else is executed only if the loop did NOT break (too many failed attempts)
                print("Too many failed attempts. Returning to the main menu.")
                continue #exit to the main menu if 3 attempts are exceeded

            if password.lower() == "exit":
                continue #skip account creation if user chose to exit

            #saving the new account in the "accounts.csv" file
            accounts[username] = password #adding the new username and password to the accounts dictionary
            save_accounts(accounts) #recall the def save_accounts to save the updated accounts to the "accounts.csv" file
            print("Account created successfully!")

        #log in
        elif choice == "2":
            #limit the username attempts to 3
            for attempt_count in range(3):
                username = input("Enter your username, or type 'exit' to exit: ")
                if username.lower() == "exit":
                    print("Exiting...")
                    break #exit the username input loop if the user types 'exit'
                password = input("Enter your password, or type 'exit' to exit: ")
                if password.lower() == "exit":
                    print("Exiting...")
                    break #exit the password input loop if the user types 'exit'
                if accounts.get(username) == password: #checking if the username and password match
                    profile_menu(username, feedback, places) #go to profile menu if valid login
                    break #exiting the loop after successful login
                else:
                    print("Invalid username or password. Please try again.")

            else: #this else is executed only if the loop did NOT break (too many failed attempts)
                print("Too many failed attempts. Returning to the main menu.")
                continue #exit to the main menu if 3 attempts are exceeded
        
        #exit
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

#call the main menu function to start the program
main_menu()

#©Vardan Grigoryan