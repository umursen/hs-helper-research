class GameIterator:

    def __init__(self):
        self.num_thread = 0
        self.threads = []

    def add_thread(self):
        self.num_thread += 1

    def remove_thread(self):
        self.num_thread -= 1
