import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from main import (
    basic_calculator, unit_converter, currency_converter,
    view_history, clear_history, export_history,
    change_theme, show_help, confirm_exit, THEME_LIGHT, THEME_DARK
)
import numpy as np
from sympy import symbols, solve, diff, integrate, simplify
from scipy import stats

# Global variables
history = []
current_theme = THEME_LIGHT

# GUI Application
class CalculatorApp:
    def __init__(self, root):
        # Initialize with ttkbootstrap style
        self.root = root
        self.style = ttk.Style()
        self.style.theme_use("cosmo")  # Start with light theme
        self.root.title("Ultimate Calculator and Unit Converter")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and arrange widgets in the GUI."""
        if not self.root:
            raise RuntimeError("Root window is null")

        # Create main container with padding
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=BOTH, expand=YES)

        # Title with larger, bold font
        title = ttk.Label(
            self.main_container,
            text="Ultimate Calculator & Converter",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=20)

        # Create card-style frame for buttons
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        # Grid layout for buttons with consistent styling
        buttons = [
            ("Basic Calculator", self.open_basic_calculator, "info", 0, 0),
            ("Unit Converter", self.open_unit_converter, "info", 0, 1),
            ("Currency Converter", self.open_currency_converter, "info", 1, 0),
            ("View History", self.open_history, "success", 1, 1),
            ("Change Theme", self.change_theme, "warning", 2, 0),
            ("Clear History", self.clear_history, "danger", 2, 1),
            ("Export History", self.export_history, "secondary", 3, 0),
            ("Exit", self.exit_app, "danger", 3, 1),
        ]

        for text, command, style, row, col in buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                bootstyle=style,
                width=20,
                padding=10
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for responsive layout
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def open_basic_calculator(self):
        """Open the enhanced basic calculator window."""
        calculator_window = ttk.Toplevel(self.root)
        calculator_window.title("Advanced Calculator")
        calculator_window.geometry("600x800")

        # Main frame
        main_frame = ttk.Frame(calculator_window, padding="20")
        main_frame.pack(expand=YES, fill=BOTH)

        # Create notebook for different calculator modes
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=BOTH, expand=YES, pady=10)

        # Basic Operations Tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Basic")
        
        # Scientific Operations Tab
        scientific_frame = ttk.Frame(notebook)
        notebook.add(scientific_frame, text="Scientific")
        
        # Statistics Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")

        # Matrix Operations Tab
        matrix_frame = ttk.Frame(notebook)
        notebook.add(matrix_frame, text="Matrix")

        # === Basic Operations Tab ===
        # Input frame for basic calculations
        input_frame = ttk.Frame(basic_frame)
        input_frame.pack(fill=X, pady=10)

        # First number input
        ttk.Label(
            basic_frame,
            text="First Number:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        
        num1_entry = ttk.Entry(
            basic_frame,
            font=("Helvetica", 12)
        )
        num1_entry.pack(fill=X, pady=5)

        # Operation selection
        ttk.Label(
            basic_frame,
            text="Operation:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        
        operation_var = tk.StringVar(value='+')
        operations = ['+', '-', '*', '/', '^', '%', '//', '√', 'log', 'ln']
        operation_menu = ttk.Combobox(
            basic_frame,
            textvariable=operation_var,
            values=operations,
            state="readonly",
            font=("Helvetica", 12)
        )
        operation_menu.pack(fill=X, pady=5)

        # Second number input
        ttk.Label(
            basic_frame,
            text="Second Number:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        
        num2_entry = ttk.Entry(
            basic_frame,
            font=("Helvetica", 12)
        )
        num2_entry.pack(fill=X, pady=5)

        # Result display
        self.result_var = tk.StringVar(value="Result will appear here")
        self.result_label = ttk.Label(
            basic_frame,
            textvariable=self.result_var,
            font=("Helvetica", 14, "bold"),
            bootstyle="info",
            padding=10
        )
        self.result_label.pack(pady=20)

        def calculate_basic():
            try:
                num1 = float(num1_entry.get())
                num2 = float(num2_entry.get())
                operation = operation_var.get()

                result = basic_calculator(history, num1, operation, num2)
                
                # Format the result for display
                if isinstance(result, float) and result.is_integer():
                    formatted_result = int(result)
                else:
                    formatted_result = f"{result:.6g}"
                
                # Update the result display immediately
                self.result_var.set(f"Result: {formatted_result}")
                
                # Force update the display
                calculator_window.update_idletasks()
                basic_frame.update_idletasks()
                self.result_label.update_idletasks()
                
            except ValueError as e:
                self.result_var.set(f"Error: {str(e)}")
                calculator_window.update_idletasks()
            except Exception as e:
                self.result_var.set(f"Error: {str(e)}")
                calculator_window.update_idletasks()

        # Calculate button
        calc_button = ttk.Button(
            basic_frame,
            text="Calculate",
            command=calculate_basic,
            bootstyle="primary",
            width=20,
            padding=10
        )
        calc_button.pack(pady=10)

        # Clear button
        def clear_inputs():
            num1_entry.delete(0, tk.END)
            num2_entry.delete(0, tk.END)
            operation_var.set('+')
            self.result_var.set("Result will appear here")
            calculator_window.update_idletasks()

        ttk.Button(
            basic_frame,
            text="Clear",
            command=clear_inputs,
            bootstyle="secondary",
            width=20,
            padding=10
        ).pack(pady=10)

        # === Scientific Operations Tab ===
        ttk.Label(
            scientific_frame,
            text="Scientific Calculator",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Expression input
        ttk.Label(
            scientific_frame,
            text="Enter Expression (use x as variable):",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        
        expr_entry = ttk.Entry(
            scientific_frame,
            font=("Helvetica", 12)
        )
        expr_entry.pack(fill=X, pady=5)

        result_var = tk.StringVar()
        result_label = ttk.Label(
            scientific_frame,
            textvariable=result_var,
            font=("Helvetica", 12)
        )
        result_label.pack(pady=10)

        def calculate_scientific():
            try:
                expr = expr_entry.get()
                x = symbols('x')
                
                # Calculate derivative
                derivative = diff(expr, x)
                # Calculate integral
                integral = integrate(expr, x)
                # Simplify expression
                simplified = simplify(expr)

                result = f"Derivative: {derivative}\n"
                result += f"Integral: {integral}\n"
                result += f"Simplified: {simplified}"
                
                result_var.set(result)
                history.append(f"Scientific calculation: {expr}\n{result}")
            except Exception as e:
                result_var.set(f"Error: {str(e)}")

        ttk.Button(
            scientific_frame,
            text="Calculate",
            command=calculate_scientific,
            bootstyle="primary"
        ).pack(pady=10)

        # === Statistics Tab ===
        ttk.Label(
            stats_frame,
            text="Statistical Analysis",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ttk.Label(
            stats_frame,
            text="Enter numbers (comma-separated):",
            font=("Helvetica", 12)
        ).pack(anchor=W)

        stats_entry = ttk.Entry(
            stats_frame,
            font=("Helvetica", 12)
        )
        stats_entry.pack(fill=X, pady=5)

        stats_result = tk.StringVar()
        stats_label = ttk.Label(
            stats_frame,
            textvariable=stats_result,
            font=("Helvetica", 12)
        )
        stats_label.pack(pady=10)

        def calculate_stats():
            try:
                numbers = [float(x.strip()) for x in stats_entry.get().split(',')]
                numbers = np.array(numbers)
                
                result = f"Mean: {np.mean(numbers):.2f}\n"
                result += f"Median: {np.median(numbers):.2f}\n"
                result += f"Std Dev: {np.std(numbers):.2f}\n"
                result += f"Variance: {np.var(numbers):.2f}\n"
                result += f"Min: {np.min(numbers):.2f}\n"
                result += f"Max: {np.max(numbers):.2f}"
                
                stats_result.set(result)
                history.append(f"Statistical analysis:\n{result}")
            except Exception as e:
                stats_result.set(f"Error: {str(e)}")

        ttk.Button(
            stats_frame,
            text="Analyze",
            command=calculate_stats,
            bootstyle="primary"
        ).pack(pady=10)

        # === Matrix Operations Tab ===
        ttk.Label(
            matrix_frame,
            text="Matrix Operations",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Matrix A input
        ttk.Label(
            matrix_frame,
            text="Enter Matrix A (comma-separated rows, semicolon between rows):",
            font=("Helvetica", 12)
        ).pack(anchor=W)

        matrix_a_entry = ttk.Entry(
            matrix_frame,
            font=("Helvetica", 12)
        )
        matrix_a_entry.pack(fill=X, pady=5)

        # Matrix B input
        ttk.Label(
            matrix_frame,
            text="Enter Matrix B (same format):",
            font=("Helvetica", 12)
        ).pack(anchor=W)

        matrix_b_entry = ttk.Entry(
            matrix_frame,
            font=("Helvetica", 12)
        )
        matrix_b_entry.pack(fill=X, pady=5)

        matrix_result = tk.StringVar()
        matrix_label = ttk.Label(
            matrix_frame,
            textvariable=matrix_result,
            font=("Helvetica", 12)
        )
        matrix_label.pack(pady=10)

        def parse_matrix(text):
            """Convert string input to numpy matrix."""
            rows = text.strip().split(';')
            return np.array([
                [float(x.strip()) for x in row.split(',')]
                for row in rows
            ])

        def calculate_matrix():
            try:
                matrix_a = parse_matrix(matrix_a_entry.get())
                matrix_b = parse_matrix(matrix_b_entry.get())
                
                result = f"Matrix Addition:\n{matrix_a + matrix_b}\n\n"
                result += f"Matrix Multiplication:\n{matrix_a @ matrix_b}\n\n"
                result += f"Matrix A Determinant: {np.linalg.det(matrix_a):.2f}\n"
                result += f"Matrix A Inverse:\n{np.linalg.inv(matrix_a)}"
                
                matrix_result.set(result)
                history.append(f"Matrix operations:\n{result}")
            except Exception as e:
                matrix_result.set(f"Error: {str(e)}")

        ttk.Button(
            matrix_frame,
            text="Calculate",
            command=calculate_matrix,
            bootstyle="primary"
        ).pack(pady=10)

    def open_unit_converter(self):
        """Open the unit converter window with inline results."""
        unit_converter_window = ttk.Toplevel(self.root)
        unit_converter_window.title("Unit Converter")
        unit_converter_window.geometry("500x700")

        # Main container
        main_frame = ttk.Frame(unit_converter_window, padding="20")
        main_frame.pack(expand=YES, fill=BOTH)

        # Title
        ttk.Label(
            main_frame,
            text="Unit Converter",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, pady=10)

        # Category selection
        ttk.Label(
            input_frame,
            text="Select Category:",
            font=("Helvetica", 12)
        ).pack(anchor=W)

        # Conversion options for each category
        conversion_options = {
            'Length': [
                'Meters to Feet',
                'Feet to Meters',
                'Kilometers to Miles',
                'Miles to Kilometers'
            ],
            'Weight': [
                'Kilograms to Pounds',
                'Pounds to Kilograms',
                'Grams to Ounces',
                'Ounces to Grams'
            ],
            'Temperature': [
                'Celsius to Fahrenheit',
                'Fahrenheit to Celsius',
                'Celsius to Kelvin'
            ],
            'Volume': [
                'Liters to Gallons',
                'Gallons to Liters',
                'Milliliters to Ounces',
                'Ounces to Milliliters'
            ],
            'Speed': [
                'km/h to mph',
                'mph to km/h',
                'm/s to km/h',
                'km/h to m/s'
            ]
        }

        categories = list(conversion_options.keys())
        self.category_var = tk.StringVar(value=categories[0])
        self.unit_var = tk.StringVar()

        category_menu = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            bootstyle="primary"
        )
        category_menu.pack(fill=X, pady=(5, 15))

        # Unit conversion selection
        ttk.Label(
            input_frame,
            text="Select Conversion:",
            font=("Helvetica", 12)
        ).pack(anchor=W)

        def update_unit_options(*args):
            selected_category = self.category_var.get()
            unit_menu['values'] = conversion_options[selected_category]
            self.unit_var.set(conversion_options[selected_category][0])

        unit_menu = ttk.Combobox(
            input_frame,
            textvariable=self.unit_var,
            state="readonly",
            bootstyle="primary"
        )
        unit_menu.pack(fill=X, pady=(5, 15))

        # Bind category selection to update unit options
        self.category_var.trace('w', update_unit_options)
        update_unit_options()  # Initialize unit options

        # Value input
        ttk.Label(
            input_frame,
            text="Enter Value:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        
        self.value_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        self.value_entry.pack(fill=X, pady=(5, 15))

        # Result display
        result_var = tk.StringVar(value="Result will appear here")
        result_label = ttk.Label(
            main_frame,
            textvariable=result_var,
            font=("Helvetica", 14),
            bootstyle="info"
        )
        result_label.pack(pady=20)

        def convert():
            try:
                if not self.value_entry.get():
                    raise ValueError("Value field cannot be empty")
                value = float(self.value_entry.get())
                category = self.category_var.get()
                unit_choice = self.unit_var.get()

                if not category:
                    raise ValueError("Category not selected")
                if not unit_choice:
                    raise ValueError("Unit choice not selected")

                result = unit_converter(history, category, value, unit_choice)
                result_var.set(result)
            except ValueError as e:
                result_var.set(f"Error: {str(e)}")
            except Exception as e:
                result_var.set(f"Error: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)

        # Convert button
        ttk.Button(
            button_frame,
            text="Convert",
            command=convert,
            bootstyle="success-outline",
            width=20,
            padding=10
        ).pack(side=LEFT, padx=5)

        # Exit button
        ttk.Button(
            button_frame,
            text="Exit",
            command=unit_converter_window.destroy,
            bootstyle="danger-outline",
            width=20,
            padding=10
        ).pack(side=RIGHT, padx=5)

    def open_currency_converter(self):
        """Open the currency converter window with inline results."""
        currency_converter_window = ttk.Toplevel(self.root)
        currency_converter_window.title("Currency Converter")
        currency_converter_window.geometry("400x600")

        # Main frame
        main_frame = ttk.Frame(currency_converter_window, padding="20")
        main_frame.pack(expand=YES, fill=BOTH)

        # Title
        ttk.Label(
            main_frame,
            text="Currency Converter",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, pady=10)

        # Amount input
        ttk.Label(
            input_frame,
            text="Enter Amount:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        amount_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        amount_entry.pack(fill=X, pady=(5, 15))

        # From currency
        ttk.Label(
            input_frame,
            text="From Currency (e.g., USD):",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        from_currency_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        from_currency_entry.pack(fill=X, pady=(5, 15))

        # To currency
        ttk.Label(
            input_frame,
            text="To Currency (e.g., EUR):",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        to_currency_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        to_currency_entry.pack(fill=X, pady=(5, 15))

        # Result display
        result_var = tk.StringVar(value="Result will appear here")
        result_label = ttk.Label(
            main_frame,
            textvariable=result_var,
            font=("Helvetica", 14),
            bootstyle="info"
        )
        result_label.pack(pady=20)

        def convert_currency():
            try:
                if not amount_entry.get() or not from_currency_entry.get() or not to_currency_entry.get():
                    raise ValueError("Please fill all fields")

                amount = float(amount_entry.get())
                from_currency = from_currency_entry.get().strip().upper()
                to_currency = to_currency_entry.get().strip().upper()

                if not from_currency or not to_currency:
                    raise ValueError("Currencies cannot be empty")

                result = currency_converter(history, amount, from_currency, to_currency)
                result_var.set(result)
            except ValueError as e:
                result_var.set(f"Error: {str(e)}")
            except Exception as e:
                result_var.set(f"Error: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)

        # Convert button
        ttk.Button(
            button_frame,
            text="Convert",
            command=convert_currency,
            bootstyle="success-outline",
            width=20,
            padding=10
        ).pack(side=LEFT, padx=5)

        # Exit button
        ttk.Button(
            button_frame,
            text="Exit",
            command=currency_converter_window.destroy,
            bootstyle="danger-outline",
            width=20,
            padding=10
        ).pack(side=RIGHT, padx=5)

    def open_history(self):
        """Open the history window."""
        if self.root is None:
            raise RuntimeError("Root window is null")

        history_window = ttk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("400x300")

        history_text = ScrolledText(history_window, wrap=tk.WORD, width=50, height=15)
        history_text.pack(pady=10)

        if not history:
            history_text.insert(tk.END, "History is empty.\n")
        else:
            try:
                for entry in history:
                    history_text.insert(tk.END, entry + "\n")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while displaying history: {str(e)}")

    def clear_history(self):
        """Clear the history."""
        try:
            if not history:
                messagebox.showinfo("Info", "History is already empty.")
                return
            clear_history(history)
            messagebox.showinfo("Info", "History cleared.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear history: {str(e)}")

    def export_history(self):
        """Export the history to a file."""
        try:
            if not history:
                messagebox.showinfo("Info", "No history to export.")
                return
            export_history(history)
            messagebox.showinfo("Info", "History exported to 'history.txt'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export history: {str(e)}")

    def change_theme(self):
        """Change the theme between light and dark."""
        current_theme = self.style.theme.name
        
        # Toggle between light and dark themes
        if current_theme == "darkly":
            new_theme = "cosmo"
        else:
            new_theme = "darkly"
            
        try:
            self.style.theme_use(new_theme)
        except Exception as e:
            print(f"Failed to change theme: {str(e)}")

    def show_help(self):
        """Display the help menu."""
        try:
            if self.root is None:
                raise RuntimeError("Root window is null")
            help_text = show_help()
            messagebox.showinfo("Help", help_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying help: {str(e)}")

    def exit_app(self):
        """Exit the application."""
        try:
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during exit: {str(e)}")
            self.root.destroy()

# Run the GUI Application
if __name__ == "__main__":
    try:
        # Create the root window with ttkbootstrap
        root = ttk.Window(themename="cosmo")
        app = CalculatorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")