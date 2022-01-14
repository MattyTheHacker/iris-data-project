import tkinter as tk
from matplotlib import pyplot as plt

def test():
    pass

def plot1():
    tx = [5,6,7,8,9,10,11,12,13,14,15,16,17]
    ty = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300]

    plt.plot(tx, ty)
    plt.show()


# Initialise Tkinter and set a title.
print("Intitialising tkinter")
root = tk.Tk()
root.title("Flower Analysis")
root.geometry("400x400")

# Create tkinter menu
print("Creating Menu Bar")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create file menu item
print("Creating File Menu")
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open File", command=test)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=test)

# Create edit menu item
print("Creating Edit Menu")
edit_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=test)
edit_menu.add_command(label="Copy", command=test)
edit_menu.add_command(label="Paste", command=test)
file_menu.add_separator()

# Create data control menu item
print("Creating Data Menu")
data_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Data", menu=data_menu)
data_menu.add_command(label="Plot Bar Chart", command=test)
data_menu.add_command(label="Plot Scatter Graph", command=test)

# Create help menu item
print("Creating Help Menu")
help_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=test)
help_menu.add_command(label="Help", command=test)

# Create dev menu item
print("Creating Help Menu")
dev_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Dev", menu=dev_menu)
dev_menu.add_command(label="Plot 1", command=test)
dev_menu.add_command(label="Plot 2", command=plot1)


print("Running Main Loop...")
root.mainloop()
print("Main Loop Complete.")