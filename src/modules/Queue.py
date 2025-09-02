from collections import deque
from typing import Any, Optional

class Queue:
    def __init__(self, maxSize: int) -> None:
        self.__queue = self.createQueue(maxSize)


    def createQueue(self, maxSize: int):
        return deque(maxlen = maxSize)
    

    def enqueue(self, value: Any) -> None:
        if self.size() < self.__queue.maxlen:
            self.__queue.append(value)

    
    def dequeue(self) -> Any:
        if self.isEmpty():
            raise IndexError("Queue Is Empty")
        return self.__queue.popleft()
    
    def isEmpty(self) -> bool:
        return not self.__queue
    
    def isFull(self) -> bool:
        return self.size() == self.__queue.maxlen
    

    def peek(self) -> Any:
        if self.isEmpty():
            return IndexError("Queue is Empty")
        return self.__queue[0]
    

    def size(self) -> int:
        return len(self.__queue)
