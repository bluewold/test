import mmh3
from bitarray import bitarray
import threading

BIT_SIZE = 5000000

class BloomFilter(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BloomFilter,"_instance"):
            with BloomFilter._instance_lock:
                if not hasattr(BloomFilter,"_instance"):
                    BloomFilter._instance = object.__new__(cls)
        return BloomFilter._instance

    def __init__(self):
        bit_array = bitarray(BIT_SIZE)
        bit_array.setall(0)
        self.start = 41
        self.end = 48
        self.bit_array = bit_array

    def add(self,url):
        pointlist = self.get_position(url)
        for point in pointlist:
            self.bit_array[point] = 1


    def get_position(self,url):
        pointlist = []
        i = self.start
        while i <self.end:
            i = i+1
            pointlist.append(mmh3.hash(url,i)%BIT_SIZE)
        return pointlist

    def contains(self,url):
        pointlist = self.get_position(url)

        for point in pointlist:
            if self.bit_array[point] == 0:
                self.add(url)
                return False
        return True