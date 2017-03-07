from scrapy.utils.reqser import request_to_dict, request_from_dict

from . import picklecompat

import redis
class Base(object):
    def __init__(self, server, spider, key, serializer=None):
        if serializer is None:
	      serializer = picklecompat
	      #if not hasattr(serializer, 'loads'):
	      #    raise TypeError("serializer does not implement 'loads' function: %r"% serializer)
		#if not hasattr(serializer, 'dumps'):
		#    raise TypeError("serializer '%s' does not implement 'dumps' function: %r"% serializer)
        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer
        
    def _encode_request(self, request):
	"""Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
	"""Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
	"""Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
	"""Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
	"""Pop a request"""
        raise NotImplementedError

    def clear(self):
	"""Clear queue/stack"""
        self.server.delete(self.key)


class FifoQueue(Base):
    def __len__(self):
        return self.server.llen(self.key)

    def push(self, request):
        #self.server.lpush(self.key, self._encode_request(request))
	data=self._encode_request(request)
	#ret=self.server.lpush(self.key,data)
	self.server.execute_command('lpush',self.key,data)
	print self.__len__()
    def pop(self, timeout=0):		
        #if timeout > 0:
        #data = self.server.brpop(self.key,timeout)
            #if isinstance(data,tuple):
            #    data = data[1]
	      #else:
	      #    data = self.server.rpop(self.key)
        #if data:
        #    return self._decode_request(data)
        #data=self.server.execute_command('lindex',self.key,0)
	#print type(data)
	#if data:
        #    return self._decode_request(data)
	print self.__len__()
	if self.__len__()==0:
		return     
        else:
            data=self.server.brpop(self.key,0)
	    if data:
                return self._decode_request(data[1])
class PriorityQueue(Base):
    def __len__(self):
        return self.server.zcard(self.key)

    def push(self, request):
        data = self._encode_request(request)
        score = -request.priority
        self.server.execute_command('ZADD', self.key, score, data)

    def pop(self, timeout=0):
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


class LifoQueue(Base):
    def __len__(self):
        return self.server.llen(self.key)

    def push(self, request):
        self.server.lpush(self.key, self._encode_request(request))
    def pop(self, timeout=0):
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            #if isinstance(data, tuple):
            #    data = data[1]
		#else:
            #    data = self.server.lpop(self.key)
        if data:
            return self._decode_request(data)


# TODO: Deprecate the use of these names.
SpiderQueue = FifoQueue
SpiderStack = LifoQueue
SpiderPriorityQueue = PriorityQueue
