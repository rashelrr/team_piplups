from getpass import getpass
import re

usernames_passwords = {}

def main():
    print("Welcome to our service! This service allows you to leave restaurant reviews for your friends to read!\n")

    loginSignup = input("Type 'Log in' to log into your account or 'Sign up' to create a new account: ").lower()

    while loginSignup != "log in" and loginSignup != "sign up":
        loginSignup = input("Error. Please type 'Log in' to log into your account or 'Sign up' to create a new account: ").lower()

    if loginSignup == "log in":
        login()
    else:
        signup()

def login():
    username = input("Enter your username: ")
    pwd = getpass("Enter your password: ")

    # TO DO: verify that hashtable contains this username-password pair
        # if so, proceed to next step (show instructions)
        # else, throw error: "invalid username or password"

def signup():
    username = input("To create your account, enter a username: ");
    userLen = len(username)

    # check if username is valid
    valid = False
    while valid is False:

        # check valid characters and length
        invalidCharsLen = not checkChars(username) or userLen < 6 or userLen > 30
        if invalidCharsLen is True:
            error = ("Username is not valid. Username should meet the following requirements:\n"
                     "- First character must be a letter\n"
                     " - At least one digit\n"
                     " - Must be between 6 and 30 characters, inclusive\n"
                     " Please try again: ")
            username = input(error)
            userLen = len(username)
    
        # check username doesn't already exist
        userExists = username in usernames_passwords
        if userExists is True:
            username = input("This username is already taken. Please enter another username: ")

        if invalidCharsLen is False and userExists is False:
            valid = True
    
    # TO DO: check if password is valid

    
    print("success!!!")

def checkChars(username):
    ''' Checks the following about username:
        - first char is a letter
        - contains at least one digit
        - contains only letters and digits - done
    '''
    if len(username) == 0:
        return False

    valid_chars = re.match("^[A-Za-z0-9]*$", username)
    number_flag = re.match(".*\\d+.*", username)
    firstChar = username[0] 
    first_letter_flag = re.match("[A-Za-z]", firstChar)

    return valid_chars and number_flag and first_letter_flag; 


if __name__=="__main__":
    main()
