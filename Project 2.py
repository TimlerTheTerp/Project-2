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

                                                                                           *******PROJECT3*******
# imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("600x500")  # Increased window height
        self.title('Notebook')
        self.configure(bg='#98FB98')  # Light green background color
        self.notebook = []
        self.notes = []
        self.snippets = []
        
        button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Arial', 12, 'bold')}
        
        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note, **button_style)
        self.new_button.pack(pady=30)  # Increased vertical padding

        # Open Notebook Button
        self.open_button = tk.Button(self, text="Open Notebook", command=self.open_notebook, **button_style)
        self.open_button.pack(pady=30)  # Increased vertical padding

        # Save Notebook Button
        self.save_button = tk.Button(self, text="Save Notebook", command=self.save_notebook, **button_style)
        self.save_button.pack(pady=30)  # Increased vertical padding
             
    def new_note(self):
        note_window = NoteForm(self, self.notebook, self.notes, self.snippets)
        return None

    def open_notebook(self):
        filepath = filedialog.askopenfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")])
        
        if filepath:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                
                self.notes = []
                self.snippets = []
                
                i = 0
                while i < len(lines):
                    if i + 4 < len(lines):
                        title = lines[i].strip()
                        text = lines[i+1].strip()
                        meta = lines[i+2].strip()
                        snippet_title = lines[i+3].strip()
                        snippet_code = lines[i+4].strip()
                        
                        note_dict = {'title': title, 'text': text, 'meta': meta}
                        self.notes.append(note_dict)
                        
                        snippet = Snippet(snippet_title, snippet_code)
                        self.snippets.append(snippet)
                        
                        i += 5
                    else:
                        break
            
            note_window = NoteForm(self, self.notebook, self.notes, self.snippets)
            note_window.load_note()

    def save_notebook(self):
        filepath = filedialog.asksaveasfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")])

class NoteForm(tk.Toplevel):
    
    def __init__(self, master, notebook, notes, snippets):
        super().__init__(master)

        self.notes = notes
        self.snippets = snippets

        self.geometry("600x500")
        self.configure(bg='#98FB98')  # Light green background color

        actualnote = 'Please write something in python noteswise that is useful for your understanding'

        # Note title
        title_label = tk.Label(self, bg='#98FB98', text='Note Title:', font=('Courier', 12, 'bold'), fg='black')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        # Note text
        text_label = tk.Label(self, bg='#98FB98', text='Note Text:', font=('Courier', 12, 'bold'), fg='black')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.note_title = tk.Entry(self, width=60, font=('Courier', 12))
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title')

        self.notebook = tk.Text(self, height=10, width=40, font=('Courier', 12))
        self.notebook.grid(padx=10, pady=10, row=2, column=1, sticky='w')
        self.notebook.insert('1.0', actualnote)

        # Snippet Fields
        snippet_title_label = tk.Label(self, bg='#98FB98', text='Snippet Title:', font=('Courier', 12, 'bold'), fg='black')
        snippet_title_label.grid(padx=10, pady=10, row=3, column=0, sticky='e')
        self.snippet_title = tk.Entry(self, width=60, font=('Courier', 12))
        self.snippet_title.grid(padx=10, pady=10, row=3, column=1, sticky='w')

        snippet_code_label = tk.Label(self, bg='#98FB98', text='Snippet Code:', font=('Courier', 12, 'bold'), fg='black')
        snippet_code_label.grid(padx=10, pady=10, row=4, column=0, sticky='e')
        self.snippet_code = tk.Text(self, height=10, width=40, font=('Courier', 12))
        self.snippet_code.grid(padx=10, pady=10, row=4, column=1, sticky='w')

        # Submit Note Button
        self.submit_button = tk.Button(self, text="Submit Note", command=self.submit, font=('Courier', 12, 'bold'), bg='purple', fg='white')
        self.submit_button.grid(row=6, column=1, pady=10)

    def metadata(self):
        now = datetime.datetime.now()
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        return metadata_str
    
    def save_file(self):
        now = datetime.datetime.now()
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        title = self.note_title.get()
        text = self.notebook.get('1.0', 'end').strip('\n')
        meta = f'created {now}, {metadata_str}'
        note_dict = {'title':title, 'text':text, 'meta':meta}
        self.notes.append(note_dict)
        
        snippet_title = self.snippet_title.get()
        snippet_code = self.snippet_code.get('1.0', 'end').strip('\n')
        
        filetext=f"{title}\n{text}\n{meta}\n{snippet_title}\n{snippet_code}"

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
        self.notes.append(new_note)

        snippet_title = self.snippet_title.get()
        snippet_code = self.snippet_code.get("1.0", tk.END)

        new_snippet = Snippet(snippet_title, snippet_code)
        self.snippets.append(new_snippet)

        self.save_file()

    def load_note(self):
        if self.notes:
            note = self.notes[-1]
            self.note_title.delete(0, tk.END)
            self.note_title.insert(0, note['title'])
            self.notebook.delete('1.0', tk.END)
            self.notebook.insert('1.0', note['text'])

        if self.snippets:
            snippet = self.snippets[-1]
            self.snippet_title.delete(0, tk.END)
            self.snippet_title.insert(0, snippet.title)
            self.snippet_code.delete('1.0', tk.END)
            self.snippet_code.insert('1.0', snippet.code)

class MakeNote():
    def __init__(self, note_dict):
        self.title = note_dict.get("title", "")
        self.text = note_dict.get("text", "")
        self.metadata = note_dict.get("metadata", "") 

class Snippet:
    def __init__(self, title, code, created_at=None, updated_at=None):
        self.title = title
        self.code = code
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.updated_at = updated_at if updated_at else self.created_at

    def update_code(self, new_code):
        self.code = new_code
        self.updated_at = datetime.datetime.now()

if __name__ == '__main__':
    
    main_window = MainWindow()

    main_window.mainloop()
