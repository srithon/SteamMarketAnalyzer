import Analysis
import psycopg2

table_name = 'csgo'

with open('C:/Development/SteamMarketAnalyzer/password.txt', 'r') as password_file:
            connection = psycopg2.connect(host='localhost',
                                        dbname='steammarket',
                                        user='postgres',
                                        password=password_file.read().rstrip(),
                                        port=7538)

cursor = connection.cursor()
cursor.execute(f'SELECT DISTINCT name FROM {table_name}')
item_names = [item[0] for item in cursor.fetchall()]


for item in item_names:
    cursor.execute(f'SELECT volume, price FROM {table_name} WHERE name=%s ORDER BY time DESC', (item,))
    entries = cursor.fetchall()

    price = [entry[1] for entry in entries]
    volume = entries[0][0]

    action = Analysis.suggested_action(volume, price)

    if action != Analysis.Action.IGNORE:
        print(f'{item}: {action}')

# print (Analysis.suggested_action(8,[4, 8, 6, 4, 2, 0]))