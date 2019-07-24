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
        # num_workers, appid, output_table_name, input_table_name

    def populate(self):
        self.start_button = tk.Button(self, text='Start', command=self.start_analysis)
        self.start_button.grid(padx=50, pady=50)

        self.num_workers_field = HintTextEntry(self, 'Number of Workers', grid_args={'padx':50,'pady':20})
        self.appid_field = HintTextEntry(self, 'App ID', grid_args={'padx':50,'pady':20})
        self.output_table_name_field = HintTextEntry(self, 'Output Table', grid_args={'padx':50,'pady':20})
        self.input_table_name_field = HintTextEntry(self, 'Input Table', grid_args={'padx':50,'pady':20})
    
    def start_analysis(self):
        print('Start filldb?')
        print(self.num_workers_field.get(0))
        print(self.appid_field.get(0))
        print(self.output_table_name_field.get(0))
        print(self.input_table_name_field.get(0))

class HintTextEntry(tk.Text):
    def __init__(self, master, hint_text, grid_args=None):
        tk.Text.__init__(self, master)
        self.hint_text = hint_text
        self.insert('1.0', hint_text)
        self.bind('<Enter>', self.handle_enter)
        self.bind('<Leave>', self.handle_leave)

        if grid_args is not None:
            self.grid(**grid_args)
    
    def handle_enter(self, event):
        print(self.get(1.0,'end'))
        print(self.hint_text)
        if self.get(1.0,'end').rstrip() == self.hint_text:
            self.delete(1.0, 'end')

    def handle_leave(self, event):
        if not self.get(1.0, 'end').rstrip():
            self.insert(1.0, self.hint_text)

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

class Logs(tk.Text):
    def __init__(self, master):
        tk.Text.__init__(self, master)
        self.grid()
    
    def append(self, text):
        self.insert('end', text)

root = tk.Tk()
app = Application(root)
root.mainloop()