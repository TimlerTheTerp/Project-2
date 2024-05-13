# imports
import os
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
import datetime

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
        l = Label(f, text="  Welcome to the Note Creating Machine!  ", font=("Arial", 16), fg='white')
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

    def MainSelection(self):
        self.destroy()  # Close the StartScreen window
        start = MainWindow()  # Create an instance of MainWindow
        start.mainloop()  # Run the MainWindow loop

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
