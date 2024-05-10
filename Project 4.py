# imports
import os
import tkinter as tk
from tkinter import Label
from tkinter import ttk
from tkinter import filedialog
import datetime

#Start Screen, 
class StartScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Georgia', 12, 'bold')}

        #Frame for title
        f = tk.Frame(self, bg = 'purple', bd = 5)
        f.place(x = 220, y = 100)

        #Title
        l = Label(f, text="  Welcome to the Note Creating Machine!  ", font=("Georgia", 16))
        l.pack()

        #Start button
        self.start_button = tk.Button(self, text="Begin", command=self.MainSelection, **self.button_style)
        self.start_button.place(x = 250, y = 250)  # Increase the top padding to start lower

        #Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.Quit, **self.button_style)
        self.quit_button.place(x = 530, y = 250)  # Increase the top padding to start lower

    #This gives the function that the user takes them to the real application
    def MainSelection(self):
            start = MainWindow()
            return None
    
    def Quit(self):
            self.destroy()

#Real Window       
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')
        self.notebook = []
        self.notes = []

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Georgia', 12, 'bold')}

        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note, **self.button_style)
        self.new_button.pack(pady=(100, 30))  # Increase the top padding to start lower
        # Open Note Button
        self.open_button = tk.Button(self, text="Open Note", command=self.open_notebook, **self.button_style)
        self.open_button.pack(pady=30)
        # Quit Notebook Button
        self.quit_button = tk.Button(self, text="Quit Notebook", command=lambda:[self.destroy,StartScreen.quit(self)], **self.button_style) 
        #the second command is to destroy both the startscreen as well when the quit button is pressed on mainwindow
        self.quit_button.pack(pady=30)

    def new_note(self):
        note_window = NoteForm(self, self.notebook, self.notes, self.button_style)
        return None

    def open_notebook(self):
        filepath = filedialog.askopenfilename(initialdir=os.path.normpath(r"C:\Users\timle\OneDrive\Documents\PythonNotebook").encode('utf-8'),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")])

        if filepath:
            with open(filepath, 'r') as file:
                file_contents = file.read()
                note_chunks = file_contents.split('\n\n')  # Split the file contents based on empty lines

                self.notes = []

                for chunk in note_chunks:
                    lines = chunk.strip().split('\n')  # Split each chunk into lines
                    if len(lines) >= 3:
                        title = lines[0]
                        text = '\n'.join(lines[1:-1])  # Join the lines for the note text
                        meta = lines[-1]

                        note_dict = {'title': title, 'text': text, 'meta': meta}
                        self.notes.append(note_dict)
                    else:
                        # Handle the case when the chunk does not have the expected format
                        # You can log an error message or skip the chunk
                        print(f"Skipping invalid note chunk: {chunk}")

            note_window = NoteForm(self, self.notebook, self.notes, self.button_style)
            note_window.load_note()

#Note creator
class NoteForm(tk.Toplevel):

    def __init__(self, master, notebook, notes, button_style):
        super().__init__(master)

        self.notes = notes

        self.geometry("800x400")  # Increased window size
        self.configure(bg='#efd9fd')  # Light green background color = #98FB98

        actualnote = 'Please write something in python that is useful for your\nunderstanding.'

        # Snippet Title
        title_label = tk.Label(self, bg='#efd9fd', text='Snippet Title:', font=('Courier', 12, 'bold'), fg='black')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        # Snippet
        text_label = tk.Label(self, bg='#efd9fd', text='Snippet:', font=('Courier', 12, 'bold'), fg='black')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.snippet_title = tk.Entry(self, width=40, font=('Courier', 12))
        self.snippet_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.snippet_title.insert(0, 'Untitled')

        self.snippet = tk.Text(self, height=10, width=60, font=('Courier', 12))
        self.snippet.grid(padx=10, pady=10, row=2, column=1, sticky='w')
        self.snippet.insert('1.0', actualnote)

        buttons_frame = tk.Frame(self, bg = '#efd9fd')
        buttons_frame.grid(row = 6, column = 1)
        # Submit Note Button
        self.submit_button = tk.Button(buttons_frame, text="Submit Note", command=self.submit, **button_style)
        self.submit_button.grid(row=0, column=0, padx = 50)

        #quit note button
        self.quit_button = tk.Button(buttons_frame, text = "Quit Note", command = self.quit_note, **button_style)
        self.quit_button.grid(row = 0, column = 1, padx = 50)

    def metadata(self):
        now = datetime.datetime.now()
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        return metadata_str

    def save_file(self):
        now = datetime.datetime.now()
        metadata_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        title = self.snippet_title.get()
        text = self.snippet.get('1.0', 'end').strip('\n')
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
            "title": self.snippet_title.get(),
            "text": self.snippet.get("1.0", tk.END),
            "metadata": self.metadata()
        }

        new_note = MakeNote(note_dict)
        self.notes.append(new_note)

        self.save_file()

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

#commented out so that the mainwindow doesn't open after quitting the start screen
#if __name__ == '__main__':

    #main_window = MainWindow()

    #main_window.mainloop()
