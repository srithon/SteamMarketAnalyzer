import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.add_elements()
    def add_elements(self):
        self.quit_button = tk.Button(self, text='Hello World', command=self.quit)
        self.quit_button.grid()


main_window = tk.Tk()

app = Application(main_window)

main_window.mainloop()