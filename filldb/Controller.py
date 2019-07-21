import ProxyList
import Worker

class Controller:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.proxy_list = ProxyList()
        self.workers = list()
        for _ in range(num_workers):
            self.workers.append(Worker(self.proxy_list))
