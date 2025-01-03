def basic_calculator(history):
    try:
        num1 = float(input("Enter the first number: "))
        operator = input("Enter the operator (+, -, *, /): ")
        num2 = float(input("Enter the second number: "))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: Division by zero!")
                return
            result = num1 / num2
        else:
            print("Invalid operator!")
            return

        operation = f"{num1} {operator} {num2} = {result}"
        print(operation)
        history.append(operation)
    except ValueError:
        print("Invalid input! Please enter numbers.")

def unit_converter(history):
    print("Select category:")
    print("1. Length")
    print("2. Weight")
    print("3. Temperature")
    category = input("Enter your choice: ")

    try:
        value = float(input("Enter the value: "))

        if category == '1':  # Length
            print("1. Meters to Feet")
            print("2. Feet to Meters")
            print("3. Kilometers to Miles")
            print("4. Miles to Kilometers")
            choice = input("Enter your choice: ")
            if choice == '1':
                result = value * 3.28084
                conversion = f"{value} meters = {result} feet"
            elif choice == '2':
                result = value / 3.28084
                conversion = f"{value} feet = {result} meters"
            elif choice == '3':
                result = value * 0.621371
                conversion = f"{value} kilometers = {result} miles"
            elif choice == '4':
                result = value / 0.621371
                conversion = f"{value} miles = {result} kilometers"
            else:
                print("Invalid choice!")
                return

        elif category == '2':  # Weight
            print("1. Kilograms to Pounds")
            print("2. Pounds to Kilograms")
            print("3. Grams to Ounces")
            print("4. Ounces to Grams")
            choice = input("Enter your choice: ")
            if choice == '1':
                result = value * 2.20462
                conversion = f"{value} kilograms = {result} pounds"
            elif choice == '2':
                result = value / 2.20462
                conversion = f"{value} pounds = {result} kilograms"
            elif choice == '3':
                result = value * 0.035274
                conversion = f"{value} grams = {result} ounces"
            elif choice == '4':
                result = value / 0.035274
                conversion = f"{value} ounces = {result} grams"
            else:
                print("Invalid choice!")
                return

        elif category == '3':  # Temperature
            print("1. Celsius to Fahrenheit")
            print("2. Fahrenheit to Celsius")
            print("3. Celsius to Kelvin")
            choice = input("Enter your choice: ")
            if choice == '1':
                result = (value * 9/5) + 32
                conversion = f"{value}°C = {result}°F"
            elif choice == '2':
                result = (value - 32) * 5/9
                conversion = f"{value}°F = {result}°C"
            elif choice == '3':
                result = value + 273.15
                conversion = f"{value}°C = {result} K"
            else:
                print("Invalid choice!")
                return

        else:
            print("Invalid category!")
            return

        print(conversion)
        history.append(conversion)
    except ValueError:
        print("Invalid input! Please enter a number.")

def view_history(history):
    if not history:
        print("History is empty.")
    else:
        print("\nHistory:")
        for entry in history:
            print(entry)

def main():
    history = []
    while True:
        print("\nMenu:")
        print("1. Basic Calculator")
        print("2. Unit Converter")
        print("3. View History")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            basic_calculator(history)
        elif choice == '2':
            unit_converter(history)
        elif choice == '3':
            view_history(history)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()