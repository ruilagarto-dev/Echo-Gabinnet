from modules.Queue import Queue
from typing import Any, Optional
import threading

class ThreadManager:
    def __init__(self, size: int, timeout: int) -> None:
        self.maxThreads = size
        self.timeout = timeout
        self.__taskQueue = Queue(size)
        self.__completeTaskQueue = Queue(size)
        self.threads = []
        self._lock = threading.Lock()

    def createNewTask(self, task, *args, **kwargs):
        if self.__taskQueue.isFull():
            raise RuntimeError("QUEUE is FULL")
        
        self.__taskQueue.enqueue((task, args, kwargs))
        self.__startThreadForTask(task)

    
    def __startThreadForTask(self, task) -> None:
        if threading.active_count() - 1 < self.maxThreads:        
            thread = threading.Thread(
                target=self.__executeTask, 
                args = (task,),
                daemon=True
            )

            thread.start()
            self.threads.append(thread)


    def __executeTask(self, task):
        while True:
            if self.__taskQueue.isEmpty():
                break
            func, args, kwargs = self.__taskQueue.dequeue()
            try:
                result = task(*args, **kwargs)
                with self._lock:
                    self.__completeTaskQueue.enqueue(("SUCCESS", result))
            except Exception as e:
                with self._lock:
                    self.__completeTaskQueue.enqueue(("ERROR", e))
        
    def __getCompletedTask(self):
        if not self.__completeTaskQueue.isEmpty():
            return self.__completeTaskQueue.dequeue()
        return None
    
    def __wait(self)-> None:
        for thread in self.threads:
            thread.join(timeout = self.timeout)

    
    def runThreads(self):
        self.__wait()
        x = []
        for status, result in iter(self.__getCompletedTask, None):
            if status == "SUCCESS":
                x.append(result)
        
        return x

    
    


    
