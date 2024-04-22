# imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("800x500")  
        self.title('Notebook')
        self.configure(bg='#98FB98')  
        self.notebook = []
        self.notes = []
        self.snippets = []
        
        button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Arial', 12, 'bold')}
        
        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note, **button_style)
        self.new_button.pack(pady=30)  
        # Open Notebook Button
        self.open_button = tk.Button(self, text="Open Notebook", command=self.open_notebook, **button_style)
        self.open_button.pack(pady=30)  
        # Save Notebook Button
        self.save_button = tk.Button(self, text="Save Notebook", command=self.save_notebook, **button_style)
        self.save_button.pack(pady=30)  
             
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

        self.geometry("800x600")  # Increased window size
        self.configure(bg='#98FB98')  # Light green background color

        actualnote = 'Please write something in python  that is useful for your understanding'

        # Note title
        title_label = tk.Label(self, bg='#98FB98', text='Note Title:', font=('Courier', 12, 'bold'), fg='black')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        # Note text
        text_label = tk.Label(self, bg='#98FB98', text='Note Text:', font=('Courier', 12, 'bold'), fg='black')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.note_title = tk.Entry(self, width=40, font=('Courier', 12))  
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title')

        self.notebook = tk.Text(self, height=10, width=60, font=('Courier', 12)) 
        self.notebook.grid(padx=10, pady=10, row=2, column=1, sticky='w')
        self.notebook.insert('1.0', actualnote)

        # Snippet Fields
        snippet_title_label = tk.Label(self, bg='#98FB98', text='Snippet Title:', font=('Courier', 12, 'bold'), fg='black')
        snippet_title_label.grid(padx=10, pady=10, row=3, column=0, sticky='e')
        self.snippet_title = tk.Entry(self, width=40, font=('Courier', 12))  
        self.snippet_title.grid(padx=10, pady=10, row=3, column=1, sticky='w')

        snippet_code_label = tk.Label(self, bg='#98FB98', text='Snippet Code:', font=('Courier', 12, 'bold'), fg='black')
        snippet_code_label.grid(padx=10, pady=10, row=4, column=0, sticky='e')
        self.snippet_code = tk.Text(self, height=10, width=60, font=('Courier', 12))  
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