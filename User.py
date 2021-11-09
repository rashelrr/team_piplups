# Food Groups 

def User():
    def __init__(self):
        self.username = ""
        self.current_group = "" 


    def create_group(self):
        group = input("Please enter the name of your group.\nGroup names are limited to alphanumeric characters ([a-z], [A-Z], [0-9]): ")
        valid = False
        while valid is False: 
            while group.isalnum() is False:
                group = input("Invalid characters used, please try again.") #Check if it's database or not.
            if group != "charmander": #replace charmander with the names in database - change this later!
                print("Group successfully created!")
                valid = True
            else:
                group = input("Group name is already in database, try again: ")
            

    #def add_user(self):

    #def enter_group(self, groupname):
        # enter a groups

    #def display_reviews(self):
        # display reviews of all friends in this friend group

    def leave_review(self):
        print("Please follow the instructions provided: ")
        star_review = input("Please rate your review out of five stars - Use integers.")
        if star_review 

    #def help(self):
        # Print all the commands with their descriptions

    #def options(self): 

    '''Not for first iteration'''
    #def leave_group(self):
    #def current_group(self):
    #def display_reviews_for_restaurant():
        # displays reviews for restaurant from all friend groups that user is a part ofd