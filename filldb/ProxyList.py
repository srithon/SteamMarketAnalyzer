from selenium import webdriver
from random import random

from time import sleep, time

import os

import sys

import threading

import requests

class ProxyList:
    initial_url = 'https://free-proxy-list.net/anonymous-proxy.html'
    pages_per_refresh = 2

    def __init__(self):
        self.url = ProxyList.initial_url
        self.proxy_page = 1
        self.proxies = list()
        self.lock = threading.Lock()
        self.shutdown = False
        self.refresh_proxies()
    
    def refresh_proxies(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        
        print('Entered refresh_proxies')
        if self.shutdown:
            raise SystemExit()

        if self.url == 'https://proxy.rudnkh.me/txt':
            s = requests.Session()
            try:
                r = s.get(self.url, timeout=3.0)
                for proxy in r.text.split('\n'):
                    self.proxies.append(proxy.rstrip())
            except:
                return self.refresh_proxies()
            finally:
                self.url = 'https://us-proxy.org'
        else:
            while True:
                try:
                    driver = webdriver.Firefox(firefox_options=options)
                    break
                except Exception as e:
                    print(e)
            
            while True:
                try:
                    driver.get(self.url)
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
            
            # self.proxies.clear()

            for _ in range(ProxyList.pages_per_refresh):
                while current_page < self.proxy_page:
                    next_button_container = driver.find_element_by_css_selector('#proxylisttable_next')
                    next_button = next_button_container.find_element_by_css_selector('a:nth-child(1)')
                    sleep(0.5)
                    driver.execute_script('"window.scrollTo(0, document.body.scrollHeight);"')

                    if not 'disabled' in next_button_container.get_attribute('class'):
                        next_button.click()
                    else:
                        print(f'Changing proxy sites. Currently: {self.url}')
                        if self.url == 'https://us-proxy.org':
                            self.url = 'https://free-proxy-list.net/uk-proxy.html'
                        elif self.url == 'https://free-proxy-list.net/uk-proxy.html':
                            self.url = 'https://free-proxy-list.net/anonymous-proxy.html'
                        elif self.url == 'https://free-proxy-list.net/anonymous-proxy.html':
                            self.url = 'https://proxy.rudnkh.me/txt'
                        else:
                            self.url = 'https://us-proxy.org'
                        
                        self.proxy_page = 1
                        
                        return self.refresh_proxies()

                    current_page += 1
                
                proxies_body = driver.find_element_by_css_selector('#proxylisttable > tbody:nth-child(2)')
                proxies = proxies_body.find_elements_by_xpath('.//tr')
                print('{} proxies found in total'.format(len(proxies)))
                if 'dataTables_empty' in proxies[0].get_attribute('class'):
                    print('No Proxies Found!')
                    sys.exit()

                for proxy_element in proxies:
                    ip = proxy_element.find_element_by_xpath('.//td[1]').text
                    port = proxy_element.find_element_by_xpath('.//td[2]').text
                    print('{}:{}'.format(ip, port))
                    self.proxies.append('{}:{}'.format(ip, port))
                
                self.proxy_page += 1

        os.system('taskkill /f /im geckodriver.exe /T')
        print('Exited refresh_proxies')
        
    def get_new_proxy(self):
        print('{} proxies remaining'.format(len(self.proxies)))
        if not self.proxies:
            self.refresh_proxies()
        return self.proxies.pop(int(random() * len(self.proxies)))

    def synchronized_get_new_proxy_dict(self):
        print(f'Proxy request from Worker \'{threading.current_thread().name}\'')
        if self.shutdown:
            raise SystemExit()
        with self.lock:
            try:
                return self.get_new_proxy_dict()
            finally:
                print(f'Proxy request returned from Worker \'{threading.current_thread().name}\'')
    
    def get_new_proxy_dict(self):
        return ProxyList.get_proxy_dict(self.get_new_proxy())

    def get_proxy_dict(current_proxy):
        return { "https" : str(current_proxy) }

# Testing ProxyList refresh
if __name__ == '__main__':
    p = ProxyList()
    p.proxy_page = 4
    p.refresh_proxies()