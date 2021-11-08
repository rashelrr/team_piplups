import java.util.*;
import java.util.Scanner;
import java.io.Console;

public class Driver {
    private static HashMap<String, String> credentials = new HashMap<>();


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);  // Create a Scanner object
        System.out.println("Welcome to our service! This service allows you to " +
        "leave restaurant reviews for your friends to read! \n");

        System.out.println("Type 'Log in' to log into your account or 'Sign up' to create a new account: ");
        String input = scanner.nextLine();
        String loginOrSignup = input.toLowerCase();
    
        while ( !loginOrSignup.equals("log in") && !loginOrSignup.equals("sign up") ) {
            System.out.println("Error. Please enter 'Log in' to log into your account or 'Sign up' to create a new account.");
            input = scanner.nextLine();
            loginOrSignup = input.toLowerCase();
        }

        if (loginOrSignup.equals("log in"))
            logIn(scanner);
        else
            signUp(scanner);

    }

    public static void logIn(Scanner scanner) {
        System.out.print("Enter your username: ");
        String username = scanner.nextLine();

        Console cnsl = System.console();
        if (cnsl == null) {
            System.out.println("No console available");
            scanner.close();
            return;
        }

        char[] password = cnsl.readPassword("Enter your password: ");
        String pwd = String.valueOf(password);
        System.out.println("le password >>> " + pwd);

        // verify that hashtable contains this username-password pair
           // if so, proceed to next step (show instructions)
           // else, throw error: "invalid username or password"

        scanner.close();
    }

    public static void signUp(Scanner scanner) {
        
        System.out.print("To create your account, enter a username: ");
        String username = scanner.nextLine();
        int userLen = username.length();

        // check if username is valid
        boolean valid = false;
        while ( !valid ) {

            boolean invalidCharsLen = !checkChars(username) || (userLen < 6 || userLen > 30);
            if ( invalidCharsLen ) {
                System.out.println("Username is not valid. Username should meet the following requirements:\n" +
                " - First character must be a letter\n - Must contain at least one digit\n - Must be between " +
                "6 and 30 characters, inclusive\n - Contains only letters and digits\nPlease try again: ");
                username = scanner.nextLine();
                userLen = username.length();
            }
    
            boolean userExists = credentials.containsKey(username);
            if ( userExists ) {
                System.out.println("This username is already taken. Please enter another username: ");
                username = scanner.nextLine();
            }

            if ( !invalidCharsLen && !userExists )
                valid = true; 
        }

        System.out.print("Please enter a password: ");
        /*String password = scanner.nextLine();
        userLen = username.length();

        // check if username is valid
        valid = false;
        while ( !valid ) {

            boolean invalidCharsLen = !checkChars(username) || (userLen < 8 || userLen > 30);
            if ( invalidCharsLen ) {
                System.out.println("Username contains invalid characters and/or invalid length. " + 
                "Username should contain letters and at least one digit. Username should be any length " +
                " between 6 and 30 characters, inclusive. Please try again: ");
                username = scanner.nextLine();
                userLen = username.length();
            }
    
            boolean userExists = credentials.containsKey(username);
            if ( userExists ) {
                System.out.println("This username is already taken. Please enter another username: ");
                username = scanner.nextLine();
            }

            if ( !invalidCharsLen && !userExists )
                valid = true; 
        }*/


        scanner.close();
    }

    public static boolean checkChars(String username) {
        /* Checks the following about username:
         * first char is a letter
         * contains at least one digit
         * contains only letters and digits
        */
        if (username.length() == 0)
            return false;

        String firstChar = String.valueOf(username.charAt(0));

        boolean isValidChars = username.matches("[a-zA-Z0-9]*");
        boolean isFirstLetter = firstChar.matches("[A-Za-z]"); 
        boolean containsDigit = username.matches(".*\\d+.*");
        
        return isValidChars && isFirstLetter && containsDigit;       
    }
    
}