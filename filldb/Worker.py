import ProxyList
# import requests
import asyncio
import math

class Worker:
    proxies_per_worker = 3
    delay = 2.5

    def __init__(self, cursor, proxies, item_list):
        self.cursor = cursor
        self.proxies = proxies
        self.reserved_proxies = list()
        self.item_list = item_list
        # self.session = requests.Session()
        for _ in range(Worker.proxies_per_worker):
            self.reserved_proxies.append(self.new_proxy())
    
    def new_proxy(self):
        return self.proxies.synchronized_get_new_proxy_dict()
    
    def process_item(self, pid):
        if self.item_list.is_empty():
            return
        item = self.item_list.pop(0)

        while True:
            try:
                response = self.session.get(f'https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name={item}', proxies = self.reserved_proxies[pid]).json()
                break
            except Exception as e:
                print(f'{pid}: {e}')
                self.reserved_proxies[pid] = self.new_proxy

        try:
            lowest_price = response['lowest_price'][1:]
        except:
            try:
                lowest_price = response['median_price'][1:]
            except:
                print(f'Gave up on {item}')
                return

        try:
            price = math.floor(float(lowest_price.replace(',' , '')) * 100)
        except Exception as e:
            print(e)
            print('--------Price failed-----------')
            return
        
        try:
            volume = response['volume'].replace(',' , '')
        except:
            volume = 0
        
        query = 'INSERT INTO tf2(time, name, price, volume) VALUES (NOW(), %s, %s, %s)'
        self.cursor.execute(query, (item, price, volume))
    
    def test_async_function(self, pid):
        print(pid)

    async def process_items(self, pid):
        while True:
            test_async_function(pid)
            asyncio.sleep(Worker.delay)
