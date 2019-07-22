import requests
from time import sleep, time

import psycopg2

from requests.exceptions import ProxyError

import os

from random import random

from ProxyList import ProxyList

import sys

appid = input('AppID: ') # CS:GO 730 TF2 440
table_name = input('Table Name: ') #tf2_item_names csgo_item_names

response = input(f'Are these the desired outputs? (Y/N)\nAppID: {appid}\nTable Name: {table_name}\n')

if response is not 'Y':
    sys.exit()

with open('../password.txt', 'r') as password_file:
    connection = psycopg2.connect(host='localhost',
                                 dbname='steammarket',
                                 user='postgres',
                                 password=password_file.read().rstrip(),
                                 port=7538)

cursor = connection.cursor()

ProxyList.pages_per_refresh = 1
proxies = ProxyList()

def main():
    global proxies, appid, table_name
    s = requests.Session()
    start = 0
    
    if proxies == None:
        sys.exit()
    proxy_dict = proxies.get_new_proxy_dict()
 
    while start < 24000:
        success = False

        while not success:
            try:
                r = s.get(f'https://steamcommunity.com/market/search/render/?query=&start={start}&count=100&norender=1&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid={appid}&category_{appid}_ItemSet[]=any&', proxies = proxy_dict).json()
                success = True
            except KeyboardInterrupt:
                s.close()
                connection.commit()
                cursor.close()
                connection.close()
                sys.exit()
            except Exception as e:
                print(e)
                proxy_dict = proxies.get_new_proxy_dict()

            try:
                for i in r['results']:
                    try:
                        cursor.execute(f'INSERT INTO table_name(name) VALUES (%s)', (i['name'],))
                    except Exception as e:
                        print(e)
                success = True
            except KeyboardInterrupt:
                s.close()
                connection.commit()
                cursor.close()
                connection.close()
                sys.exit()
            except:
                success = False
                proxy_dict = proxies.get_new_proxy_dict()

        start += 100
        
        print(start)
        
        try:
            sleep(5)
        except KeyboardInterrupt:
            break
        
        if start % 2_000 == 0:
            connection.commit()
            print('Committing...')
    print('Exiting...')
    s.close()
    connection.commit()
    cursor.close()
    connection.close()
    
main()