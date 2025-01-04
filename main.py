import math
import numpy as np
from sympy import symbols, solve, diff, integrate, simplify
from scipy import stats

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

# 1. Add missing current_theme initialization at the top
current_theme = THEME_LIGHT

def basic_calculator(history, num1, operation, num2):
    """Perform basic calculations."""
    try:
        # Validate inputs
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise ValueError("Numbers must be numeric values!")
        
        if operation not in ['+', '-', '*', '/', '^', '%', '//', '√', 'log', 'ln']:
            raise ValueError("Invalid operation!")

        # Perform calculation based on operation
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ValueError("Error: Division by zero!")
            result = num1 / num2
        elif operation == '^':
            result = num1 ** num2
        elif operation == '%':
            if num2 == 0:
                raise ValueError("Error: Modulo by zero!")
            result = num1 % num2
        elif operation == '//':
            if num2 == 0:
                raise ValueError("Error: Division by zero!")
            result = num1 // num2
        elif operation == '√':
            # num1 is the number, num2 is the root
            if num2 == 0:
                raise ValueError("Error: Root cannot be zero!")
            if num1 < 0 and num2 % 2 == 0:
                raise ValueError("Error: Even root of negative number!")
            result = num1 ** (1/num2)
        elif operation == 'log':
            if num1 <= 0 or num2 <= 0:
                raise ValueError("Error: Logarithm inputs must be positive!")
            if num2 == 1:
                raise ValueError("Error: Log base cannot be 1!")
            result = math.log(num1, num2)  # num2 is the base
        elif operation == 'ln':
            if num1 <= 0:
                raise ValueError("Error: Natural log input must be positive!")
            result = math.log(num1)  # num2 is ignored for natural log
        else:
            raise ValueError("Invalid operation!")

        # Format the operation string based on the operator
        if operation == 'log':
            operation_str = f"log base {num2} of {num1} = {result}"
        elif operation == 'ln':
            operation_str = f"ln({num1}) = {result}"
        elif operation == '√':
            operation_str = f"{num2}√{num1} = {result}"
        else:
            operation_str = f"{num1} {operation} {num2} = {result}"

        # Add to history
        history.append(operation_str)
        
        return result
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def unit_converter(history, category, value, choice):
    """Convert between various units."""
    try:
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be numeric!")
        
        # Create conversion mappings
        conversions = {
            'Length': {
                'Meters to Feet': (METERS_TO_FEET, "meters", "feet"),
                'Feet to Meters': (FEET_TO_METERS, "feet", "meters"),
                'Kilometers to Miles': (KILOMETERS_TO_MILES, "kilometers", "miles"),
                'Miles to Kilometers': (MILES_TO_KILOMETERS, "miles", "kilometers")
            },
            'Weight': {
                'Kilograms to Pounds': (KILOGRAMS_TO_POUNDS, "kilograms", "pounds"),
                'Pounds to Kilograms': (POUNDS_TO_KILOGRAMS, "pounds", "kilograms"),
                'Grams to Ounces': (GRAMS_TO_OUNCES, "grams", "ounces"),
                'Ounces to Grams': (OUNCES_TO_GRAMS, "ounces", "grams")
            },
            'Temperature': {
                'Celsius to Fahrenheit': lambda x: (x * 9/5) + 32,
                'Fahrenheit to Celsius': lambda x: (x - 32) * 5/9,
                'Celsius to Kelvin': lambda x: x + 273.15
            },
            'Volume': {
                'Liters to Gallons': (LITERS_TO_GALLONS, "liters", "gallons"),
                'Gallons to Liters': (GALLONS_TO_LITERS, "gallons", "liters"),
                'Milliliters to Ounces': (ML_TO_OUNCES, "milliliters", "ounces"),
                'Ounces to Milliliters': (OUNCES_TO_ML, "ounces", "milliliters")
            },
            'Speed': {
                'km/h to mph': (KMH_TO_MPH, "km/h", "mph"),
                'mph to km/h': (MPH_TO_KMH, "mph", "km/h"),
                'm/s to km/h': (MS_TO_KMH, "m/s", "km/h"),
                'km/h to m/s': (KMH_TO_MS, "km/h", "m/s")
            }
        }

        if category not in conversions:
            raise ValueError(f"Invalid category: {category}")
        
        if choice not in conversions[category]:
            raise ValueError(f"Invalid conversion choice: {choice}")

        # Handle temperature separately due to different formulas
        if category == 'Temperature':
            result = conversions[category][choice](value)
            unit_from, unit_to = choice.split(" to ")
            conversion = f"{value}°{unit_from[0]} = {result:.4f}°{unit_to[0]}"
        else:
            conversion_factor, unit_from, unit_to = conversions[category][choice]
            result = value * conversion_factor
            conversion = f"{value} {unit_from} = {result:.4f} {unit_to}"

        history.append(conversion)
        return conversion
    except ValueError as e:
        raise ValueError(str(e))

def currency_converter(history, amount, from_currency, to_currency):
    """Convert between supported currencies."""
    try:
        # Validate amount and currencies
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a positive number!")
        
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
            
        if from_currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {from_currency}")
        if to_currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {to_currency}")

        result = amount * (EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency])
        conversion_str = f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}"
        history.append(conversion_str)
        return conversion_str
    except ValueError as e:
        raise ValueError(str(e))

def view_history(history):
    """Display the calculation and conversion history."""
    if not history:
        return "History is empty."
    return "\n".join(history)

def clear_history(history):
    """Clear the history."""
    history.clear()
    return "History cleared."

def export_history(history):
    """Export the history to a file."""
    try:
        with open("history.txt", "w") as file:
            for entry in history:
                file.write(entry + "\n")
        return "History exported to 'history.txt'."
    except IOError:
        raise ValueError("Error writing to file!")

def change_theme():
    """Change the theme between light and dark."""
    global current_theme
    if current_theme == THEME_LIGHT:
        current_theme = THEME_DARK
    else:
        current_theme = THEME_LIGHT
    return f"{'Dark' if current_theme == THEME_DARK else 'Light'} theme applied."

def show_help():
    """Display the help menu."""
    return (
        "Help Menu:\n"
        "1. Basic Calculator: Perform arithmetic and scientific operations.\n"
        "2. Unit Converter: Convert between various units (length, weight, etc.).\n"
        "3. Currency Converter: Convert between supported currencies.\n"
        "4. View History: See all calculations and conversions performed.\n"
        "5. Change Theme: Switch between light and dark themes.\n"
        "6. Clear History: Clear the calculation and conversion history.\n"
        "7. Export History: Save the history to a file.\n"
        "8. Exit: Close the program."
    )

def confirm_exit():
    """Confirm before exiting the program."""
    try:
        return True  # In a real implementation, you might want to add user input here
    except:
        return False

def scientific_calculation(expr_str):
    """Perform scientific calculations."""
    try:
        x = symbols('x')
        expr = sympify(expr_str)
        
        derivative = diff(expr, x)
        integral = integrate(expr, x)
        simplified = simplify(expr)
        
        return {
            'derivative': str(derivative),
            'integral': str(integral),
            'simplified': str(simplified)
        }
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def statistical_analysis(numbers):
    """Perform statistical analysis."""
    try:
        arr = np.array(numbers)
        return {
            'mean': np.mean(arr),
            'median': np.median(arr),
            'std': np.std(arr),
            'var': np.var(arr),
            'min': np.min(arr),
            'max': np.max(arr)
        }
    except Exception as e:
        raise ValueError(f"Invalid data: {str(e)}")

def matrix_operations(matrix_a, matrix_b):
    """Perform matrix operations."""
    try:
        return {
            'addition': matrix_a + matrix_b,
            'multiplication': matrix_a @ matrix_b,
            'det_a': np.linalg.det(matrix_a),
            'inverse_a': np.linalg.inv(matrix_a)
        }
    except Exception as e:
        raise ValueError(f"Invalid matrices: {str(e)}")