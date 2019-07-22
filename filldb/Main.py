from Controller import Controller
import asyncio
import psycopg2
import sys

with open('../password.txt', 'r') as password_file:
    connection = psycopg2.connect(host='localhost',
                                 dbname='steammarket',
                                 user='postgres',
                                 password=password_file.read().rstrip(),
                                 port=7538)

def main():
    controller = Controller(connection.cursor(), 3)
    try:
        controller.start_workers()
    except KeyboardInterrupt:
        controller.shutdown()

main()
