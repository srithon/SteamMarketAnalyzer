import requests

import psycopg2

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector.errors import IntegrityError

from time import sleep, time

import math

import logging

import os

import json

import sys

from selenium import webdriver

from random import random

from requests.exceptions import ProxyError

from json.decoder import JSONDecodeError




delay = 2.5




verbose = True




log_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s\t%(message)s',
                                  datefmt='%H:%M:%S')

log_handler = logging.FileHandler(filename='filldatabase_tf2.log')
log_handler.setFormatter(log_formatter)

log_handler.setLevel(logging.DEBUG)

#  logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('root_logger')

#  logging.getLogger('')
logger.addHandler(log_handler)

logger.setLevel(logging.DEBUG)

logger.info('Starting script...')

with open('password.txt', 'r') as password_file:
    connection = psycopg2.connect(host='localhost',
                                 dbname='steammarket',
                                 user='postgres',
                                 password=password_file.read().rstrip(),
                                 port=7538)

cursor = connection.cursor()

mysql_connection = mysql.connector.connect(host='localhost',
                             database='tf2metalvsmarketprice',
                             user='root',
                             password='LrD3FZGUz5JXy5c')

mysql_cursor = mysql_connection.cursor()

proxy_page = 1

init_time = time()

s = None

proxies = list()

items = list()

def save_lists():
    connection.commit()


def get_proxies():
    global proxy_page

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Firefox(firefox_options=options)
    
    while True:
        try:
            driver.get('https://us-proxy.org')
            break
        except Exception as e:
            print(e)
            logger.error(e)
        
    search = driver.find_element_by_css_selector('#proxylisttable_filter > label:nth-child(1) > input:nth-child(1)')
    search.send_keys('elite proxy')
    sort_by_https = driver.find_element_by_css_selector('th.sorting:nth-child(7)') 
    sort_by_https.click()
    sleep(0.5)
    sort_by_https.click()
    sleep(1.0)

    current_page = 1

    while current_page < proxy_page:
        next_button = driver.find_element_by_css_selector('#proxylisttable_next > a:nth-child(1)')
        sleep(0.5)
        driver.execute_script('"window.scrollTo(0, document.body.scrollHeight);"')
        next_button.click()
        current_page += 1

    proxy_page += 1
    
    proxies_body = driver.find_element_by_css_selector('#proxylisttable > tbody:nth-child(2)')
    proxies = proxies_body.find_elements_by_xpath('.//tr')
    print('{} proxies found in total'.format(len(proxies)))
    if len(proxies) == 0:
          print('No Proxies Found!')
          logger.e('No Proxies Found!')
          return None
    proxy_list = list()
    for proxy_element in proxies:
        ip = proxy_element.find_element_by_xpath('.//td[1]').text
        port = proxy_element.find_element_by_xpath('.//td[2]').text
        print('{}:{}'.format(ip, port))
        logger.info('{}:{}'.format(ip, port))
        proxy_list.append('{}:{}'.format(ip, port))
    os.system('taskkill /f /im geckodriver.exe /T')
    return proxy_list
    
def get_new_proxy():
    global proxies
    print('{} proxies remaining'.format(len(proxies)))
    if len(proxies) == 0:
        logger.debug('Used up all proxies! Refreshing')
        proxies = get_proxies()
    return proxies.pop(int(random() * len(proxies)))
    

def get_proxy_dict(current_proxy):
    return { "https" : str(current_proxy) }


def refresh_database():
    global items
    # cursor.execute('SELECT ItemName FROM `item list steam market tf2 tf2` WHERE PriceValue IS NULL ORDER BY PointValue ASC')
    mysql_cursor.execute('SELECT name FROM `tf2 metal vs steam market prices` WHERE realPrice IS NOT NULL ORDER BY metalPrice ASC')
    items.clear()
    items = [item[0] for item in mysql_cursor.fetchall()]

def close_mysql_connection():
    if mysql_connection.is_connected():
        mysql_connection.commit()
        mysql_connection.close()
        mysql_cursor.close()

def shutdown():
    global s
    
    try:
        s.close()
    except Exception as e:
        print(e)

    try:
        connection.commit()
        connection.close()
        cursor.close()
        print('Committed and closed')
    except Exception as e:
        print(e)

    final_time = time()
    print('Time passed - {}'.format(final_time - init_time))
    logger.info('Time passed - {}'.format(final_time - init_time))
    logger.info('Counter = {}'.format(count))

    s = None

    log_handler.close()

    sys.exit()


def main(delay):
    global init_time, items, proxies, s
    proxies = get_proxies()
    if proxies == None:
        logger.error('No proxies found!')
        sys.exit()
    proxy_dict = get_proxy_dict(get_new_proxy())
    s = requests.Session()
    init_time = time()
    counter = 0
    try:
        broken = True

        refresh_database()
        close_mysql_connection()
        
        failures = 0
        
        while broken:
            broken = False
            item = items[0]
            while item != None:
                item = items[0]

                if verbose:
                    print(item)

                try:
                    r = s.get('https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name=' + item, proxies = proxy_dict)
                    first_time = True
                    
                    if r.text == 'null':
                        print('null in source')
                        logger.error('NULL IN SOURCE')
                        logger.info('Counter = {}'.format(counter))
                        proxy_dict = get_proxy_dict(get_new_proxy())
                        continue
                    
                    try:
                        lowest_price = None
                        
                        try:
                            json = r.json()
                        except JSONDecodeError as b:
                            print(b)
                            logger.error(b)
                            proxy_dict = get_proxy_dict(get_new_proxy())
                            continue
                        
                        try:
                            lowest_price = (json['lowest_price'])[1:]
                        except KeyError as e:
                            print(e)
                            logger.error(e)
                            try:
                                lowest_price = (json['median_price'])[1:]
                            except:
                                print('Gave up on {}'.format(item))
                                logger.error('Gave up on {}'.format(item))
                                del items[:1]
                                item = items[0]
                                sleep(delay)
                                continue
                        price = math.floor(float(lowest_price) * 100)
                        query = 'INSERT INTO tf2(time, name, price, volume) VALUES (NOW(), %s, %s, %s)'
                        
                        try:
                            volume = json['volume']
                        except KeyError as e:
                            volume = 0

                        if verbose:
                            print(query % (item, price, volume))

                        cursor.execute(query, (item, price, volume))
                        failures = 0
                    except Exception as e:
                        try:
                            print('Error in {}'.format(query))
                        except:
                            pass
                        print(e)
                        logger.error(e)
                        sleep(delay)

                        if random() < 0.125:
                            del items[:1]
                            item = items[0]
                            logger.d('Skipping this garbage')
                            print('Skipping')

                        continue
                except KeyboardInterrupt as e:
                    print('Exiting...')
                    shutdown()
                except requests.exceptions.ProxyError as e:
                    print('Proxy Error')
                    logger.error(e)
                    proxy_dict = get_proxy_dict(get_new_proxy())
                    sleep(2)
                    continue
                except:
                    logger.debug('Failed to get response. Retrying. item = {}'.format(item))

                    if verbose:
                        print('Failed to get response. Retrying. item = {}'.format(item))

                    sleep(delay)
                    init_time += delay
                    
                    if failures > 3:
                        proxy_dict = get_proxy_dict(get_new_proxy())
                        print('4 failures; switching proxies')
                        failures = 0
                    else:
                        failures += 1
                    
                    continue
                try:
                    sleep(delay)
                    counter += 1
                    del items[:1]
                    item = items[0]
                    if verbose:
                        print('Completed iteration #{}'.format(counter))
                    if (counter % 10 == 0):
                        print('Saving lists...')
                        logger.info('Saving lists...')
                        save_lists()
                        broken = True
                        break
                except KeyboardInterrupt:
                    print('Exiting...')
                    shutdown()
            
    except Exception as e:
        print(e)
    return counter

last_count = 0

try:
    count = main(delay)
except Exception as e:
    print(e)
finally:
    shutdown()

