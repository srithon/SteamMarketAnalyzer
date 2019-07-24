from ProxyList import ProxyList
from Worker import Worker
import threading
import sys
from time import time
import asyncio

class Controller:
    def __init__(self, db_cursor, num_workers, appid, output_table, input_table):
        self.db_cursor = db_cursor
        db_cursor.execute(f'SELECT DISTINCT name FROM {input_table} ORDER by name DESC')
        item_list = [item[0] for item in db_cursor.fetchall()]
        print(len(item_list))
        db_cursor_wrapper = CursorWrapper(db_cursor)
        self.num_workers = num_workers
        self.proxy_list = ProxyList()
        self.worker_threads = list()
        self.workers = list()
        self.last_commit = time()
        item_sublists = self.n_sub_lists(num_workers, item_list)
        print([len(list) for list in item_sublists])
        for i in range(num_workers):
            self.workers.append(Worker(db_cursor_wrapper, self.proxy_list, item_sublists[i], appid, output_table))
    
    def n_sub_lists(self, n, list_to_split):
        av_size = len(list_to_split) // n
        return [list_to_split[i:i+av_size] for i in range(0, len(list_to_split), av_size)]
    
    def display_stats(self):
        for index, worker in enumerate(self.workers):
            print(f'Worker #{index}: {worker.counter}')
        print('Total: {}'.format(sum([worker.counter for worker in self.workers])))
    
    def shutdown(self):    
        print('Keyboard interrupt; shutting down')
        self.db_cursor.connection.commit()
        self.db_cursor.connection.close()
        for worker in self.workers:
            worker.item_list.clear()
        self.display_stats()
    
    def start_workers(self):
        # await asyncio.gather(*[worker.process_items(index) for index, worker in enumerate(self.workers)])
        # this should run each worker on a different process
        for i in range(len(self.workers)):
            event_loop = asyncio.new_event_loop()
            self.worker_threads.append(threading.Thread(target=self.workers[i].start_worker, args=(event_loop,)))
            self.worker_threads[-1].start()
            
        for t in self.worker_threads:
            print('Joining thread')
            try:
                t.join()
            except KeyboardInterrupt:
                self.shutdown()
                sys.exit()
        
        self.shutdown()


class CursorWrapper:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        self.commit_requests = 0
        self.lock = threading.Lock()
        self.last_commit = 0
    
    def request_commit(self):
        with self.lock:
            self.commit_requests += 1
            # last commit was over 1 minutes ago and more than one request
            if time() - self.last_commit > 60 and self.commit_requests > 1:
                self.db_cursor.connection.commit()
                self.commit_requests = 0
                self.last_commit = time()
    
    def execute(self, query, args):
        self.db_cursor.execute(query, args)