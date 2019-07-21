from selenium import webdriver
from random import random

from time import sleep, time

import os

import threading

class ProxyList:
    initial_url = 'https://free-proxy-list.net/anonymous-proxy.html'

    def __init__(self):
        self.url = ProxyList.initial_url
        self.proxy_page = 0
        self.proxies = list()
        self.refresh_proxies()
        self.lock = threading.Lock()
    
    def refresh_proxies(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        
        driver = webdriver.Firefox(firefox_options=options)
        
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

        while current_page < self.proxy_page:
            next_button = driver.find_element_by_css_selector('#proxylisttable_next > a:nth-child(1)')
            sleep(0.5)
            driver.execute_script('"window.scrollTo(0, document.body.scrollHeight);"')
            try:
                next_button.click()
            except:
                print('Changing proxy sites. Currently: {}'.format(url))
                if self.url == 'https://us-proxy.org':
                    self.url = 'https://free-proxy-list.net/uk-proxy.html'
                elif self.url == 'https://free-proxy-list.net/uk-proxy.html':
                    self.url = 'https://free-proxy-list.net/anonymous-proxy.html'
                else:
                    self.url = 'https://us-proxy.org'
                
                self.proxy_page = 0
                
                return

            current_page += 1

        self.proxy_page += 1
        
        proxies_body = driver.find_element_by_css_selector('#proxylisttable > tbody:nth-child(2)')
        proxies = proxies_body.find_elements_by_xpath('.//tr')
        print('{} proxies found in total'.format(len(proxies)))
        if not proxies:
            print('No Proxies Found!')
            return None
        
        self.proxies.clear()

        for proxy_element in proxies:
            ip = proxy_element.find_element_by_xpath('.//td[1]').text
            port = proxy_element.find_element_by_xpath('.//td[2]').text
            print('{}:{}'.format(ip, port))
            self.proxies.append('{}:{}'.format(ip, port))
        os.system('taskkill /f /im geckodriver.exe /T')
        
    def get_new_proxy(self):
        print('{} proxies remaining'.format(len(self.proxies)))
        if not self.proxies:
            self.refresh_proxies()
        return self.proxies.pop(int(random() * len(self.proxies)))

    def synchronized_get_new_proxy_dict(self):
        with self.lock:
            return self.get_proxy_dict(self.get_new_proxy())

    def get_proxy_dict(self, current_proxy):
        return { "https" : str(current_proxy) }