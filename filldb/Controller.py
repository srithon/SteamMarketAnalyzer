import ProxyList
import Worker
import asyncio

class Controller:
    def __init__(self, db_cursor, num_workers):
        self.db_cursor = db_cursor
        self.num_workers = num_workers
        # self.proxy_list = ProxyList()
        self.workers = list()
        for _ in range(num_workers):
            self.workers.append(Worker(self.proxy_list))
    
    async def work(self):
        await asyncio.gather(*[worker.process_items for worker in self.workers])

