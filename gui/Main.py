import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid()
        self.main_frame = MainFrame(self)
        self.analysis_frame = AnalysisFrame(self)
        self.filldb_frame = FillDBFrame(self)
        self.main_frame.tkraise()
    
    def switch_to_analysis(self):
        self.analysis_frame.tkraise()
    
    def switch_to_filldb(self):
        self.filldb_frame.tkraise()

class AnalysisFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.populate()
        self.grid(column=0, row=0, sticky='nsew')

    def populate(self):
        self.start_button = tk.Button(self, text='Start', command=self.start_analysis)
        self.start_button.grid(padx=50, pady=50)
    
    def start_analysis(self):
        print('Start analysis....')
    

class FillDBFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.populate()
        self.grid(column=0, row=0, sticky='nsew')

    def populate(self):
        self.start_button = tk.Button(self, text='Start', command=self.start_analysis)
        self.start_button.grid(padx=50, pady=50)
    
    def start_analysis(self):
        print('Start filldb....')

class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.populate()
    
    def populate(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit, activebackground='#A05')
        self.quit_button.grid(padx=50, pady=50)
        self.filldb_button = tk.Button(self, text='Fill DB', command=self.master.switch_to_filldb)
        self.filldb_button.grid(padx=50, pady=50)
        self.analysis_button = tk.Button(self, text='Analysis', command=self.master.switch_to_analysis)
        self.analysis_button.grid(padx=50, pady=50)

root = tk.Tk()
app = Application(root)
root.mainloop()