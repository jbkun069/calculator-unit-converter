import math

# Theme colors (ANSI escape codes)
THEME_LIGHT = {
    "text": "\033[97m",  # White text
    "background": "\033[40m",  # Black background
    "highlight": "\033[94m",  # Blue highlight
    "reset": "\033[0m",  # Reset to default
}

THEME_DARK = {
    "text": "\033[30m",  # Black text
    "background": "\033[107m",  # White background
    "highlight": "\033[92m",  # Green highlight
    "reset": "\033[0m",  # Reset to default
}

current_theme = THEME_LIGHT  # Default theme

# Constants for conversions
METERS_TO_FEET = 3.28084
FEET_TO_METERS = 1 / METERS_TO_FEET
KILOMETERS_TO_MILES = 0.621371
MILES_TO_KILOMETERS = 1 / KILOMETERS_TO_MILES
KILOGRAMS_TO_POUNDS = 2.20462
POUNDS_TO_KILOGRAMS = 1 / KILOGRAMS_TO_POUNDS
GRAMS_TO_OUNCES = 0.035274
OUNCES_TO_GRAMS = 1 / GRAMS_TO_OUNCES
LITERS_TO_GALLONS = 0.264172
GALLONS_TO_LITERS = 1 / LITERS_TO_GALLONS
ML_TO_OUNCES = 0.033814
OUNCES_TO_ML = 1 / ML_TO_OUNCES
KMH_TO_MPH = 0.621371
MPH_TO_KMH = 1 / KMH_TO_MPH
MS_TO_KMH = 3.6
KMH_TO_MS = 1 / MS_TO_KMH

# Exchange rates (fixed for demonstration)
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.85,
    'INR': 82.0,
    'GBP': 0.73,
}

def apply_theme(text, highlight=False):
    """Apply the current theme to the text."""
    if highlight:
        return f"{current_theme['highlight']}{text}{current_theme['reset']}"
    return f"{current_theme['text']}{current_theme['background']}{text}{current_theme['reset']}"

def get_float_input(prompt):
    """Get a valid float input from the user."""
    while True:
        try:
            return float(input(apply_theme(prompt)))
        except ValueError:
            print(apply_theme("Invalid input! Please enter a number.", highlight=True))

def show_help():
    """Display the help menu."""
    print(apply_theme("\nHelp Menu:", highlight=True))
    print(apply_theme("1. Basic Calculator: Perform arithmetic and scientific operations."))
    print(apply_theme("2. Unit Converter: Convert between various units (length, weight, etc.)."))
    print(apply_theme("3. Currency Converter: Convert between supported currencies."))
    print(apply_theme("4. View History: See all calculations and conversions performed."))
    print(apply_theme("5. Change Theme: Switch between light and dark themes."))
    print(apply_theme("6. Clear History: Clear the calculation and conversion history."))
    print(apply_theme("7. Export History: Save the history to a file."))
    print(apply_theme("8. Exit: Close the program."))

def basic_calculator(history):
    """Perform basic and scientific calculations."""
    print(apply_theme("\nScientific Calculator Operations:", highlight=True))
    print(apply_theme("+ : Addition"))
    print(apply_theme("- : Subtraction"))
    print(apply_theme("* : Multiplication"))
    print(apply_theme("/ : Division"))
    print(apply_theme("^ : Exponentiation"))
    print(apply_theme("sqrt : Square Root"))
    print(apply_theme("log : Logarithm (base 10)"))
    print(apply_theme("ln : Natural Logarithm (base e)"))
    print(apply_theme("sin : Sine (in radians)"))
    print(apply_theme("cos : Cosine (in radians)"))
    print(apply_theme("tan : Tangent (in radians)"))
    print(apply_theme("pi : π (pi)"))
    print(apply_theme("e : Euler's number"))

    operation = input(apply_theme("Enter the operation: ")).strip().lower()

    if operation in ['+', '-', '*', '/', '^']:
        num1 = get_float_input("Enter the first number: ")
        num2 = get_float_input("Enter the second number: ")

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                print(apply_theme("Error: Division by zero!", highlight=True))
                return
            result = num1 / num2
        elif operation == '^':
            result = num1 ** num2

        operation_str = f"{num1} {operation} {num2} = {result}"
        print(apply_theme(operation_str))
        history.append(operation_str)

    elif operation in ['sqrt', 'log', 'ln', 'sin', 'cos', 'tan']:
        num = get_float_input("Enter the number: ")

        if operation == 'sqrt':
            if num < 0:
                print(apply_theme("Error: Cannot calculate square root of a negative number!", highlight=True))
                return
            result = math.sqrt(num)
        elif operation == 'log':
            if num <= 0:
                print(apply_theme("Error: Logarithm is undefined for non-positive numbers!", highlight=True))
                return
            result = math.log10(num)
        elif operation == 'ln':
            if num <= 0:
                print(apply_theme("Error: Natural logarithm is undefined for non-positive numbers!", highlight=True))
                return
            result = math.log(num)
        elif operation == 'sin':
            result = math.sin(num)
        elif operation == 'cos':
            result = math.cos(num)
        elif operation == 'tan':
            result = math.tan(num)

        operation_str = f"{operation}({num}) = {result}"
        print(apply_theme(operation_str))
        history.append(operation_str)

    elif operation == 'pi':
        result = math.pi
        operation_str = f"π = {result}"
        print(apply_theme(operation_str))
        history.append(operation_str)

    elif operation == 'e':
        result = math.e
        operation_str = f"e = {result}"
        print(apply_theme(operation_str))
        history.append(operation_str)

    else:
        print(apply_theme("Invalid operation!", highlight=True))

def unit_converter(history):
    """Convert between various units."""
    print(apply_theme("\nUnit Converter Categories:", highlight=True))
    print(apply_theme("1. Length"))
    print(apply_theme("2. Weight"))
    print(apply_theme("3. Temperature"))
    print(apply_theme("4. Time"))
    print(apply_theme("5. Volume"))
    print(apply_theme("6. Data Storage"))
    print(apply_theme("7. Speed"))
    category = input(apply_theme("Enter your choice: "))

    value = get_float_input("Enter the value: ")

    if category == '1':  # Length
        print(apply_theme("1. Meters to Feet"))
        print(apply_theme("2. Feet to Meters"))
        print(apply_theme("3. Kilometers to Miles"))
        print(apply_theme("4. Miles to Kilometers"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value * METERS_TO_FEET
            conversion = f"{value} meters = {result} feet"
        elif choice == '2':
            result = value * FEET_TO_METERS
            conversion = f"{value} feet = {result} meters"
        elif choice == '3':
            result = value * KILOMETERS_TO_MILES
            conversion = f"{value} kilometers = {result} miles"
        elif choice == '4':
            result = value * MILES_TO_KILOMETERS
            conversion = f"{value} miles = {result} kilometers"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '2':  # Weight
        print(apply_theme("1. Kilograms to Pounds"))
        print(apply_theme("2. Pounds to Kilograms"))
        print(apply_theme("3. Grams to Ounces"))
        print(apply_theme("4. Ounces to Grams"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value * KILOGRAMS_TO_POUNDS
            conversion = f"{value} kilograms = {result} pounds"
        elif choice == '2':
            result = value * POUNDS_TO_KILOGRAMS
            conversion = f"{value} pounds = {result} kilograms"
        elif choice == '3':
            result = value * GRAMS_TO_OUNCES
            conversion = f"{value} grams = {result} ounces"
        elif choice == '4':
            result = value * OUNCES_TO_GRAMS
            conversion = f"{value} ounces = {result} grams"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '3':  # Temperature
        print(apply_theme("1. Celsius to Fahrenheit"))
        print(apply_theme("2. Fahrenheit to Celsius"))
        print(apply_theme("3. Celsius to Kelvin"))
        choice = input(apply_theme("Enter your choice: "))
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
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '4':  # Time
        print(apply_theme("1. Seconds to Minutes"))
        print(apply_theme("2. Minutes to Seconds"))
        print(apply_theme("3. Hours to Days"))
        print(apply_theme("4. Days to Hours"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value / 60
            conversion = f"{value} seconds = {result} minutes"
        elif choice == '2':
            result = value * 60
            conversion = f"{value} minutes = {result} seconds"
        elif choice == '3':
            result = value / 24
            conversion = f"{value} hours = {result} days"
        elif choice == '4':
            result = value * 24
            conversion = f"{value} days = {result} hours"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '5':  # Volume
        print(apply_theme("1. Liters to Gallons"))
        print(apply_theme("2. Gallons to Liters"))
        print(apply_theme("3. Milliliters to Ounces"))
        print(apply_theme("4. Ounces to Milliliters"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value * LITERS_TO_GALLONS
            conversion = f"{value} liters = {result} gallons"
        elif choice == '2':
            result = value * GALLONS_TO_LITERS
            conversion = f"{value} gallons = {result} liters"
        elif choice == '3':
            result = value * ML_TO_OUNCES
            conversion = f"{value} milliliters = {result} ounces"
        elif choice == '4':
            result = value * OUNCES_TO_ML
            conversion = f"{value} ounces = {result} milliliters"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '6':  # Data Storage
        print(apply_theme("1. Bytes to Kilobytes"))
        print(apply_theme("2. Kilobytes to Bytes"))
        print(apply_theme("3. Megabytes to Gigabytes"))
        print(apply_theme("4. Gigabytes to Megabytes"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value / 1024
            conversion = f"{value} bytes = {result} kilobytes"
        elif choice == '2':
            result = value * 1024
            conversion = f"{value} kilobytes = {result} bytes"
        elif choice == '3':
            result = value / 1024
            conversion = f"{value} megabytes = {result} gigabytes"
        elif choice == '4':
            result = value * 1024
            conversion = f"{value} gigabytes = {result} megabytes"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    elif category == '7':  # Speed
        print(apply_theme("1. km/h to mph"))
        print(apply_theme("2. mph to km/h"))
        print(apply_theme("3. m/s to km/h"))
        print(apply_theme("4. km/h to m/s"))
        choice = input(apply_theme("Enter your choice: "))
        if choice == '1':
            result = value * KMH_TO_MPH
            conversion = f"{value} km/h = {result} mph"
        elif choice == '2':
            result = value * MPH_TO_KMH
            conversion = f"{value} mph = {result} km/h"
        elif choice == '3':
            result = value * MS_TO_KMH
            conversion = f"{value} m/s = {result} km/h"
        elif choice == '4':
            result = value * KMH_TO_MS
            conversion = f"{value} km/h = {result} m/s"
        else:
            print(apply_theme("Invalid choice!", highlight=True))
            return

    else:
        print(apply_theme("Invalid category!", highlight=True))
        return

    print(apply_theme(conversion))
    history.append(conversion)

def currency_converter(history):
    """Convert between supported currencies."""
    print(apply_theme("\nCurrency Converter", highlight=True))
    print(apply_theme("Supported currencies: USD, EUR, INR, GBP"))
    print(apply_theme("Example: Convert 100 USD to INR"))

    amount = get_float_input("Enter the amount: ")
    from_currency = input(apply_theme("Enter the source currency (e.g., USD): ")).strip().upper()
    to_currency = input(apply_theme("Enter the target currency (e.g., INR): ")).strip().upper()

    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        print(apply_theme("Unsupported currency!", highlight=True))
        return

    result = amount * (EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency])
    conversion_str = f"{amount} {from_currency} = {result:.2f} {to_currency}"
    print(apply_theme(conversion_str))
    history.append(conversion_str)

def view_history(history):
    """Display the calculation and conversion history."""
    if not history:
        print(apply_theme("History is empty.", highlight=True))
    else:
        print(apply_theme("\nHistory:", highlight=True))
        for entry in history:
            print(apply_theme(entry))

def clear_history(history):
    """Clear the calculation and conversion history."""
    history.clear()
    print(apply_theme("History cleared.", highlight=True))

def export_history(history):
    """Export the history to a file."""
    with open("history.txt", "w") as file:
        for entry in history:
            file.write(entry + "\n")
    print(apply_theme("History exported to 'history.txt'.", highlight=True))

def change_theme():
    """Change the theme between light and dark."""
    global current_theme
    print(apply_theme("\nSelect Theme:", highlight=True))
    print(apply_theme("1. Light Theme"))
    print(apply_theme("2. Dark Theme"))
    choice = input(apply_theme("Enter your choice: "))

    if choice == '1':
        current_theme = THEME_LIGHT
        print(apply_theme("Light theme applied.", highlight=True))
    elif choice == '2':
        current_theme = THEME_DARK
        print(apply_theme("Dark theme applied.", highlight=True))
    else:
        print(apply_theme("Invalid choice! Theme remains unchanged.", highlight=True))

def confirm_exit():
    """Confirm before exiting the program."""
    choice = input(apply_theme("Are you sure you want to exit? (y/n): ")).strip().lower()
    return choice == 'y'

def main():
    """Main function to run the program."""
    history = []
    print(apply_theme("Welcome to the Ultimate Calculator and Unit Converter!", highlight=True))
    while True:
        print(apply_theme("\nMenu:", highlight=True))
        print(apply_theme("1. Basic Calculator"))
        print(apply_theme("2. Unit Converter"))
        print(apply_theme("3. Currency Converter"))
        print(apply_theme("4. View History"))
        print(apply_theme("5. Change Theme"))
        print(apply_theme("6. Clear History"))
        print(apply_theme("7. Export History"))
        print(apply_theme("8. Help"))
        print(apply_theme("9. Exit"))
        choice = input(apply_theme("Enter your choice: "))

        if choice == '1':
            basic_calculator(history)
        elif choice == '2':
            unit_converter(history)
        elif choice == '3':
            currency_converter(history)
        elif choice == '4':
            view_history(history)
        elif choice == '5':
            change_theme()
        elif choice == '6':
            clear_history(history)
        elif choice == '7':
            export_history(history)
        elif choice == '8':
            show_help()
        elif choice == '9':
            if confirm_exit():
                print(apply_theme("Exiting the program. Goodbye!", highlight=True))
                break
        else:
            print(apply_theme("Invalid choice! Please try again.", highlight=True))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(apply_theme("\nProgram interrupted. Exiting gracefully.", highlight=True))