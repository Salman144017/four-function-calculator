"""Four Function calculator"""
import sys


def add(number1, number2):
    """Function to perform addition"""
    return number1 + number2


def subtract(number1, number2):
    """Function to perform subtraction"""
    return number1 - number2


def multiply(number1, number2):
    """Function to perform multiplication"""
    return number1 * number2


def divide(number1, number2):
    """Function to perform division"""
    # Check if operation is divide by zero
    if number2 == 0:
        return "Error: divided by 0 not allowed"
    return number1 / number2


def handle_option(option):
    """function to handle selected option"""
    try:
        if option in ["a", "s", "m", "d"]:
            # Get user input for 2 numbers
            input1 = input("Enter first number: ")
            input2 = input("Enter second number: ")
            number1 = float(input1)
            number2 = float(input2)
            if option == "a":
                # Perform addition and display result
                print(f"{input1} + {input2} = ", add(number1, number2))
            elif option == "s":
                # Perform subtraction and display result
                print(f"{input1} - {input2} = ", subtract(number1, number2))
            elif option == "m":
                # Perform multiplication and display result
                print(f"{input1} * {input2} = ", multiply(number1, number2))
            elif option == "d":
                # Perform division and display result
                print(f"{input1} / {input2} = ", divide(number1, number2))
        else:
            # Display error message for invalid option
            print("Invalid option entered")
    except ValueError:
        # Display error message for incorrect format of number
        print("Incorrect format of number")


def main():
    """Function for main flow"""
    while True:
        # Display option menu
        print(
            """Options Menu:
           Enter "a" for addition
           Enter "s" for subtraction
           Enter "m" for multiplication
           Enter "d" for division
           Enter "q" to quit"""
        )
        # Get user input for option
        option = input("Enter option: ")
        if option == "q":
            # If q is selected quit program
            sys.exit()
        else:
            # Call handleOption to perform selected option
            handle_option(option)


# Call main function to start program
if __name__ == "__main__":
    main()
