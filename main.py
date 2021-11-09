from getpass import getpass
import re
#from User import User

usernames_passwords = {}
all_users = {} # key: username, value: User object

def main():
    openingMessage()

def openingMessage():
    print("Welcome to our service! This service allows you to leave restaurant reviews for your friends to read!\n")

    loginSignup = input("Type 'Log in' to log into your account or 'Sign up' to create a new account: ").lower()

    while loginSignup != "log in" and loginSignup != "sign up":
        loginSignup = input("Error. Please type 'Log in' to log into your account or 'Sign up' to create a new account: ").lower()

    if loginSignup == "log in":
        login()
    else:
        signup()

def login():
    ### TODO FOR SECOND ITERATION: usernames+passwords should be in a DATABASE instead of local usernames_passwords
    # so that even when user quits program, their username/password is saved somewhere
    # check connect4?

    username = input("Enter your username: ")
    while True:        
        if username in usernames_passwords:
            break
        else:
            username = input("Username does not exist. Please enter your username: ")

    pwd = getpass("Enter your password: ")
    while True:        
        if len(pwd) != 0 and pwd == usernames_passwords[username]:
            break
        else:
            username = getpass("Invalid password. Please enter your password: ")

    print_instructions()

def print_instructions():
    print(("Below are the commands that you can use to do everything in this "
            "app, such as enter a friend group, add a review, etc."))
    print("~commands here~") 

def signup():
    username = enterUsername()
    pwd = enterPassword()

    usernames_passwords[username] = pwd

    # create a new user, add to all_users
    #new_user = User(username)                   ### TODO: in User class, make User take a parameter! 
    #all_users[username] = new_user

    inp = input("Account has been created. Type 'y' to log into your account, or 'n' to quit: ")
    if inp == 'y':
        login()

def enterUsername():
    ''' Check if username is valid'''
    username = input("To create your account, enter a username: ")
    userLen = len(username)

    while True:
        # check valid characters and length
        invalidCharsLen = userLen < 6 or userLen > 30 or not validCharsUser(username)
        if invalidCharsLen is True:
            error = ("Username is not valid. Username should meet the following requirements:\n"
                     "\t- First character must be a letter\n"
                     "\t- At least one digit\n"
                     "\t- Must be between 6 and 30 characters, inclusive\n"
                     "Please try again: ")
            username = input(error)
            userLen = len(username)
    
        # check username doesn't already exist
        userExists = username in usernames_passwords
        if userExists is True:
            username = input("This username is already taken. Please enter another username: ")

        if invalidCharsLen is False and userExists is False:
            break
    
    return username

def enterPassword():
    ''' Check if password is valid '''
    password = getpass("Enter a password: ")
    pwdLen = len(password)

    while True:
        # check valid characters and length
        invalidCharsLen = pwdLen < 8 or pwdLen > 30 or not validCharsPwd(password)
        if invalidCharsLen is True:
            error = ("Password is not valid. Password should meet the following requirements:\n"
                    "\t- At least one lowercase letter\n"
                    "\t- At least one uppercase letter\n"
                    "\t- At least one digit\n"
                    "\t- At least one special character. Special characters include: ~, @, #, %, &, !, $, ^, *, (, )\n"
                    "\t- Must be between 8 and 16 characters, inclusive\n"
                    "Please try again: ")
            password = getpass(error)
            pwdLen = len(password)

        if invalidCharsLen is False:
            break

    # re-enter password + check passwords match
    reenter_pwd = getpass("Re-enter your password: ")
    while True:
        if password != reenter_pwd:
            reenter_pwd = getpass("Passwords do not match. Please re-enter your password: ")
        else:
            break
    
    return password

def validCharsPwd(password):
    ''' Checks that password meets the credentials below:
        * At least one lowercase letter
        * At least one uppercase letter
        * At least one number
        * At least one special character. Special characters include: ~, @, #, %, &, !, $, ^, *, (, )
    '''
    hasLUD = re.search("(?=.*\d)(?=.*[a-z])(?=.*[A-Z])", password) # has at least one of each: lower, upper, number
    hasSpecial = False

    for ch in password:
        isSpecial = (ch == '~' or ch == '!' or ch == '@' or ch == '#' or ch == '$' or ch == '%' or 
                        ch == '^' or ch == '&' or ch == '*' or ch == '(' or ch == ')' or ch == '~')
        if isSpecial is True:
            hasSpecial = True
        if isSpecial is True or str(ch).isalnum() is True:
            continue
        else:
            return False

    return True if hasLUD is not None and hasSpecial is True else False
    

def validCharsUser(username):
    ''' Checks username meets the following requirements:
        * first char is a letter
        * contains at least one number
        * contains only letters and numbers - done
    '''
    valid_chars = re.match("^[A-Za-z0-9]*$", username)
    number_flag = re.match(".*\\d+.*", username)
    firstChar = username[0] 
    first_letter_flag = re.match("[A-Za-z]", firstChar)

    return valid_chars and number_flag and first_letter_flag


if __name__=="__main__":
    main()
