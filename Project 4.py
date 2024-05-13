# imports
import os
import tkinter as tk
from tkinter import Label
from tkinter import ttk
from tkinter import filedialog
import datetime

#Tyler Vu, I was in charge of making the start screen.
#We made a start screen which prompts the user to welcome the user to the screen.
#Thara Le, I was in charge of making design/aesthetic changes.
#I edited the colors, geometry, added borders, and moved around buttons to look more appealing to the user.
class StartScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Georgia', 12, 'bold')}

        #Frame for title
        f = tk.Frame(self, bg='purple', bd=5)
        f.place(x=220, y=100)

        #Title
        l = Label(f, text="  Welcome to the Note Creating Machine!  ", font=("Georgia", 16))
        l.pack()

        #Date and Time Label
        self.date_time_label = Label(self, text="", font=("Georgia", 12), bg='#efd9fd')
        self.date_time_label.place(x=10, y=10)

        #Start button
        self.start_button = tk.Button(self, text="Begin", command=self.MainSelection, **self.button_style)
        self.start_button.place(x=250, y=250)

        #Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.Quit, **self.button_style)
        self.quit_button.place(x=530, y=250)

    #We made the opening where the user gets to open the maker move
    def MainSelection(self):
        self.destroy()  # Close the StartScreen window
        start = MainWindow()  # Create an instance of MainWindow
        start.mainloop()  # Run the MainWindow loop

    #Made a quit button as well
    def Quit(self):
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title('Notebook')
        self.configure(bg='#efd9fd')
        self.notebook = []
        self.notes = []

        self.button_style = {'bg': 'purple', 'fg': 'white', 'font': ('Georgia', 12, 'bold')}

        # Date and Time Label
        self.date_time_label = Label(self, text="", font=("Georgia", 12), bg='#efd9fd')
        self.date_time_label.place(x=10, y=10)
        self.update_date_time_label()  # Update the date and time label

        # New Note Button
        self.new_button = tk.Button(self, text="New Note", command=self.new_note, **self.button_style)
        self.new_button.pack(pady=(100, 30))

        # Open Note Button
        self.open_button = tk.Button(self, text="Open Note", command=self.open_notebook, **self.button_style)
        self.open_button.pack(pady=30)

        # Quit Notebook Button
        self.quit_button = tk.Button(self, text="Quit Notebook", command=self.quit_app, **self.button_style)
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


class NoteForm(tk.Toplevel):
    def __init__(self, master, notebook, notes, button_style):
        super().__init__(master)

        self.notes = notes

        self.geometry("800x400")
        self.configure(bg='#efd9fd')

        # Snippet Title
        title_label = tk.Label(self, bg='#efd9fd', text='Snippet Title:', font=('Courier', 12, 'bold'), fg='black')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        # Snippet, we added a scrollbar
        text_label = tk.Label(self, bg='#efd9fd', text='Snippet:', font=('Courier', 12, 'bold'), fg='black')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.snippet_title = tk.Entry(self, width=40, font=('Courier', 12))
        self.snippet_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.snippet_title.insert(0, 'Untitled')
        
        snippet_frame = tk.Frame(self, bg='#efd9fd')  # Frame to contain the text widget and scrollbar
        snippet_frame.grid(row=2, column=1, sticky='w')

        self.snippet = tk.Text(snippet_frame, height=10, width=60, font=('Courier', 12))
        self.snippet.grid(row=0, column=0, sticky='w')

        scrollbar = tk.Scrollbar(snippet_frame, orient='vertical', command=self.snippet.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.snippet.config(yscrollcommand=scrollbar.set)

        buttons_frame = tk.Frame(self, bg='#efd9fd')
        buttons_frame.grid(row=6, column=1)


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
        now = datetime.datetime.now()
        title = self.snippet_title.get()
        text = self.snippet.get('1.0', 'end').strip('\n')
        meta = f'created {now}'
        note_dict = {'title': title, 'text': text, 'meta': meta}
        self.notes.append(note_dict)

        filetext = f"{title}\n{text}\n{meta}"

        file = filedialog.asksaveasfile(initialdir="C:\\Users\\sdemp\\Documents\\GitHub\\Courses\\INST326\\test_files",
                                         defaultextension=".txt",
                                         filetypes=[("text file", ".txt"),
                                                    ("all files", ".*")])
        if file:
            file.write(filetext)
            file.close()

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
