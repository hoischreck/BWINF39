from threading import Thread
import queue, math, requests

class Simple1DThreadHandler():
    def __init__(self, thread_amount, function, arguments):
        self.thread_amount = thread_amount
        self.func = function
        self.args = arguments
        self.queue = queue.Queue()
        self.threads = list()
    def run(self):
        arguments = self.split_args()
        for t in arguments:
            self.threads.append(Thread(target=lambda q, args: q.put(self.func(args)), args=(self.queue, t)))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        r = list()
        while not self.queue.empty():
            r.append(self.queue.get())
        return r
    def split_args(self):
        chunks = math.ceil(len(self.args)/self.thread_amount)
        return [self.args[chunks*i:chunks*(i+1)] for i in range(len(self.args[::chunks]))]

def factorial(self, n):
    return n if n <= 1 else n * self.factorial(n-1)

def text_files_from_url(name, *urls):
    for c, i in enumerate(urls):
        with open(os.path.join("Beispiele", f"{name}{c + 1}"), "w", encoding="utf8") as f:
            f.write(requests.get(i).text)
