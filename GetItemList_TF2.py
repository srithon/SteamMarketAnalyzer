import requests
from time import sleep, time

import psycopg2

with open('password.txt', 'r') as password_file:
    connection = psycopg2.connect(host='localhost',
                                 dbname='steammarket',
                                 user='postgres',
                                 password=password_file.read().rstrip(),
                                 port=7538)

cursor = connection.cursor()


def main():
    s = requests.Session()
    start = 10000
    while start < 24000:
        success = False

        while not success:
            try:
                r = s.get(f'https://steamcommunity.com/market/search/render/?query=&start={start}&count=100&norender=1&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid=440&category_440_ItemSet[]=any&').json()
                success = True
            except Exception as e:
                print(e)

        for i in r['results']:
            try:
                cursor.execute('INSERT INTO tf2_item_names(name) VALUES (%s)', (i['name'],))
            except Exception as e:
                print(e)

        start += 100
        
        print(start)
        
        try:
            sleep(5)
        except KeyboardInterrupt:
            break
        
        if start % 5_000 == 0:
            connection.commit()
            print('Committing...')
    print('Exiting...')
    s.close()
    connection.commit()
    cursor.close()
    connection.close()
    
main()