from GUI import Application
import tkinter
from time import sleep, time
import sys
import threading
from datetime import datetime

def write_starting_filldb(appid, output_table, input_table, num_workers):
    with open('filldb_logs.txt', 'a+') as logs:
        logs.write(f'({num_workers}) {input_table}->{output_table} ({appid})...')

def finish_current_filldb():
    with open('filldb_logs.txt', 'a+') as logs:
        dt_object = datetime.fromtimestamp(time())
        logs.write(f'{dt_object}-DONE\n')

def check_finished():
    with open('filldb_logs.txt', 'r') as logs:
        return not logs.read().endswith('...')

def wait_for_finish():
    while not check_finished():
        print(f'Waiting... {sys.argv}')
        sleep(900)
        # 15 minutes

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Insufficient arguments')
    else:
        wait_for_finish()

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

        write_starting_filldb(appid, output_table, input_table, num_workers)

        app.filldb_frame.start_filling_db(on_complete=finish_current_filldb)
        root.mainloop()

    # self.num_workers_field.get_full(), self.appid_field.get_full(), self.output_table_name_field.get_full(), self.input_table_name_field.get_full())
else:
    print('ProgrammableGUI was imported?')