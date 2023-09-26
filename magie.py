import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import re
import operator
from collections import Counter
from fractions import Fraction
import statistics

class StatisticsCalculator:
    def __init__(self, data):
        self.data = data

    def calculate_mode(self):
        count = Counter(self.data)
        max_count = max(count.values())
        mode = [num for num, freq in count.items() if freq == max_count]
        return mode[0]

    def calculate_median(self):
        return Fraction(statistics.median(self.data)).limit_denominator()

    def calculate_range(self):
        return max(self.data) - min(self.data)

    def calculate_mean(self):
        total = Fraction(sum(self.data))
        return total / len(self.data)

    def calculate_variance(self):
        if len(self.data) == 1:
            return "Need more input for calculation"
        mean = self.calculate_mean()
        variance = sum((x - mean) ** 2 for x in self.data) / (len(self.data) - 1)
        return Fraction(variance).limit_denominator()

    def calculate_std_dev(self):
        variance = self.calculate_variance()
        if isinstance(variance, str):
            return "Need more input for calculation"
        return Fraction(variance ** 0.5).limit_denominator()

    def calculate_geometric_mean(self):
        product = 1
        for num in self.data:
            product *= num
        return product ** (1/len(self.data))

    def calculate_harmonic_mean(self):
        if 0 in self.data:
            return "Undefined due to division by 0"
        return len(self.data) / sum(1/num for num in self.data)

    @staticmethod
    def safe_eval(expr):
        # Define a safe dictionary with allowed operations and functions
        safe_dict = {
            'Fraction': Fraction,
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
        }
        
        # Only evaluate expressions that are composed of safe characters
        allowed_chars = set('0123456789/*-+^ ')
        if not all(char in allowed_chars for char in expr):
            raise ValueError("Invalid characters in expression")
        
        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')
        
        # Evaluate the expression with the safe dictionary
        return eval(expr, {"__builtins__": None}, safe_dict)

    @staticmethod
    def parse_input(input_string):
        if any(op in input_string for op in ['+', '-', '*', '/', '^']):
            return StatisticsCalculator.safe_eval(input_string)
        else:
            try:
                # First, attempt to treat as a float
                return float(input_string)
            except ValueError:
                try:
                    # Next, attempt to treat as an integer
                    return int(input_string)
                except ValueError:
                    # If it's neither float nor integer, treat as a fraction
                    return Fraction(input_string)

    @staticmethod 
    def calculate_regression_lines(x_values, y_values):
        n = len(x_values)

        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_x2 = sum([x**2 for x in x_values])
        sum_y2 = sum([y**2 for y in y_values])
        sum_xy = sum([x*y for x, y in zip(x_values, y_values)])

        # First Regression Line (y on x)
        b1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        a1 = (sum_y - b1 * sum_x) / n

        # Second Regression Line (x on y)
        b2 = (n * sum_xy - sum_x * sum_y) / (n * sum_y2 - sum_y**2)
        a2 = (sum_x - b2 * sum_y) / n

        # Formatting directly here
        y1_equation = f"{b1:.4f}x {'+ ' if a1 >= 0 else ' '}{a1:.4f}"
        y2_equation = f"{1/b2:.4f}x {'+ ' if (-a2/b2) >= 0 else ' '}{-a2/b2:.4f}"

        return {
            "y1": y1_equation,
            "y2": y2_equation
        }

    

    def calculate_correlation_coefficient(self, x_values, y_values):
        n = len(x_values)
        
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_x2 = sum([x**2 for x in x_values])
        sum_y2 = sum([y**2 for y in y_values])
        sum_xy = sum([x*y for x, y in zip(x_values, y_values)])
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))**0.5
        r = numerator / denominator
        
        return r
    

class StatisticsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Math Stats Calculator")
        self.create_widgets()

    def create_widgets(self):
        # Create the notebook (tabbed pane)
        notebook = ttk.Notebook(self.master)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create the General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self.create_general_tab(general_frame)

        # Create the Regression tab (empty for now)
        regression_frame = ttk.Frame(notebook)
        notebook.add(regression_frame, text="Regression")
        self.create_regression_tab(regression_frame)


    def create_regression_tab(self, parent_frame):
        # Frame for input fields
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(padx=20, pady=20, fill=tk.X)

        # Label and Text input for x-values
        x_label = ttk.Label(input_frame, text="X Values:")
        x_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        self.x_input_box = tk.Text(input_frame, height=3, width=50)
        self.x_input_box.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky=tk.EW)

        # Label and Text input for y-values
        y_label = ttk.Label(input_frame, text="Y Values:")
        y_label.grid(row=2, column=0, pady=(0, 10), sticky=tk.W)
        self.y_input_box = tk.Text(input_frame, height=3, width=50)
        self.y_input_box.grid(row=3, column=0, columnspan=2, pady=(0, 20), sticky=tk.EW)

        # Button to trigger regression calculation
        calc_button = tk.Button(input_frame, text="Calculate Regression", command=self.calculate_and_display_regression)
        calc_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Frame for results
        results_frame = ttk.Frame(parent_frame)
        results_frame.pack(padx=20, pady=20, fill=tk.X)

        # Labels and Entry fields for regression results
        self.regression_vars = {
            "y1": tk.StringVar(),
            "y2": tk.StringVar(),
        }

        for idx, (label, var) in enumerate(self.regression_vars.items()):
            ttk.Label(results_frame, text=label).grid(row=idx, column=0, pady=5, padx=20, sticky=tk.W)
            entry = ttk.Entry(results_frame, textvariable=var, state='readonly')
            entry.bind('<Button-1>', self.copy_to_clipboard)  # Bind click event
            entry.grid(row=idx, column=1, pady=5, padx=20, sticky=tk.EW)

            # Label to show "Copied!" message
            copied_label = ttk.Label(results_frame, text="", width=10)
            copied_label.grid(row=idx, column=2, pady=5, padx=20, sticky=tk.W)
            entry.copied_label = copied_label

        # Korrelationskoeffizient
        self.correlation_var = tk.StringVar()
        ttk.Label(results_frame, text="Korrelationskoeffizient:").grid(row=3, column=0, pady=5, padx=20, sticky=tk.W)
        correlation_entry = ttk.Entry(results_frame, textvariable=self.correlation_var, state='readonly')
        correlation_entry.bind('<Button-1>', self.copy_to_clipboard)  # Bind click event
        correlation_entry.grid(row=3, column=1, pady=5, padx=20, sticky=tk.EW)

        # Label to show "Copied!" message for Korrelationskoeffizient
        copied_label_correlation = ttk.Label(results_frame, text="", width=10)
        copied_label_correlation.grid(row=3, column=2, pady=5, padx=20, sticky=tk.W)
        correlation_entry.copied_label = copied_label_correlation

        # Korrelationsstärke
        self.correlation_strength_var = tk.StringVar()
        ttk.Label(results_frame, text="Korrelationsstärke:").grid(row=4, column=0, pady=5, padx=20, sticky=tk.W)
        correlation_strength_entry = ttk.Entry(results_frame, textvariable=self.correlation_strength_var, state='readonly')
        correlation_strength_entry.bind('<Button-1>', self.copy_to_clipboard)  # Bind click event
        correlation_strength_entry.grid(row=4, column=1, pady=5, padx=20, sticky=tk.EW)

        # Label to show "Copied!" message for Korrelationsstärke
        copied_label_strength = ttk.Label(results_frame, text="", width=10)
        copied_label_strength.grid(row=4, column=2, pady=5, padx=20, sticky=tk.W)
        correlation_strength_entry.copied_label = copied_label_strength



    def create_general_tab(self, parent_frame):
        # Tutorial/Instruction Label
        tutorial_text = (
            "1. Enter numbers separated by commas or spaces.\n"
            "2. Input like '3/4', '5+3', '5-3', and '5^3' is allowed."
        )
        tutorial_label = ttk.Label(parent_frame, text=tutorial_text, wraplength=600, justify=tk.LEFT)
        tutorial_label.pack(padx=20, pady=10)

        # Input box
        self.input_box = tk.Text(parent_frame, height=5, width=50)
        self.input_box.pack(padx=20, pady=10)
        self.input_box.bind('<Control-a>', self.select_all)

        # Button to trigger calculation
        calc_button = tk.Button(parent_frame, text="Calculate", command=self.calculate_and_display)
        calc_button.pack(pady=20)

        # Labels and Entry fields for results
        self.results_vars = {
            "Modus": tk.StringVar(),
            "Median": tk.StringVar(),
            "Spannweite": tk.StringVar(),
            "Varianz": tk.StringVar(),
            "Standardabweichung": tk.StringVar(),
            "Arithmetischer Mittelwert": tk.StringVar(),
            "Geometrischer Mittelwert": tk.StringVar(),
            "Harmonischer Mittelwert": tk.StringVar()
        }

        for label, var in self.results_vars.items():
            row = ttk.Frame(parent_frame)
            row.pack(pady=5, padx=20, fill=tk.X)
            ttk.Label(row, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row, textvariable=var, state='readonly')
            entry.bind('<Button-1>', self.copy_to_clipboard)  # Bind click event
            entry.pack(side=tk.LEFT)

            # Label to show "Copied!" message
            copied_label = ttk.Label(row, text="", width=10)
            copied_label.pack(side=tk.LEFT)
            entry.copied_label = copied_label  # Stor # Store reference to the label in the entry widget


    def calculate_and_display_regression(self):
        x_text = self.x_input_box.get(1.0, tk.END).strip()
        y_text = self.y_input_box.get(1.0, tk.END).strip()
        x_values = [StatisticsCalculator.parse_input(piece) for piece in x_text.replace(',', ' ').split() if piece.strip()]
        y_values = [StatisticsCalculator.parse_input(piece) for piece in y_text.replace(',', ' ').split() if piece.strip()]

        # Ensure that x and y values have the same length
        if len(x_values) != len(y_values):
            tk.messagebox.showerror("Error", "The number of x-values must match the number of y-values.")
            return

        calculator = StatisticsCalculator(x_values)  # Initialize with x_values just to satisfy the class constructor
        regression_lines = calculator.calculate_regression_lines(x_values, y_values)

        self.regression_vars["y1"].set(regression_lines["y1"])
        self.regression_vars["y2"].set(regression_lines["y2"])

        print(regression_lines)
        
        correlation_coefficient = calculator.calculate_correlation_coefficient(x_values, y_values)
        self.correlation_var.set(f"{correlation_coefficient:.4f}")

        correlation_strength = self.correlation_strength_label(correlation_coefficient)
        self.correlation_strength_var.set(correlation_strength)

    def select_all(self, event):
        """Select all text in the Text widget."""
        self.input_box.tag_add(tk.SEL, "1.0", tk.END)
        self.input_box.mark_set(tk.INSERT, "1.0")
        self.input_box.see(tk.INSERT)
        return 'break'

    def copy_to_clipboard(self, event):
        # Copy text from entry to clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(event.widget.get())

        # Display "Copied!" message in green color
        event.widget.copied_label.config(text="Copied!", foreground="green")

        # After 1 second (1000 milliseconds), clear the "Copied!" message and reset the color
        self.master.after(1000, lambda: event.widget.copied_label.config(text="", foreground="black"))


    @staticmethod
    def correlation_strength_label(r):
        r = abs(r)
        if 0.9 <= r <= 1:
            return "eine sehr starke"
        elif 0.8 <= r < 0.9:
            return "eine starke"
        elif 0.7 <= r < 0.8:
            return "eine mittelstarke"
        elif 0.6 <= r < 0.7:
            return "eine schwache"
        elif 0.5 <= r < 0.6:
            return "eine sehr schwache"
        else:
            return "keine"


    def calculate_and_display(self):
        input_text = self.input_box.get(1.0, tk.END).strip()
        numbers = [StatisticsCalculator.parse_input(piece) for piece in input_text.replace(',', ' ').split() if piece.strip()]
        calculator = StatisticsCalculator(numbers)

        self.results_vars["Modus"].set(calculator.calculate_mode())
        self.results_vars["Median"].set(calculator.calculate_median())
        self.results_vars["Spannweite"].set(calculator.calculate_range())
        self.results_vars["Varianz"].set(calculator.calculate_variance())
        self.results_vars["Standardabweichung"].set(calculator.calculate_std_dev())
        self.results_vars["Arithmetischer Mittelwert"].set(calculator.calculate_mean())
        self.results_vars["Geometrischer Mittelwert"].set(calculator.calculate_geometric_mean())
        self.results_vars["Harmonischer Mittelwert"].set(calculator.calculate_harmonic_mean())



if __name__ == "__main__":
    root = tk.Tk()
    gui = StatisticsGUI(root)
    root.mainloop()