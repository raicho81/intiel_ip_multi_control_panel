# -*- coding: utf-8 -*-
import queue
import threading
import functools
import PyQt5.QtCore

class Looper(object):

    def __init__(self):
        self.main_id = id(threading.current_thread())
        self.tasks = queue.Queue()

    def process(self):

        try:
            task = self.tasks.get_nowait()
        except queue.Empty:
            pass
        else:
            f, args, kw = task
            f(*args, **kw)

    def enqueue_task(self, f, args=None, kw=None):
        task = f, args or [], kw or {}
        self.tasks.put(task)

    def run_in_ui(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if id(threading.current_thread()) == self.main_id:
                return func(*args, **kwargs)
            else:
                return self.enqueue_task(func, args, kwargs)

        return wrapper
