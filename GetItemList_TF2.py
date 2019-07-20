import requests
from time import sleep, time

import psycopg2

from selenium import webdriver

from requests.exceptions import ProxyError

import os

from random import random

import sys

with open('password.txt', 'r') as password_file:
    connection = psycopg2.connect(host='localhost',
                                 dbname='steammarket',
                                 user='postgres',
                                 password=password_file.read().rstrip(),
                                 port=7538)

cursor = connection.cursor()

proxy_page = 1

proxy_url = 'https://free-proxy-list.net/anonymous-proxy.html'

proxies = list()

def get_proxies():
    global proxy_page, proxy_url

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Firefox(firefox_options=options)
    
    while True:
        try:
            driver.get(proxy_url)
            break
        except Exception as e:
            print(e)
        
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
        try:
            next_button.click()
        except:
            print('Changing proxy sites. Currently: {}'.format(proxy_url))
            if proxy_url == 'https://us-proxy.org':
                proxy_url = 'https://free-proxy-list.net/uk-proxy.html'
            elif proxy_url == 'https://free-proxy-list.net/uk-proxy.html':
                proxy_url = 'https://free-proxy-list.net/anonymous-proxy.html'
            else:
                proxy_url = 'https://us-proxy.org'
            
            proxy_page = 0
            
            return
        current_page += 1

    proxy_page += 1
    
    proxies_body = driver.find_element_by_css_selector('#proxylisttable > tbody:nth-child(2)')
    proxies = proxies_body.find_elements_by_xpath('.//tr')
    print('{} proxies found in total'.format(len(proxies)))
    if len(proxies) == 0:
          print('No Proxies Found!')
          return None
    proxy_list = list()
    for proxy_element in proxies:
        ip = proxy_element.find_element_by_xpath('.//td[1]').text
        port = proxy_element.find_element_by_xpath('.//td[2]').text
        print('{}:{}'.format(ip, port))
        proxy_list.append('{}:{}'.format(ip, port))
    os.system('taskkill /f /im geckodriver.exe /T')
    return proxy_list
    
def get_new_proxy():
    global proxies
    print('{} proxies remaining'.format(len(proxies)))
    if len(proxies) == 0:
        proxies = get_proxies()
    return proxies.pop(int(random() * len(proxies)))
    

def get_proxy_dict(current_proxy):
    return { "https" : str(current_proxy) }


def main():
    global proxies
    s = requests.Session()
    start = 0
    
    proxies = get_proxies()
    if proxies == None:
        sys.exit()
    proxy_dict = get_proxy_dict(get_new_proxy())
 
    while start < 24000:
        success = False

        while not success:
            try:
                r = s.get(f'https://steamcommunity.com/market/search/render/?query=&start={start}&count=100&norender=1&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid=440&category_440_ItemSet[]=any&', proxies = proxy_dict).json()
                success = True
            except KeyboardInterrupt:
                s.close()
                connection.commit()
                cursor.close()
                connection.close()
                sys.exit()
            except Exception as e:
                print(e)
                proxy_dict = get_proxy_dict(get_new_proxy())

            try:
                for i in r['results']:
                    try:
                        cursor.execute('INSERT INTO tf2_item_names(name) VALUES (%s)', (i['name'],))
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
                proxy_dict = get_proxy_dict(get_new_proxy())

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