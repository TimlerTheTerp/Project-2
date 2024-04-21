# imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime # one module for working with dates and times

# The MainWindow class creates a custom GUI window based on the tkinter window (tk.Tk)
# It has an __init__() method, and three additional methods (new_note(), open_notebook(), and save_notebook())
# These methods correspond to new, open, and save buttons in the window.
# The new_note method calls the NoteForm class to create a new note form top level window.

#This class helps edit notes
class EditHistory:
    def __init__(self):
        self.edits = []

    def add_edit(self, timestamp, user=None, note_data=None):
        """Adds a new edit entry to the history."""
        self.edits.append({
            "timestamp": timestamp,
            "user": user,  # Optional for user tracking
            "note_data": note_data  # Optional for detailed changes captured (future extension)
        })

    def get_history(self):
        """Returns the complete edit history."""
        return self.edits
    
class MainWindow(tk.Tk):
    def __init__(self):  #initialize the main window
        super().__init__() # initialize it as a tkinter window
        
        self.geometry("600x400") # set the default window size
        self.title('Notebook') #set the default window title
        self.notebook = [] # initialize an attribute named 'notebook' as an empty list
        self.notes = []
        
        

        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note)
        self.new_button.place(x=100, y=350)  

        # Open Notebook Button
        self.open_button = tk.Button(self, text="Open Notebook", command=self.open_notebook)
        self.open_button.place(x=265, y=350) 

        # Save Notebook Button
        self.save_button = tk.Button(self, text="Save Notebook", command=self.save_notebook)
        self.save_button.place(x=450, y=350) 

             
    def new_note(self):
        note_window = NoteForm(self, self.notebook, self.notes)
        return None

    def open_notebook(self):
        filepath = filedialog.askopenfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")])


    def save_notebook(self):
        filepath = filedialog.asksaveasfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")])
       

    

# the NoteForm() class creates a Toplevel window that is a note form containing fields for
# data entry for title, text, link, and tags. It also calculates a meta field with date, time, and timezone
# the Noteform class has an __init__() method, and a submit() method that is called by a submit button
# the class may contain additional methods to perform tasks like calculating the metadata, for example
# the submit method calls the MakeNote class that transforms the the entered data into a new note object.

class NoteForm(tk.Toplevel):
    
    def __init__(self, master, notebook, notes): # initialize the new object
        super().__init__(master) # initialize it as a toplevel window

        #We make a list for the notes to be stored in order for the notebook can turn into objects
        self.notes = []

        self.geometry("600x300")
        self.new_button = tk.Button(self, text= "Submit Note",  font = ('Times New Roman', 15, 'bold'), command=self.submit)
        self.new_button.place(x= 275, y = 250)

        # Note
        actualnote = 'Please write something in python noteswise that is useful for your understanding'

        #Note title
        title_label = tk.Label(self, bg='light gray', text='Note Title:')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        text_label = tk.Label(self, bg='light gray', text='Note Text:')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        #Note Actual
        self.note_title = tk.Entry(self, width=80)
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title') # adds default text (useful during development)

        # create our note text field
        self.notebook = tk.Text(self, height=10, width=60)
        self.notebook.grid(padx=10, pady=10, row=2, column=1)
        self.notebook.insert('1.0', actualnote) # adds default text (useful during development)

    #Finds the date, time and timezone
    
    def metadata(self):
        #Used for calculation
        #Metadata
        #We need the data itself to calculate the stuff
        now = datetime.datetime.now() # gets the current date and time
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z") #Finds the timezone
    
    def save_file(self):
        #Metadata
        #We need the data itself to calculate the stuff
        now = datetime.datetime.now() # gets the current date and time
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z") #Finds the timezone
        title = self.note_title.get()
        text = self.notebook.get('1.0', 'end').strip('\n')
        meta = f'created {now}, {metadata_str}'
        note_dict = {'title':title, 'text':text, 'meta':meta}
        self.notes.append(note_dict)
        filetext=f"{title}\n{text}\n{meta}"


        file = filedialog.asksaveasfile(initialdir="C:\\Users\\sdemp\\Documents\\GitHub\\Courses\\INST326\\test_files",
                                            defaultextension=".txt", 
                                            filetypes=[("text file", ".txt"),
                                            ("all files", ".*")])
        file.write(filetext)
        file.close()
        
        
       

    
    def submit(self):

        note_dict = {
            "title": self.note_title.get(),
            "text": self.notebook.get("1.0", tk.END),
            "metadata": self.metadata()
        }

        new_note = MakeNote(note_dict)
        self.save_file()
        self.notes.append(new_note)
        
        
       

    
# The MakeNote class takes a dictionary containing the data entered into the form window,
# and transforms it into a new note object.
# At present the note objects have attributes but no methods.

class MakeNote():
    def __init__(self, note_dict):
        self.title = note_dict.get("title", "")
        self.text = note_dict.get("text", "")
        self.metadata = note_dict.get("metadata", "") 

    



# main execution

if __name__ == '__main__':
    
    main_window = MainWindow() # this creates a notebook / main window called main_window. You may change the name if you want

    main_window.mainloop()

# Print Notes
# This section of code is used to print the contents of the saved note files.

import os

# Specify the directory where the note files are saved
notes_directory = r"C:/Users/ahmed/Downloads"

# Get a list of all text files in the specified directory
note_files = [file for file in os.listdir(notes_directory) if file.endswith(".txt")]

# Iterate over each note file and print its contents
for i, note_file in enumerate(note_files, start=1):
    file_path = os.path.join(notes_directory, note_file)
    with open(file_path, "r") as file:
        note_content = file.read()
        title, text, meta = note_content.split("\n", 2)
        
        print(f"Note {i}:")
        print(f"Title: {title}")
        print(f"Text: {text}")
        print(f"Metadata: {meta}")
        print()
