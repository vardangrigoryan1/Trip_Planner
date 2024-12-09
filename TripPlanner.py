import csv

accounts_file = "accounts.csv"
feedback_file = "feedback.csv"
places_file = "places.csv"

#load accounts from the CSV file
def load_accounts():
    accounts = {}
    with open(accounts_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            username = row['username']
            password = row['password']
            accounts[username] = password
    return accounts

#save accounts to the CSV file
def save_accounts(accounts):
    with open(accounts_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['username', 'password'])  #write header row
        for username, password in accounts.items():  #write each account as a row
            writer.writerow([username, password])

#check if the password is strong
def is_strong_password(password):
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    return None  #password is strong

#check if the username already exists
def is_duplicate_username(accounts, username):
    return username in accounts

#load feedback from the CSV file
def load_feedback():
    feedback = []
    with open(feedback_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            country = row['country']
            user_feedback = row['user_feedback']
            feedback.append((country, user_feedback))
    return feedback

#save feedback to the file
def save_feedback(feedback):
    with open(feedback_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['country', 'user_feedback'])  #write header row
        for country, user_feedback in feedback:
            writer.writerow([country, user_feedback])  #write each feedback as a row

#load places from the CSV file
def load_places():
    places = []
    with open(places_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            country = row['Country']
            city = row['City']
            place_to_visit = row['Place']
            places.append((country, city, place_to_visit))  #store as a tuple
    return places

#function to check if a place exists for the given country
def is_there_place(country, places):
    #using map to search for the country in places
    results = list(map(lambda place: place if place[0].lower() == country.lower() else None, places))
    results = [place for place in results if place is not None]  #filter out None values
    if results:
        for place in results:
            print("City: " + place[1] +", Place to visit: " + place[2])
        return True
    return False

#profile menu function
def profile_menu(username, feedback, places):
    while True:
        print("\nWelcome, " + username + "!")
        print("1. Write Feedback About a Country")
        print("2. View my feedback")
        print("3. Search feedback by country")
        print("4. Search Places to visit by country")
        print("5. Log Out")

        choice = input("Enter your choice: ")

        if choice == "1":
            country = input("Enter the name of the country: ")
            user_feedback = input("Enter your feedback: ")
            feedback.append((country, username + ": " + user_feedback))
            save_feedback(feedback)
            print("Feedback saved successfully!")

        elif choice == "2":
            print("\nFeedback by",username)
            for country, user_feedback in feedback:
                if user_feedback.startswith(username + ":"):
                    print("- " + country + ": " + user_feedback.split(": ", 1)[1])

                    option = input("Would you like to delete this feedback? (Y/N): ")
                    if option.lower() == "y":
                        feedback.remove((country, user_feedback))
                        print("Feedback for '" + country + "' is deleted.")
                    elif option.lower() == "n":
                        print("Feedback about",country,"is not deleted")

        elif choice == "3":
            country = input("Enter the name of the country: ")
            search_feedback(feedback, country)

        elif choice == "4":
            while True:
                country = input("Please enter the country that you want: ")
                if is_there_place(country, places) or country == "exit":
                    break
                else:
                    print("We don't have that country. Try again, or type 'exit' to exit")
                
        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")

#search feedback by country
def search_feedback(feedback, country):
    print("\nFeedback about " + country + ":")
    found = False
    for fb_country, user_feedback in feedback:
        if fb_country.lower() == country.lower():
            print("- " + user_feedback)
            found = True
    if not found:
        print("No feedback found for this country.")

#main menu function
def main_menu():
    accounts = load_accounts()
    feedback = load_feedback()
    places = load_places()

    while True:
        print("\nMain Menu:")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            #get the username input first (without attempt limit)
            username = input("Enter a username, or type 'exit' to exit: ")
            if username.lower() == "exit":
                print("Exiting...")
                continue  #skip the password input step if the user chose to exit
            if is_duplicate_username(accounts, username):
                print("Username already exists. Please try again.")
                continue  #re-ask the user to enter a username if it's a duplicate
            print("Password must contain 6 characters, at least one lowercase, uppercase and digit.")
            #limit the password attempts to 3 using a for loop
            for attempt_count in range(3):
                password = input("Enter a password, or type 'exit' to exit: ")
                if password.lower() == "exit":
                    print("Exiting...")
                    break  #exit the password input loop if the user types 'exit'
                
                password_feedback = is_strong_password(password)
                if password_feedback:
                    print(password_feedback)  #show the issue and prompt again
                else:
                    break  #password is strong, proceed
            
            else:  #this else block is executed only if the loop did NOT break (too many failed attempts)
                print("Too many failed attempts. Returning to the main menu.")
                continue  #exit to the main menu if 3 attempts are exceeded

            if password.lower() == "exit":
                continue  #skip account creation if user chose to exit

            #save the new account
            accounts[username] = password
            save_accounts(accounts)
            print("Account created successfully!")

        elif choice == "2":
            while True: 
                username = input("Enter your username, or type 'exit' to exit: ")
                if username.lower() == "exit":
                    print("Exiting...")
                    break
                password = input("Enter your password, or type 'exit' to exit: ")
                if password == "exit":
                    print("Exiting...")
                    break
                if accounts.get(username) == password:
                    profile_menu(username, feedback, places)
                    break
                else:
                    print("Invalid username or password. Please try again.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

#call the main menu function to start the program
main_menu()

#©Vardan Grigoryan
