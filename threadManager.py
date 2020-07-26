from queue import Queue


class ThreadManager:
    def __init__(self):
        self.num_thread = 0
        self.density_queue = Queue()
        self.thread_queue = Queue()
        self.thread_limit = 16

    def add_thread(self):
        self.num_thread += 1

    def remove_thread(self):
        self.num_thread -= 1
