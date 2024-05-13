# imports
import tkinter as tk
import json
import csv
from tkinter import Label
from tkinter import ttk
from tkinter import filedialog
import datetime
from xml.etree import ElementTree as ET
import os

#Github Link
#https://github.com/TimlerTheTerp/Project-2

#Tyler Vu, I was in charge of making the start screen
#1 I made a start screen which prompts the user to welcome the user to the screen. Makes the program better by greeting the user
#Thara Le, I was in charge of making design/aesthetic changes.
#2 I edited the colors, geometry, added borders, and moved around buttons to look more appealing to the user.
#Salih Awel, I was in charge of improving the overall user interface and experience.
#3 Added resizable windows, implemented vertical scrollbars in text area for large notes, incorporated keyboard shortcuts (Ctrl+N, Ctrl+Q),
#included tooltip text on buttons for guidance. Changed font to Arial for readability.
#Alexander Guidinetti, I was in charge of condensing/revising.
#4 I fixed some bugs with the opening/quitting, condensed/revised some parts, and added a live time on all the windows.

class StartScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Arial', 12, 'bold')}

        # Frame for title
        f = tk.Frame(self, bg='purple', bd=5)
        f.place(x=220, y=100)

        # Title
        l = Label(f, text="  Welcome to the Note Creating Machine!  ", font=("Arial", 16), fg='black')
        l.pack()

        # Date and Time Label
        self.date_time_label = Label(self, text="", font=("Arial", 12), bg='#efd9fd')
        self.date_time_label.place(x=10, y=10)

        # Start button
        self.start_button = tk.Button(self, text="Begin", command=self.MainSelection, **self.button_style)
        self.start_button.place(x=250, y=250)

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.Quit, **self.button_style)
        self.quit_button.place(x=530, y=250)

    # 2 I made the opening where the user gets to open the maker move, the user clicks and opens the program. This improves the program because it leads the user to the main screen
    def MainSelection(self):
        self.destroy()  # Close the StartScreen window
        start = MainWindow()  # Create an instance of MainWindow
        start.mainloop()  # Run the MainWindow loop

    # 3 I made a quit button as well because what if the user decides to exit the program. If the user accidentally clicks on this program, he or she will have the choice to exit out
    def Quit(self):
        self.destroy()

#Tyler Vu, Helps chooses fileformat, this thing is important because it allows the user to choose file format
class FileFormatDialog(tk.Toplevel):
    def __init__(self, filly):
        super().__init__(filly)

        self.title("Select Preffered File Format")
        self.geometry("300x150")
        self.grab_set()

        label = tk.Label(self, text="Select the file format:")
        label.pack(pady=10)

        self.file_format = tk.StringVar()
        self.file_format.set("txt")  # Set default selection

        formats = [("Text File (.txt)", "txt"),
                   ("JSON (.json)", "json"),
                   ("CSV (.csv)", "csv"),
                   ("XML (.xml)", "xml")]

        for text, value in formats:
            radio = tk.Radiobutton(self, text=text, variable=self.file_format, value=value)
            radio.pack(anchor="w")

        button = tk.Button(self, text="Save", command=self.save_format)
        button.place(x = 175, y = 100)

    def save_format(self):
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')
        self.notebook = []
        self.notes = []

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Arial', 12, 'bold')}

        self.minsize(800, 500)
        self.maxsize(1200, 800)

        self.bind("<Control-n>", lambda event: self.new_note())
        self.bind("<Control-q>", lambda event: self.quit_app())

        self.tooltip_window = None

        # Date and Time Label
        self.date_time_label = Label(self, text="", font=("Arial", 12), bg='#efd9fd')
        self.date_time_label.place(x=10, y=10)
        self.update_date_time_label()  # Update the date and time label

        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note, **self.button_style)
        self.new_button.pack(pady=(100, 30))
        self.new_button.bind("<Enter>", lambda event: self.show_tooltip("Create a new note"))
        self.new_button.bind("<Leave>", lambda event: self.hide_tooltip())

        # Open Note Button
        self.open_button = tk.Button(self, text="Open Note", command=self.open_notebook, **self.button_style)
        self.open_button.pack(pady=30)
        self.open_button.bind("<Enter>", lambda event: self.show_tooltip("Open an existing note"))
        self.open_button.bind("<Leave>", lambda event: self.hide_tooltip())

        # Quit Notebook Button
        self.quit_button = tk.Button(self, text="Quit Notebook", command=self.quit_app, **self.button_style)
        self.quit_button.pack(pady=30)
        self.quit_button.bind("<Enter>", lambda event: self.show_tooltip("Quit the notebook application"))
        self.quit_button.bind("<Leave>", lambda event: self.hide_tooltip())

    def new_note(self):
        note_window = NoteForm(self, self.notebook, self.notes, self.button_style)
        return None

    def open_notebook(self):
        filepath = filedialog.askopenfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
                                              filetypes=[("text files", "*.txt"), ("all files", "*.*")])

        if filepath:
            with open(filepath, 'r') as file:
                file_contents = file.read()
                note_chunks = file_contents.split('\n\n')

                self.notes = []

                for chunk in note_chunks:
                    lines = chunk.strip().split('\n')
                    if len(lines) >= 3:
                        title = lines[0]
                        text = '\n'.join(lines[1:-1])
                        meta = lines[-1]

                        note_dict = {'title': title, 'text': text, 'meta': meta}
                        self.notes.append(note_dict)
                    else:
                        print(f"Skipping invalid note chunk: {chunk}")

            note_window = NoteForm(self, self.notebook, self.notes, self.button_style)
            note_window.load_note()

    def quit_app(self):
        self.destroy()

    def update_date_time_label(self):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=f"Current Date and Time: {formatted_date_time}")
        self.date_time_label.after(1000, self.update_date_time_label)

    def show_tooltip(self, text):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = tk.Toplevel(self)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry("+%d+%d" % (self.winfo_pointerx() + 20, self.winfo_pointery()))
        label = tk.Label(self.tooltip_window, text=text, bg="black", fg="yellow", padx=5, pady=2)
        label.pack()

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class NoteForm(tk.Toplevel):
    def __init__(self, master, notebook, notes, button_style):
        super().__init__(master)

        self.notes = notes

        self.geometry("800x400")
        self.configure(bg='#efd9fd')

        self.minsize(800, 400)
        self.maxsize(1200, 800)

        # Snippet Title
        title_label = tk.Label(self, bg='#efd9fd', text='Note Title:', font=('Arial', 12, 'bold'), fg='black')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        # Snippet
        text_label = tk.Label(self, bg='#efd9fd', text='Note Text:', font=('Arial', 12, 'bold'), fg='black')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.snippet_title = tk.Entry(self, width=40, font=('Arial', 12))
        self.snippet_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.snippet_title.insert(0, 'Untitled')

        text_scrollbar = tk.Scrollbar(self)
        text_scrollbar.grid(row=2, column=2, sticky="ns")

        self.snippet = tk.Text(self, height=10, width=60, font=('Arial', 12), yscrollcommand=text_scrollbar.set)
        self.snippet.grid(padx=10, pady=10, row=2, column=1, sticky="nsew")

        text_scrollbar.config(command=self.snippet.yview)

        buttons_frame = tk.Frame(self, bg='#efd9fd')
        buttons_frame.grid(row=6, column=1)

        # Submit Note Button
        self.submit_button = tk.Button(buttons_frame, text="Submit Note", command=self.submit, **button_style)
        self.submit_button.grid(row=0, column=0, padx=50)

        # Quit Note Button
        self.quit_button = tk.Button(buttons_frame, text="Quit Note", command=self.quit_note, **button_style)
        self.quit_button.grid(row=0, column=1, padx=50)

    def submit(self):
        note_dict = {
            "title": self.snippet_title.get(),
            "text": self.snippet.get("1.0", tk.END),
            "metadata": self.metadata()
        }

        new_note = MakeNote(note_dict)
        self.notes.append(new_note)

        self.save_file()

    def metadata(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")

    def save_file(self):
        # Create the file format dialog
        dialog = FileFormatDialog(self)
        self.wait_window(dialog)  # Wait until the dialog is closed

        # Get the selected file format
        file_format = dialog.file_format.get()

        now = datetime.datetime.now()
        title = self.snippet_title.get()
        text = self.snippet.get('1.0', 'end').strip('\n')
        meta = f'created {now}'
        note_dict = {'title': title, 'text': text, 'meta': meta}

        # Add the note to the notes list
        self.notes.append(note_dict)

        # Prepare the content to be saved based on the selected format
        if file_format == 'txt':
            file_content = f"{title}\n{text}\n{meta}"
            file_extension = ".txt"
        elif file_format == 'json':
            file_content = json.dumps(note_dict)
            file_extension = ".json"
        elif file_format == 'csv':
            file_content = f"{title},{text},{meta}"
            file_extension = ".csv"
        elif file_format == 'xml':
            note_elem = ET.Element('note')
            title_elem = ET.SubElement(note_elem, 'title')
            title_elem.text = title
            text_elem = ET.SubElement(note_elem, 'text')
            text_elem.text = text
            meta_elem = ET.SubElement(note_elem, 'meta')
            meta_elem.text = meta
            file_content = ET.tostring(note_elem).decode()
            file_extension = ".xml"
        else:
            raise ValueError("Invalid file format specified")

        # Ask user for the file path to save
        file = filedialog.asksaveasfile(initialdir="C:\\Users\\sdemp\\Documents\\GitHub\\Courses\\INST326\\test_files",
                                        defaultextension=file_extension,
                                        filetypes=[(f"{file_format.upper()} file", f"*{file_extension}"),
                                                    ("All files", "*.*")])


    def load_note(self):
        if self.notes:
            note = self.notes[-1]
            self.snippet_title.delete(0, tk.END)
            self.snippet_title.insert(0, note['title'])
            self.snippet.delete('1.0', tk.END)
            self.snippet.insert('1.0', note['text'])

    def quit_note(self):
        self.destroy()


class MakeNote():
    def __init__(self, note_dict):
        self.title = note_dict.get("title", "")
        self.text = note_dict.get("text", "")
        self.metadata = note_dict.get("metadata", "")


main_window = StartScreen()
main_window.mainloop()

#10 notes:

#Title
#Encapsulation
#Text
#Encapsulation is another key pillar of OOP. In involves containing the methods involved with data and the data itself within a singular unit. This is what classes are. Classes contain attributes and methods which are then applied to whatever objects are created using the classes. These objects have clear properties and uses. 

#Title
#What is Object-Oriented Programming in Python?
#Text
#OOPs in python are a programming paradigm that uses objects and classes in programming. It aims to implement real-world entities like inheritance, polymorphisms, encapsulation, etc. in the programming.

#Title 
#Calling Parent class method
#Text
#Method overriding is an ability of any object-oriented programming language that allows a subclass or child class to provide a specific implementation of a method that is already provided by one of its super-classes or parent classes. Parent class methods can also be called within the overridden methods. This can generally be achieved by using Parent’s class methods can be called by using the Parent classname.method inside the overridden method.
    
#Title
#How to use datetime module
#Snippet Code
#import datetime as dt
## renames the datetime module to: dt
#now = dt.datetime.now()
#year = now.year
#month = now.month
#day_of_week = now.weekday()
#print(day_of_week)
#date_of_birth = dt.datetime(year=2003, month=10, day=24, hour=4)
#print(date_of_birth)

#Title
#Back To The Beginning: OOP
#Text
#In OOP, there are 3 main parts to it. Encapsulation which is collecting data to put it together, Polymorphism which is when objects are able to do different things, and Inheritance when objects can have same features.

#Title
#Inheritance in OOP
#Text
#Inheritance in OOP is like taking material from the older category and putting it into the new one. In other words, your reusing a code and just adding some new things to it. This is beneficial in OOP because it keeps everything organized.

#Title
#Function to check if a list is empty
#Text
#This function checks if a list is empty and returns a Boolean value (True or False).
#Snippet Code
#def is_list_empty(lst):
#    """Check if the given list is empty and return a Boolean result."""
#    return len(lst) == 0
## Example Usage
#my_list = []
#print(is_list_empty(my_list))  # Output: True

#Title 
#Exploring Nested Loops for Multi-dimensional Data Processing
#Text
#Nested loops are a powerful construct in Python that allow you to iterate over multi-dimensional data structures such as lists of lists or matrices. They enable you to traverse each element in a nested structure and perform operations efficiently. Nested loops are commonly used in tasks like matrix manipulation, image processing, and searching through multi-dimensional data.

#Title
#Data Cleaning with Python
#Snippet Code
#import pandas as pd
#data = pd.read_csv('your_dataset.csv')
## Dropping duplicate rows
#data = data.drop_duplicates()
## Handling missing values by filling them with mean
#data.fillna(data.mean(), inplace=True)
##Removing outliers 
#from scipy import stats
#data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
##Saving cleaned data into a new CSV file
#data.to_csv('cleaned_data.csv', index=False)

#Title
#RegEx
#Text
#Regular Expressions are very useful for data analysis using python. To import you would type "import re", this basically allows you easy search for terms. It could be used for the notebook application to search which specific note in a huge list has the information sequence that you need.
