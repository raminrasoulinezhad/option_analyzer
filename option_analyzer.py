import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def option_gain(strike_price, contract_price, x):
    """
    Calculate the gain or loss for an option based on the given prices.

    Parameters:
    strike_price (float): The strike price of the option.
    contract_price (float): The price paid for the option contract.
    x (list of float): A list of current prices to evaluate against the strike price.

    Returns:
    list of float: A list representing the gain or loss for each price in x.
                   The gain is calculated as (current price - strike price) - contract price
                   if the current price is greater than or equal to the strike price.
                   Otherwise, the loss is equal to the negative contract price.
    """

    y = []
    for i in x:
        if i < strike_price:
            y.append(-contract_price)
        else:
            y.append((i - strike_price) - contract_price)
    return y

def owning_stock_gain(current_price, x):
    """
    Calculate the gain or loss for owning a stock based on the given prices.

    Parameters:
    current_price (float): The current price of the stock.
    x (list of float): A list of current prices to evaluate against the strike price.

    Returns:
    list of float: A list representing the gain or loss for each price in x.
                   The gain is calculated as (current price - strike price)
                   for all prices in x.
    """
    return [i - current_price for i in x]


# Function to update the plot based on user inputs
def update_plot():
    """
    Update the plot based on the user inputs.

    This function reads the values in the Strike Price, Contract Price and Current Price
    fields and updates the plot data. It then redraws the plot with the new data.

    If the user did not enter valid floating point values, the function displays an
    error message and returns without changing the plot.
    """

    try:
        strike_price = float(strike_price_entry.get())
        contract_price = float(contract_price_entry.get())
        current_price = float(current_price_entry.get())
    except ValueError:
        result_label.config(text="Please enter valid floating point values!")
        return

    # Update plot data
    ax.clear()

    x_max = 3 * max(strike_price, current_price, contract_price)
    x = np.linspace(0,x_max,200)

    option_gain_y = option_gain(strike_price, contract_price, x)
    ax.plot(x, option_gain_y, label="Option Gain")

    owning_stock_gain_y = owning_stock_gain(current_price, x)
    ax.plot(x, owning_stock_gain_y, label="Owning a stock")

    ax.set_title("Option Gain vs owning an stock name")
    ax.set_xlabel("Stock price at execution time")
    ax.set_ylabel("Gain for each unit of the stock")

    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.axvline(0, color='gray', linestyle='--', linewidth=1)

    # Add the legend
    ax.legend()

    canvas.draw()

# Create the main application window
root = tk.Tk()
root.title("Option Gain Analyser")

# Configure the main frame
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a matplotlib figure
fig, ax = plt.subplots()

# Embed the matplotlib figure in the Tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=2)

# Create labels and entry widgets for inputs
ttk.Label(frame, text="strike_price:").grid(row=1, column=0, sticky=tk.W, pady=5)
strike_price_entry = ttk.Entry(frame, width=10)
strike_price_entry.insert(-1, '16.0')
strike_price_entry.grid(row=1, column=1, sticky=tk.E, pady=5)

ttk.Label(frame, text="contract_price:").grid(row=2, column=0, sticky=tk.W, pady=5)
contract_price_entry = ttk.Entry(frame, width=10)
contract_price_entry.insert(-1, '4.0')
contract_price_entry.grid(row=2, column=1, sticky=tk.E, pady=5)

ttk.Label(frame, text="current_price:").grid(row=3, column=0, sticky=tk.W, pady=5)
current_price_entry = ttk.Entry(frame, width=10)
current_price_entry.insert(-1, '19.25')
current_price_entry.grid(row=3, column=1, sticky=tk.E, pady=5)

# Add a button to update the plot
update_button = ttk.Button(frame, text="Update Plot", command=update_plot)
update_button.grid(row=5, column=1, columnspan=1, pady=10)

# Label to display results or errors
result_label = ttk.Label(frame, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Add a button to exit the application
exit_button = ttk.Button(frame, text="Exit", command=lambda: root.quit())
exit_button.grid(row=5, column=0, columnspan=1, pady=10)

# Run the Tkinter event loop
root.mainloop()
