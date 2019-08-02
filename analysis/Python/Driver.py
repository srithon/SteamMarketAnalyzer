import Analysis
import psycopg2

table_name = 'tf2'

with open('password.txt', 'r') as password_file:
            connection = psycopg2.connect(host='localhost',
                                        dbname='steammarket',
                                        user='postgres',
                                        password=password_file.read().rstrip(),
                                        port=7538)

cursor = connection.cursor()
cursor.execute(f'SELECT DISTINCT name FROM {table_name}')
item_names = [item[0] for item in cursor.fetchall()]


for item in item_names:
    cursor.execute(f'SELECT volume, price FROM {table_name} WHERE name LIKE \'{item}\' ORDER BY time DESC')
    entries = cursor.fetchall()

    price = [entry[1] for entry in entries]
    volume = entries[0][0]

    print(f'{item}: {Analysis.suggested_action(volume, price)}')

# print (Analysis.suggested_action(8,[4, 8, 6, 4, 2, 0]))