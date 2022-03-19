import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"

class redis_queue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(host=REDIS_HOST,port=REDIS_PORT,**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0
    
    def show_itens(self):
        return self.__db.lrange(self.key, 0, -1)
    
    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def hset(self,key,value):
        self.__db.hset(self.key,key,value)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def mostra(self):
        self.__db.hlen(self.key)