from GUI import Application
import tkinter
from time import sleep
import sys
import threading

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Insufficient arguments')
    else:
        
        root = tkinter.Tk()
        app = Application(root)

        sleep(3.0)

        appid = sys.argv[1]
        output_table = sys.argv[2]
        input_table = sys.argv[3]
        num_workers = sys.argv[4] if len(sys.argv) > 4 else 3
        
        app.switch_to_filldb()

        app.filldb_frame.num_workers_field.delete(1.0, 'end')
        app.filldb_frame.num_workers_field.insert('end', num_workers)
        app.filldb_frame.output_table_name_field.delete(1.0, 'end')
        app.filldb_frame.output_table_name_field.insert('end', output_table)
        app.filldb_frame.input_table_name_field.delete(1.0, 'end')
        app.filldb_frame.input_table_name_field.insert('end', input_table)
        app.filldb_frame.appid_field.delete(1.0, 'end')
        app.filldb_frame.appid_field.insert('end', appid)

        app.filldb_frame.start_filling_db()
        root.mainloop()

    # self.num_workers_field.get_full(), self.appid_field.get_full(), self.output_table_name_field.get_full(), self.input_table_name_field.get_full())
else:
    print('ProgrammableGUI was imported?')