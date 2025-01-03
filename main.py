import math

def basic_calculator(history):
    print("\nScientific Calculator Operations:")
    print("+ : Addition")
    print("- : Subtraction")
    print("* : Multiplication")
    print("/ : Division")
    print("^ : Exponentiation")
    print("sqrt : Square Root")
    print("log : Logarithm (base 10)")
    print("ln : Natural Logarithm (base e)")
    print("sin : Sine (in radians)")
    print("cos : Cosine (in radians)")
    print("tan : Tangent (in radians)")
    print("pi : π (pi)")
    print("e : Euler's number")

    operation = input("Enter the operation: ").strip().lower()

    if operation in ['+', '-', '*', '/', '^']:
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    print("Error: Division by zero!")
                    return
                result = num1 / num2
            elif operation == '^':
                result = num1 ** num2

            operation_str = f"{num1} {operation} {num2} = {result}"
            print(operation_str)
            history.append(operation_str)

        except ValueError:
            print("Invalid input! Please enter numbers.")

    elif operation in ['sqrt', 'log', 'ln', 'sin', 'cos', 'tan']:
        try:
            num = float(input("Enter the number: "))

            if operation == 'sqrt':
                if num < 0:
                    print("Error: Cannot calculate square root of a negative number!")
                    return
                result = math.sqrt(num)
            elif operation == 'log':
                if num <= 0:
                    print("Error: Logarithm is undefined for non-positive numbers!")
                    return
                result = math.log10(num)
            elif operation == 'ln':
                if num <= 0:
                    print("Error: Natural logarithm is undefined for non-positive numbers!")
                    return
                result = math.log(num)
            elif operation == 'sin':
                result = math.sin(num)
            elif operation == 'cos':
                result = math.cos(num)
            elif operation == 'tan':
                result = math.tan(num)

            operation_str = f"{operation}({num}) = {result}"
            print(operation_str)
            history.append(operation_str)

        except ValueError:
            print("Invalid input! Please enter a number.")

    elif operation == 'pi':
        result = math.pi
        operation_str = f"π = {result}"
        print(operation_str)
        history.append(operation_str)

    elif operation == 'e':
        result = math.e
        operation_str = f"e = {result}"
        print(operation_str)
        history.append(operation_str)

    else:
        print("Invalid operation!")

def currency_converter(history):
    print("\nCurrency Converter")
    print("Supported currencies: USD, EUR, INR, GBP")
    print("Example: Convert 100 USD to INR")

    try:
        amount = float(input("Enter the amount: "))
        from_currency = input("Enter the source currency (e.g., USD): ").strip().upper()
        to_currency = input("Enter the target currency (e.g., INR): ").strip().upper()

        # Fixed exchange rates (for demonstration purposes)
        exchange_rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'INR': 82.0,
            'GBP': 0.73,
        }

        if from_currency not in exchange_rates or to_currency not in exchange_rates:
            print("Unsupported currency!")
            return

        result = amount * (exchange_rates[to_currency] / exchange_rates[from_currency])
        conversion_str = f"{amount} {from_currency} = {result:.2f} {to_currency}"
        print(conversion_str)
        history.append(conversion_str)

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
        print("3. Currency Converter")
        print("4. View History")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            basic_calculator(history)
        elif choice == '2':
            unit_converter(history) 
        elif choice == '3':
            currency_converter(history)
        elif choice == '4':
            view_history(history)
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()