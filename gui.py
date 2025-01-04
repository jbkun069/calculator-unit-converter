import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *  # Import constants for styles
from ttkbootstrap.scrolled import ScrolledText
from main import (
    basic_calculator, unit_converter, currency_converter,
    view_history, clear_history, export_history,
    change_theme, show_help, confirm_exit, THEME_LIGHT, THEME_DARK
)

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
        """Open the basic calculator window with improved UI."""
        calculator_window = ttk.Toplevel(self.root)
        calculator_window.title("Basic Calculator")
        calculator_window.geometry("400x600")

        # Create main frame with padding
        main_frame = ttk.Frame(calculator_window, padding="20")
        main_frame.pack(expand=YES, fill=BOTH)

        # Title
        ttk.Label(
            main_frame,
            text="Basic Calculator",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Input fields with better styling
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, pady=10)

        # First number
        ttk.Label(
            input_frame,
            text="First Number:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        num1_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        num1_entry.pack(fill=X, pady=(5, 15))

        # Operation
        ttk.Label(
            input_frame,
            text="Operation (+, -, *, /, ^):",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        operation_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        operation_entry.pack(fill=X, pady=(5, 15))

        # Second number
        ttk.Label(
            input_frame,
            text="Second Number:",
            font=("Helvetica", 12)
        ).pack(anchor=W)
        num2_entry = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        num2_entry.pack(fill=X, pady=(5, 15))

        # Calculate button
        ttk.Button(
            main_frame,
            text="Calculate",
            command=lambda: calculate(),
            bootstyle="success-outline",
            width=20,
            padding=10
        ).pack(pady=20)

        # Result display
        result_var = tk.StringVar(value="Result will appear here")
        result_label = ttk.Label(
            main_frame,
            textvariable=result_var,
            font=("Helvetica", 14),
            bootstyle="info"
        )
        result_label.pack(pady=20)

        def calculate():
            try:
                if not num1_entry.get() or not num2_entry.get() or not operation_entry.get():
                    raise ValueError("Please fill all fields")

                num1 = float(num1_entry.get())
                operation = operation_entry.get().strip()
                num2 = float(num2_entry.get())
                
                result = basic_calculator(history, num1, operation, num2)
                result_var.set(f"Result: {result}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

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
    root = ttk.Window(themename="cosmo")  # Initialize with light theme
    app = CalculatorApp(root)
    root.mainloop()