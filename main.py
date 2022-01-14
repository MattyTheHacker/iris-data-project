import os
import csv
import time
import numpy as np
import tkinter as tk
from tkinter import filedialog
from collections import OrderedDict
from matplotlib import pyplot as plt

# Set a constant with the file path to enable easy access later.
PRIMARY_DIR = os.path.dirname(os.path.abspath(__file__))
# Set constant to identify specific data file to allow for unique analysis options
IRIS_COLUMN_NAMES = ['id', ' species', ' sepal_length', ' sepal_width', ' petal_length', ' petal_width']

# Class for tkinter to give the user the option to select data for the scatter graph
class ScatterGraphWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('400x150')
        self.title('Generic Scatter Graph Window')

        # Get the data columns
        with open(filepath) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    column_names_list = (", ".join(row)).split(sep=",") # Extract column names from csv dictionary
                    line_count += 1
                line_count += 1

        # Setup the drop down menus
        x_axis_data_dropdown_selected = tk.StringVar(self)
        x_axis_data_dropdown_selected.set("Select an Option")
        x_axis_data_dropdown = tk.OptionMenu(self, x_axis_data_dropdown_selected, *column_names_list)
        x_axis_data_dropdown.pack(expand=True, side="left")

        y_axis_data_dropdown_selected = tk.StringVar(self)
        y_axis_data_dropdown_selected.set("Select an Option")
        y_axis_data_dropdown = tk.OptionMenu(self, y_axis_data_dropdown_selected, *column_names_list)
        y_axis_data_dropdown.pack(expand=True, side="right")

        # Create plot graph button
        plot_graph_button = tk.Button(self, text='Plot Graph', command=lambda : \
            select_generic_data(x_axis_data_dropdown_selected.get().strip(), y_axis_data_dropdown_selected.get().strip(),"scatter"))
        plot_graph_button.pack(expand=True)

        # Create exit button
        exit_button = tk.Button(self, text='Close', command=self.destroy)
        exit_button.pack(expand=True, side="bottom")

class GenericBarChartSelectionWindow(tk.Toplevel):
    def __init__(self, master, bar_data, row_index):
        super().__init__(master)
        self.geometry('400x200')
        self.title('Bar Chart Data Selection')

        tk.Label(self, text='Please select the fields you want to include:').pack(expand=True)

        self.check_box_selection = {}
        self.row_index = row_index
        self.bar_data = bar_data

        for i in bar_data:
            var = tk.IntVar()
            tk.Checkbutton(self, text=i, variable=var).pack(expand=True)
            self.check_box_selection[i] = var

        confirm_button = tk.Button(self, text="OK", command=self.convert_selection_to_data)
        confirm_button.pack(expand=True)

        # Create exit button
        exit_button = tk.Button(self, text='Close', command=self.destroy)
        exit_button.pack(expand=True, side="bottom")


    def convert_selection_to_data(self):
        check_box_values = [(i, var.get()) for i, var in self.check_box_selection.items()]
        dict_box_values = OrderedDict(check_box_values)

        new_dict_box_values = dict_box_values.copy()
        for key, value in new_dict_box_values.items():
            if value == 0:
                del dict_box_values[key]

        desired_data_labels = list(dict_box_values.keys())

        dict_bar_data = self.bar_data.copy()
        for key, value in dict_bar_data.items():
            if key in desired_data_labels:
                pass
            else:
                del self.bar_data[key]

        bar_labels = list(self.bar_data.keys())
        n = len(bar_labels)
        bx = range(1, n+1)
        
        try:
            data = [float(i) for i in self.bar_data.values()]
            t = int(time.time())
            plt.figure(t)
            plt.bar(x=bx, height=data, tick_label=bar_labels)
            plt.title(f"Graph to show: {bar_labels}")
            plt.show()
        except ValueError:
            invalid_data_window = InvalidDataSelection(root)
            invalid_data_window.grab_set()

class BarChartWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('400x200')
        self.title('Generic Bar Chart Window')

        first_column_list = []

        # Get the data columns
        with open(filepath) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    column_names_list = (", ".join(row)).split(sep=",") # Extract column names from csv dictionary
                    line_count += 1
                first_column_list.append(row[column_names_list[0].strip()])
                line_count += 1

        tk.Label(self, text="Please select the record you wish to view.").pack(expand=True)

        record_dropdown_selected = tk.StringVar(self)
        record_dropdown_selected.set("Select an Option")
        record_dropdown = tk.OptionMenu(self, record_dropdown_selected, *first_column_list)
        record_dropdown.pack(expand=True, pady=5)

        plot_graph_button = tk.Button(self, text="Plot Graph", command=lambda:self.select_generic_bar_data(record_dropdown_selected.get().strip()))
        plot_graph_button.pack(expand=True, pady=5)

        # Create exit button
        exit_button = tk.Button(self, text='Close', command=self.destroy)
        exit_button.pack(expand=True, side="bottom", pady=5)

    def select_generic_bar_data(arg1, row_index):
        if row_index != "Select an Option":
            bar_data = None
            with open(filepath) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        column_names_list = (", ".join(row)).split(sep=",") # Extract column names from csv dictionary
                        line_count += 1
                    line_count += 1
                    if row[column_names_list[0]] == row_index:
                        bar_data = row
                        del bar_data[column_names_list[0]]
                # print(bar_data)
            bar_chart_data_select_window = GenericBarChartSelectionWindow(root, bar_data, row_index)
            bar_chart_data_select_window.grab_set()
        else:
            no_data_warning_window = DataNotSelectedWarning(root)
            no_data_warning_window.grab_set()
            print("Data not selected. Try again.")


    def plot_generic_bar(data):
        print(data)



# Class for tkinter window to warn the user they haven't selected data properly. 
class DataNotSelectedWarning(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('350x100')
        self.title('Data Manager Tools: Warning!')
        tk.Label(self, text="ATTENTION! \n You have not selected any data. \n Please check your selection and try again.").pack(expand=True)
        tk.Button(self, text="OK", command=self.destroy).pack(expand=True)

class InvalidDataSelection(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('350x100')
        self.title('Data Manager Tools: Warning!')
        tk.Label(self, text='ATTENTION!\n The data you have selected contains invalid values.\n Please check your selection and try again.').pack(expand=True)
        tk.Button(self, text='OK', command=self.destroy).pack(expand=True)

class EmptyFileSelectionWarning(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('350x100')
        self.title("Data Manager Tools: Warning!")
        tk.Label(self, text="ATTENTION!\n The file you selected appears to be empty.\n Please check your selection and try again.").pack(expand=True)
        tk.Button(self, text='OK', command=self.destroy).pack(expand=True)

class NoFileSelectedWarning(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('450x100')
        self.title("Data Manager Tools: Warning!")
        tk.Label(self, text="ATTENTION!\n You either didn't select a file or the file you selected couldn't be loaded.\n \
            Please check your selection and try again.\n If this issue persists please ").pack(expand=True)
        tk.Button(self, text='OK', command=self.destroy).pack(expand=True)

class QuitAppConfirm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x100")
        self.title("Application Manager: Confirm Action.")
        tk.Label(self, text="Are you sure you want to quit?\n\nUnsaved data will be lost.").pack(expand=True, side="top")
        tk.Button(self, text="Yes", command=exit_app).pack(expand=True, side="right", ipady=40, ipadx=20, padx=10, pady=10)
        tk.Button(self, text="No", command=self.destroy).pack(expand=True, side="left", ipady=40, ipadx=20, padx=10, pady=10)


'''
This function is triggerred when the user wants to quit the application
A window is opened with a yes or no button, if yes then quit function is called
If no then confirm window is closed.
'''
def quit_app_confirm():
    # Get confirmation of user quit request.
    confirm_window = QuitAppConfirm(root)
    confirm_window.grab_set()


'''
Exit function called when the user confirms they want to exit the program
Quit the app and destroy all active windows.
'''
def exit_app():
    root.quit
    root.destroy()

'''
This is the first function called when the program starts, it displays brief instructions
and makes sure that the correct menu options are enabled.
'''
def welcome():
    # If a user has selected a file, enable the data menu. If not, disable it.
    try:
        if filepath:
            pass
    except:
        data_menu.entryconfig("0",state="disabled")
        data_menu.entryconfig("1",state="disabled")
        # print("Data menus disabled.")

    # Standard welcome message
    global welcome_label
    welcome_text = "Welcome! To begin please click 'File' then 'Open File' to select your data.\n Please note this application only supports CSV files."
    welcome_label = tk.Label(root, text=welcome_text, pady=20, padx=20)
    welcome_label.pack()

'''
Function to make sure all open windows are closed. 
'''
def destroy_all():
    try:
        if welcome_label:
            welcome_label.destroy()
            # print("Welcome label destroyed.")
    except:
        # print("Welcome Label not found.")
        pass

    try:
        if file_info_label:
            file_info_label.destroy()
            # print("File info label destroyed.")
    except:
        # print("File Info Label not found.")
        pass

    try:
        if awaiting_file_label:
            awaiting_file_label.destroy()
            # print("Awaiting file label destroyed.")
    except:
        # print("Awaiting File Label not found.")
        pass

    try:
        if column_names_label:
            column_names_label.destroy()
            # print("Column names label destroyed.")
    except:
        # print("Column Names Label not found.")
        pass

'''
Function to provide accesss to generic graphing tools which can be used on any data
Provides a use for the program even if the user isn't using the iris data.
'''
def generic_tools():
    # print("Opening generic graphing tools")
    try:
        iris_confirm_window.destroy()
    except:
        # print("Iris confirm window wasn't open.")
        pass

    global generic_graph_tools_window
    generic_graph_tools_window = tk.Toplevel(root)
    generic_graph_tools_window.title("Generic Graphing Tool")
    generic_graph_tools_window.grid_rowconfigure(0, weight=1)
    generic_graph_tools_window.grid_columnconfigure(0, weight=1)

    scatter_graph_button = tk.Button(generic_graph_tools_window, text="Scatter Graph", padx= 10, pady=10, command=generic_scatter_graph)
    scatter_graph_button.grid(column=8, row=24)

    bar_chart_button = tk.Button(generic_graph_tools_window, text="Bar Chart", padx=10, pady=10, command=generic_bar_chart)
    bar_chart_button.grid(column=16, row=24)

    return_to_menu_button = tk.Button(generic_graph_tools_window, text="Exit Graphing Options", padx=10, pady=10, command=close_graphing_menu)
    return_to_menu_button.grid(column=24, row=24)

def generic_scatter_graph():
    generic_scatter_graph_window = ScatterGraphWindow(root)
    pass

def generic_bar_chart():
    generic_bar_chart_window = BarChartWindow(root)
    pass


'''
Iris tools function provides access to more unique tools specific to the iris data
Beneficial for more indepth analysis 
'''
def iris_tools():
    # global species_list, setosa_list, versicolor_list, virginica_list
    # setosa_list, versicolor_list, virginica_list = ([] for i in range(3))
    species_list = []
    x, y = [], []

    # print("Opening iris specific tools")
    try:
        iris_confirm_window.destroy()
    except:
        # print("Iris confirm window wasn't open.")
        pass


    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                column_names_list = (", ".join(row)).split(sep=",") # Extract column names from csv dictionary
                line_count += 1
            species_list.append(row['species'])
            # if row['species'] == "setosa":
            #     setosa_list.append(row)
            # if row['species'] == "versicolor":
            #     versicolor_list.append(row)
            # if row['species'] == "virginica":
            #     virginica_list.append(row)
            line_count += 1
        species_list = list(set(species_list))

    global iris_graph_tools_window
    iris_graph_tools_window = tk.Toplevel(root)
    iris_graph_tools_window.title("Iris Graphing Tools - Data Selection")
    iris_graph_tools_window.grid_rowconfigure(0, weight=1)
    iris_graph_tools_window.grid_columnconfigure(0, weight=1)

    iris_graph_tools_info_label_text = "Welcome to the specialised graphing tools!\n Use the dropdown menus below to choose the two sets of data you wish to compare.\
        \n If you're having issues with the bar chart formatting please try to use the generic tools before reporting an issue."
    iris_graph_tools_info_label = tk.Label(iris_graph_tools_window, text=iris_graph_tools_info_label_text).grid(column=12, row=2)

    iris_graph_tools_x_axis_label = tk.Label(iris_graph_tools_window, text="X-Axis").grid(column=8, row=4)
    iris_graph_tools_y_axis_label = tk.Label(iris_graph_tools_window, text="Y-Axis").grid(column=16, row=4)

    data_dropdown_options = column_names_list[2:]
    species_dropdown_options = species_list

    x_axis_data_dropdown_selected = tk.StringVar(iris_graph_tools_window)
    x_axis_data_dropdown_selected.set("Select an Option")
    x_axis_data_dropdown = tk.OptionMenu(iris_graph_tools_window, x_axis_data_dropdown_selected, *data_dropdown_options)
    x_axis_data_dropdown.grid(column=8, row=12)

    y_axis_data_dropdown_selected = tk.StringVar(iris_graph_tools_window)
    y_axis_data_dropdown_selected.set("Select an Option")
    y_axis_data_dropdown = tk.OptionMenu(iris_graph_tools_window, y_axis_data_dropdown_selected, *data_dropdown_options)
    y_axis_data_dropdown.grid(column=16, row=12)

    x_axis_species_dropdown_selected = tk.StringVar(iris_graph_tools_window)
    x_axis_species_dropdown_selected.set("Select an Option")
    x_axis_species_dropdown = tk.OptionMenu(iris_graph_tools_window, x_axis_species_dropdown_selected, *species_dropdown_options)
    x_axis_species_dropdown.grid(column=8, row=6)

    y_axis_species_dropdown_selected = tk.StringVar(iris_graph_tools_window)
    y_axis_species_dropdown_selected.set("Select an Option")
    y_axis_species_dropdown = tk.OptionMenu(iris_graph_tools_window, y_axis_species_dropdown_selected, *species_dropdown_options)
    y_axis_species_dropdown.grid(column=16, row=6)

    scatter_graph_button = tk.Button(iris_graph_tools_window, text="Scatter Graph", padx= 10, pady=10, command=lambda : \
        select_iris_data(x_axis_species_dropdown_selected.get().strip(), x_axis_data_dropdown_selected.get().strip(), \
            y_axis_species_dropdown_selected.get().strip(), y_axis_data_dropdown_selected.get().strip(),"scatter"))
    scatter_graph_button.grid(column=12, row=32)

    bar_chart_button = tk.Button(iris_graph_tools_window, text="Bar Chart", padx= 10, pady=10, command=lambda : \
        select_iris_data(x_axis_species_dropdown_selected.get().strip(), x_axis_data_dropdown_selected.get().strip(), \
            y_axis_species_dropdown_selected.get().strip(), y_axis_data_dropdown_selected.get().strip(),"bar"))
    bar_chart_button.grid(column=12, row=48)

    return_to_menu_button = tk.Button(iris_graph_tools_window, text="Exit Graphing Options", padx=10, pady=10, command=close_graphing_menu)
    return_to_menu_button.grid(column=12, row=64)

'''
Function to take data from iris tools and send data to the correct graphing function
Ensures that the data is properly appended to lists so matplot can handle it
'''
def select_iris_data(x_species, x_data, y_species, y_data, chart_type):
    if "Select an Option" in (x_species, x_data, y_species, y_data):
        no_data_warning_window = DataNotSelectedWarning(root)
        no_data_warning_window.grab_set()
        print("Data not selected. Try again.")
        pass
    else:
        x, y = [], []
        with open(filepath) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if x_species == y_species:
                    if row['species'] == x_species:
                        x.append(row[x_data])
                        y.append(row[y_data])
                else:
                    if row['species'] == x_species:
                        x.append(row[x_data])
                    elif row['species'] == y_species:
                        y.append(row[y_data])

        x_label = x_species + ' ' + x_data
        y_label = y_species + ' ' + y_data

        if chart_type == "scatter":
            plot_scatter_graph(x, y, x_label, y_label)
        elif chart_type == "bar":
            plot_bar_chart(x, y, x_label, y_label)
        else:
            print("Unexpected Failure. Chart type was not passed correctly. Please report this immediately.")


def select_generic_data(x_data, y_data, chart_type):
    if "Select an Option" in (x_data, y_data):
        no_data_warning_window = DataNotSelectedWarning(root)
        no_data_warning_window.grab_set()
        print("Data not selected. Try again.")
        pass
    else:
        data = {}
        x, y = [], []
        with open(filepath) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
        x, y = data[x_data], data[y_data]

        try:
            x = [float(i) for i in x]
            y = [float(i) for i in y]
            x_label, y_label = str(x_data), str(y_data)

            if chart_type == "scatter":
                plot_scatter_graph(x, y, x_label, y_label)
            elif chart_type == "bar":
                plot_bar_chart(x, y, x_label, y_label)
            else:
                print("Unexpected Failure. Chart type was not passed correctly. Please report this immediately.")
        except ValueError:
            invalid_data_window = InvalidDataSelection(root)
            invalid_data_window.grab_set()
            # print("Value error occured. See log.")


'''
Function to check if the data being imported matches the known iris data
If it does, enable specific tools, if not disable specific tools and use generic
Also present a diaolouge to the user asking if they want to use specific tools or not.
'''
def check_data(column_names_list):
    if column_names_list == IRIS_COLUMN_NAMES:
        data_menu.entryconfig("2", state="normal")

        global iris_confirm_window
        iris_confirm_window = tk.Toplevel(root)
        iris_confirm_window.title("Recognised Data")

        iris_confirm_label_text = "Hey! It looks like you might be using a recognised data set. Would you like to use the specialised tools for this data?"
        iris_confirm_label = tk.Label(iris_confirm_window, text=iris_confirm_label_text).pack(padx=20, pady=20)
        iris_confirm_yes_button = tk.Button(iris_confirm_window, text="Yes", command=iris_tools).pack(padx=20, pady=20)
        iris_confirm_no_button = tk.Button(iris_confirm_window, text="No", command=generic_tools).pack(padx=20, pady=20)
    else:
        # print("Data not recognised. Using generic tools.")
        data_menu.entryconfig("2", state="disabled")
        generic_tools()

'''
Function to close the graphing menu, used to ensure both tools aren't open at once
Call welcome function when done
'''
def close_graphing_menu():
    # print("Close graphing menu.")
    destroy_all()
    try:
        iris_graph_tools_window.destroy()
        plt.close('all')
    except:
        # print("Iris tools not open.")
        pass
    try:
        generic_graph_tools_window.destroy()
        plt.close('all')
    except:
        # print("Generic tools not open.")
        pass
    welcome()

# Function to handle a critical error in one of the windows
def critical_exit():
    # TODO: Add a label here
    # print("The active window was closed due to a critical error. See log for more information.")
    destroy_all()


def open_file():
    # Ensure variables are null before processing and remove all canvas elements so the UI is clean.
    global filepath
    filepath = None
    filename = None
    destroy_all()
    # Brief label so the user knows what is going on. Also helpful for debugging. !! Make a note !! Might remove later.
    global awaiting_file_label
    awaiting_file_label = tk.Label(root, text="Awaiting File...", padx=10, pady=10)
    awaiting_file_label.pack()
    # Get the path of the file that the user wants to open
    filepath = filedialog.askopenfilename(initialdir=PRIMARY_DIR, title="Select a File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    # Check that the user actually selected a file, if not, do nothing.
    if filepath:
        #Extract the file name from the path and display it to the user.
        filename = os.path.split(filepath)[1]
        # print(f'Selected File: {filename}')

        #Check that the file actually has data in it before opening.
        if os.stat(filepath).st_size == 0:
            empty_file_warning = EmptyFileSelectionWarning(root)
            empty_file_warning.grab_set()
            filepath = None
            filename = None
        else:
            # Enable data menu for easy access to graph options
            data_menu.entryconfig("0", state="normal")
            # Open the CSV file selected and place the data into a dictionary.
            with open(filepath) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                global data
                data = csv_reader
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        global column_names_list
                        column_names_list = (", ".join(row)).split(sep=",") # Extract column names from csv dictionary
                        # print(f'Column names are {column_names_list}')
                        global column_names_label
                        column_names_label = tk.Label(root, text=f'Column names are {column_names_list}', padx=20, pady=20)
                        column_names_label.pack() # !! Make a note !! This needed to be seperated from the previous line to allow for remote deletion.
                        line_count += 1
                    line_count += 1
                row_count = line_count - 1
                global file_info_label
                file_info_label = tk.Label(root, text=f'File "{filename}" selected. {row_count} rows were successfully imported.', padx=20, pady=20)
                file_info_label.pack()
            check_data(column_names_list)
    else:
        # User did not select a file. Display a warning.
        no_file_warning_label = NoFileSelectedWarning(root)
        no_file_warning_label.grab_set()

#Testing Function. Should be removed from final production.
def test_scatter_graph():
    pass
    tx = [5,6,7,8,9,10,11,12,13,14,15,16,17]
    ty = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300]

    plt.plot(tx, ty)
    plt.show()

#Testing Function. Should be removed from final production.
def test_bar_chart():
    pass
    tx = [5,6,7,8,9,10,11,12,13,14,15,16,17]
    ty = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300]
    plt.bar(tx, ty)
    plt.show()

# Function to take provided data and plot the chart
def plot_scatter_graph(x, y, x_label, y_label):
    try:
        t = int(time.time()) # Current time is used as the figure ID to allow an infinite number of figures open at once
        x = [float(n) for n in x] # cast the x to floats
        y = [float(n) for n in y] # cast the y list to floats
        npx = np.asarray(x)
        npy = np.asarray(y)
        m, b = np.polyfit(npx, npy, 1)
        plt.figure(t)
        plt.scatter(x, y)
        plt.plot(npx, m*npx +b)
        plt.title(f"Graph to compare '{x_label}' and '{y_label}'")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    except ValueError:
        invalid_data_window = InvalidDataSelection(root)
        invalid_data_window.grab_set()
        # print("Value error occured. See log.")

# Function to take provided data and plot the chart
def plot_bar_chart(x, y, x_label, y_label):
    try:
        t = int(time.time())
        x = [float(n) for n in x]
        y = [float(n) for n in y]
        # print(min(x), min(y))
        plt.figure(t)
        plt.bar(x, y)
        plt.title(f"Graph to compare '{x_label}' and '{y_label}'")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    except ValueError:
        invalid_data_window = InvalidDataSelection(root)
        invalid_data_window.grab_set()
        # print("Value error occured. See log.")

def delete_welcome():
    welcome_label.destroy()

# Initialise Tkinter and set a title.
# print("Intitialising tkinter")
root = tk.Tk()
root.title("Flower Analysis")
root.geometry("800x400")

# Create tkinter menu
# print("Creating Menu Bar")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create file menu item
# print("Creating File Menu")
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_app_confirm)

# Create edit menu item
# print("Creating Edit Menu")
edit_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
file_menu.add_separator()

# Create data control menu item
# print("Creating Data Menu")
data_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Data", menu=data_menu)
data_menu.add_command(label="Open Generic Graphing Tools", command=generic_tools)
data_menu.add_command(label="Open Iris Graphing Tools", command=iris_tools)

# Create help menu item
# print("Creating Help Menu")
help_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help")
help_menu.add_command(label="Help")

# Create dev menu item
# print("Creating Help Menu")
dev_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Dev", menu=dev_menu)
dev_menu.add_command(label="Plot Bar Chart", command=test_bar_chart)
dev_menu.add_command(label="Plot Scatter Graph", command=test_scatter_graph)
dev_menu.add_command(label="Delete welcome", command=delete_welcome)
# dev_menu.add_command(label="Exit Graph Options", command=graph_options_window.destroy)
# dev_menu.add_command(label="Exit Confirm Window", command=confirm_window.destroy)
# dev_menu.add_command(label="Test Data Integrity", command=GenericBarChartSelectionWindow.print_data)

# Begin meaningful paint
welcome()
# print("Running Main Loop...")
root.mainloop()
# print("Program exited.")