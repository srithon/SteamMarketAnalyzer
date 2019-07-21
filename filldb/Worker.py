import ProxyList
import requests
import asyncio
import math
import threading

class Worker:
    proxies_per_worker = 3
    delay = 2.5

    def __init__(self, cursor_wrapper, proxies, item_list):
        self.cursor = cursor_wrapper
        self.proxies = proxies
        self.reserved_proxies = list()
        self.item_list = item_list
        self.http_session = requests.Session()
        self.counter = 0
        for _ in range(Worker.proxies_per_worker):
            self.reserved_proxies.append(self.new_proxy())
    
    def new_proxy(self):
        return self.proxies.synchronized_get_new_proxy_dict()
    
    async def process_item(self, pid):
        if not self.item_list:
            return
        try:
            item = self.item_list.pop(0)
        except Exception as e:
            print(f'Error in process_item->item_list.pop(): {e}')

        while True:
            try:
                response = self.http_session.get(f'https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name={item}', proxies = self.reserved_proxies[pid]).json()
                await asyncio.sleep(0)
                break
            except Exception as e:
                print(f'{pid}: {e}')
                self.reserved_proxies[pid] = self.new_proxy()

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
        
        self.counter += 1
        print(f'Worker \'{threading.current_thread().name}\': Iteration #{self.counter}')
        if self.counter % 200 == 0:
            self.cursor.request_commit()
    
    def test_async_function(self, pid):
        print(pid)
        
    async def internal_process_items(self, pid):
        while self.item_list:
            await self.process_item(pid)
            await asyncio.sleep(Worker.delay)

    async def process_items(self):
        await asyncio.gather(*[self.internal_process_items(index) for index in range(Worker.proxies_per_worker)])
    
    def start_worker(self, event_loop):
        try:
            event_loop.run_until_complete(self.process_items())
        finally:
            event_loop.close()
