import tkinter as tk
from tkinter import messagebox, scrolledtext
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
        self.root = root
        self.root.title("Ultimate Calculator and Unit Converter")
        self.root.geometry("600x400")
        self.current_theme = THEME_LIGHT
        self.create_widgets()
        self.apply_theme_to_gui()

    def create_widgets(self) -> None:
        """Create and arrange widgets in the GUI."""
        if not self.root:
            raise RuntimeError("Root window is null")

        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Buttons
        tk.Button(main_frame, text="Basic Calculator", command=self.open_basic_calculator, width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(main_frame, text="Unit Converter", command=self.open_unit_converter, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Currency Converter", command=self.open_currency_converter, width=20).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(main_frame, text="View History", command=self.open_history, width=20).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Change Theme", command=self.change_theme, width=20).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(main_frame, text="Clear History", command=self.clear_history, width=20).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Export History", command=self.export_history, width=20).grid(row=3, column=0, padx=5, pady=5)

    def apply_theme_to_gui(self):
        """Apply the current theme to the GUI."""
        bg_color = "white" if self.current_theme == THEME_LIGHT else "black"
        fg_color = "black" if self.current_theme == THEME_LIGHT else "white"
        
        self.root.configure(bg=bg_color)
        
        # Update all frames and widgets with appropriate options
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg_color)
            elif isinstance(widget, (tk.Label, tk.Button)):
                widget.configure(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Menu):
                # Menus have different theme properties
                continue

    def open_basic_calculator(self):
        """Open the basic calculator window."""
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("Basic Calculator")
        calculator_window.geometry("300x400")
        
        # Create main frame with padding
        main_frame = tk.Frame(calculator_window, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Input fields with better spacing
        tk.Label(main_frame, text="Enter the first number:").pack(pady=5)
        num1_entry = tk.Entry(main_frame, width=30)
        num1_entry.pack(pady=5)

        tk.Label(main_frame, text="Enter the operation (+, -, *, /, ^):").pack(pady=5)
        operation_entry = tk.Entry(main_frame, width=30)
        operation_entry.pack(pady=5)

        tk.Label(main_frame, text="Enter the second number:").pack(pady=5)
        num2_entry = tk.Entry(main_frame, width=30)
        num2_entry.pack(pady=5)

        # Calculate button with better visibility
        calculate_button = tk.Button(
            main_frame, 
            text="Calculate", 
            command=lambda: calculate(),
            width=20,
            height=2
        )
        calculate_button.pack(pady=20)

        def calculate():
            try:
                if not num1_entry.get() or not num2_entry.get() or not operation_entry.get():
                    raise ValueError("Input fields cannot be empty")

                num1 = float(num1_entry.get())
                operation = operation_entry.get().strip()
                num2 = float(num2_entry.get())
                
                result = basic_calculator(history, num1, operation, num2)
                messagebox.showinfo("Result", f"Result: {result}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

    def open_unit_converter(self):
        """Open the unit converter window."""
        unit_converter_window = tk.Toplevel(self.root)
        unit_converter_window.title("Unit Converter")
        unit_converter_window.geometry("400x300")
        
        # Store window reference
        self.unit_converter_window = unit_converter_window
        
        # Initialize frame reference
        self.unit_options_frame = tk.Frame(unit_converter_window)
        self.unit_options_frame.pack(pady=10)
        
        categories = ["Length", "Weight", "Temperature", "Time", "Volume", "Data Storage", "Speed"]
        self.category_var = tk.StringVar(value=categories[0])

        tk.Label(self.unit_converter_window, text="Select category:").pack(pady=5)
        category_menu = tk.OptionMenu(self.unit_converter_window, self.category_var, *categories)
        category_menu.pack(pady=5)

        tk.Label(self.unit_converter_window, text="Enter the value:").pack(pady=5)
        self.value_entry = tk.Entry(self.unit_converter_window)
        self.value_entry.pack(pady=5)

        # Variable to store the selected unit option
        self.unit_var = tk.StringVar()

        def show_unit_options():
            """Show unit options based on the selected category."""
            if self.unit_options_frame is None:
                raise RuntimeError("Unit options frame is not initialized")

            # Clear previous options, if any
            for widget in self.unit_options_frame.winfo_children():
                widget.destroy()

            category = self.category_var.get()
            if not category:
                messagebox.showerror("Error", "Category is not selected")
                return

            options = {
                "Length": ["Meters to Feet", "Feet to Meters", "Kilometers to Miles", "Miles to Kilometers"],
                "Weight": ["Kilograms to Pounds", "Pounds to Kilograms", "Grams to Ounces", "Ounces to Grams"],
                "Temperature": ["Celsius to Fahrenheit", "Fahrenheit to Celsius", "Celsius to Kelvin"],
                "Time": ["Seconds to Minutes", "Minutes to Seconds", "Hours to Days", "Days to Hours"],
                "Volume": ["Liters to Gallons", "Gallons to Liters", "Milliliters to Ounces", "Ounces to Milliliters"],
                "Data Storage": ["Bytes to Kilobytes", "Kilobytes to Bytes", "Megabytes to Gigabytes", "Gigabytes to Megabytes"],
                "Speed": ["km/h to mph", "mph to km/h", "m/s to km/h", "km/h to m/s"]
            }.get(category, [])

            if not options:
                messagebox.showerror("Error", "No options available for the selected category")
                return

            if not self.unit_var:
                self.unit_var = tk.StringVar()

            self.unit_var.set(options[0])
            for option in options:
                tk.Radiobutton(self.unit_options_frame, text=option, variable=self.unit_var, value=option).pack(anchor=tk.W)

        show_unit_options()  # Show initial options
        self.category_var.trace("w", lambda *args: show_unit_options())  # Update options when category changes

        def convert():
            try:
                if not self.value_entry or not self.value_entry.get():
                    raise ValueError("Value field cannot be empty")
                value = float(self.value_entry.get())
                category = self.category_var.get()
                unit_choice = self.unit_var.get()

                if not category:
                    raise ValueError("Category not selected")
                if not unit_choice:
                    raise ValueError("Unit choice not selected")

                result = unit_converter(history, category, value, unit_choice)
                messagebox.showinfo("Result", f"Result: {result}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

        tk.Button(self.unit_converter_window, text="Convert", command=convert).pack(pady=10)

    def open_currency_converter(self):
        """Open the currency converter window."""
        if self.root is None:
            raise RuntimeError("Root window is null")

        currency_converter_window = tk.Toplevel(self.root)
        currency_converter_window.title("Currency Converter")
        currency_converter_window.geometry("300x200")

        tk.Label(currency_converter_window, text="Enter the amount:").pack(pady=5)
        amount_entry = tk.Entry(currency_converter_window)
        amount_entry.pack(pady=5)

        tk.Label(currency_converter_window, text="Enter the source currency (e.g., USD):").pack(pady=5)
        from_currency_entry = tk.Entry(currency_converter_window)
        from_currency_entry.pack(pady=5)

        tk.Label(currency_converter_window, text="Enter the target currency (e.g., INR):").pack(pady=5)
        to_currency_entry = tk.Entry(currency_converter_window)
        to_currency_entry.pack(pady=5)

        def convert_currency():
            try:
                if not amount_entry or not amount_entry.get() or not from_currency_entry or not from_currency_entry.get() or not to_currency_entry or not to_currency_entry.get():
                    raise ValueError("Input fields cannot be empty")

                amount = float(amount_entry.get())
                from_currency = from_currency_entry.get().strip().upper()
                to_currency = to_currency_entry.get().strip().upper()
                if not from_currency or not to_currency:
                    raise ValueError("Currencies cannot be empty")
                result = currency_converter(history, amount, from_currency, to_currency)
                messagebox.showinfo("Result", f"Result: {result}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

        tk.Button(currency_converter_window, text="Convert", command=convert_currency).pack(pady=10)

    def open_history(self):
        """Open the history window."""
        if self.root is None:
            raise RuntimeError("Root window is null")

        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("400x300")

        history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, width=50, height=15)
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
        self.current_theme = THEME_DARK if self.current_theme == THEME_LIGHT else THEME_LIGHT
        self.apply_theme_to_gui()
        messagebox.showinfo("Info", f"{'Dark' if self.current_theme == THEME_DARK else 'Light'} theme applied.")

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
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to exit: {str(e)}")
            self.root.destroy()

# Run the GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()