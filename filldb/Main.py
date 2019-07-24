from Controller import Controller
import asyncio
import psycopg2
import sys

appid = input('AppID: ') # CS:GO 730 TF2 440
output_table_name = input('Output Table Name: ') #tf2_item_names csgo_item_names
input_table_name = input('Input Table Name: ')

response = input(f'\nAre these the desired outputs? (Y/N)\nAppID: {appid}\nOutput Table Name: {output_table_name}\nInput Table Name: {input_table_name}\n')

if response is not 'Y':
    sys.exit()

def main(num_workers, appid, output_table_name, input_table_name):
    with open('../password.txt', 'r') as password_file:
        connection = psycopg2.connect(host='localhost',
                                    dbname='steammarket',
                                    user='postgres',
                                    password=password_file.read().rstrip(),
                                    port=7538)
    controller = Controller(connection.cursor(), num_workers, appid, output_table_name, input_table_name)
    try:
        controller.start_workers()
    except KeyboardInterrupt:
        controller.shutdown()

main(3, appid, output_table_name, input_table_name)
