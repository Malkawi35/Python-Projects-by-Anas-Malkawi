# Displaying a Welcome Message For the Simple Python Calculator.
print("Hey, it's nice seeing you using my simple Python calculator!")

# Functions
def add(number1, number2):
    return number1 + number2

def subtract(number1, number2):
    return number1 - number2

def multiply(number1, number2):
    return number1 * number2

def divide(number1, number2):
    if number2 != 0:
        return number1 / number2
    else:
        return "Division by Zero is not defined!"

def power(number1, number2):
    return number1 ** number2


# The start of the calculator program
def Calculator():
    # Asking the user to enter numbers
    number1 = float(input("Enter the first number: "))
    number2 = float(input("Enter the second number: "))

  # Displaying the operations
    print("Choose an operation: +, -, *, /, ^")
    Chosen_Operation = input("Enter your operation you want to use: ")

  # Performing the operations
    if Chosen_Operation == "+":
        result = add(number1, number2)
    elif Chosen_Operation == "-":
        result = subtract(number1, number2)
    elif Chosen_Operation == "*":
        result = multiply(number1, number2)
    elif Chosen_Operation == "/":
        result = divide(number1, number2)
    elif Chosen_Operation == "^":
        result = power(number1, number2)
    else:
        result = "Invalid Operation"

    # Showing the result of the calculation
    print(f"The result for your equation is: {result}")


Calculator()
