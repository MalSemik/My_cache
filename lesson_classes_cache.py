import logging
import os
import pickle
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict

import requests

# logging.basicConfig(filename='cache_logs.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger('cache')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('cache.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# class MyEncoder(JSONEncoder):
#     def default(self, o):
#         if isinstance(o, CacheEntry):
#             return o.__dict__
#         else:
#             return super().default(o)


class CacheEntry:
    def __init__(self, response, time, expiration_date):
        self.response = response
        self.time = time
        self.expiration_date = expiration_date


# TODO: Polymorphism
# TODO: Staticmethod
# TODO: test coverage
# TODO: github badges
# TODO: readme


class Cache(ABC):  # klasa abstrakcyjna
    @abstractmethod
    def cached_get(self, url, wait=5.0):
        pass

    # @abstractmethod
    # def new(self):
    #     pass


##### Wstawka od RAfala #####

# class CacheStorage(ABC):
#     @abstractmethod
#     def add(self, url, response):
#         pass
#
#     @abstractmethod
#     def remove(self, url):
#         pass
#
#     @abstractmethod
#     def get_all(self):
#         pass
#
#     @abstractmethod
#     def is_in(self, url):
#         pass
#
#
# class DictCacheStorage(CacheStorage):
#     def __init__(self):
#         self.cache = {}
#
#     def add(self, url, response):
#         self.cache[url] = response
#
#     def remove(self, url):
#         del self.cache[url]
#
#
# class PickleCacheStorage(CacheStorage):
#     def add(self, url, response):
#         pass
#
#
# def simple_clean_cache(cache: CacheStorage):
#     cache.remove('dupa')
#
#
# class BaseCache(Cache):
#     def __init__(self, storage, cleaning_strategy):
#         pass
#
# cache_1 = BaseCache(storage=PickleCacheStorage(), cleaning_strategy=simple_clean_cache)
# cache_2 = BaseCache(storage=DictCacheStorage(), cleaning_strategy=lambda x: print("dupa"))

##### Wstawka od RAfala #####


class DictCache(Cache):
    def __init__(self):
        self.cache: Dict[str, CacheEntry] = {}

    def _find_expired_urls(self):
        urls_to_del = []
        for key, value in self.cache.items():
            if datetime.now() > self.cache[key].expiration_date:
                urls_to_del.append(key)
        return urls_to_del

    def _del_expired_urls(self, urls_to_del):
        for url_to_del in urls_to_del:
            del self.cache[url_to_del]
            logger.info(f'Deleted {url_to_del}')
        logger.debug(f'Actual cache is: {self.cache}')

    def _clean_old_cache_entries(self):
        # TODO: zadanie domowe, usuwac jesli len(cache) > N
        # TODO: w pickle cache'u uzaleznic to od wielkosci pliku
        # Use https://docs.python.org/3/library/os.path.html#os.path.getsize
        urls_to_del = self._find_expired_urls()
        logger.info(f'I\'m going to delete {urls_to_del}')
        self._del_expired_urls(urls_to_del)

    def _get_new_response(self, url, wait):
        response = requests.get(url)
        response.from_cache = False
        time = datetime.now()
        expiration_date = time + timedelta(seconds=wait)
        # cache[url] = {'response': response, 'time': time, 'expiration_date': expiration_date}
        self.cache[url] = CacheEntry(response, time, expiration_date)
        # print(response)
        return response

    def _should_download_new(self, url):
        if url not in self.cache or datetime.now() > self.cache[url].expiration_date:
            return True
        else:
            return False

    def cached_get(self, url, wait=5.0):
        self._clean_old_cache_entries()
        if self._should_download_new(url):
            response = self._get_new_response(url, wait)
            logger.debug(f'New response: {response} ')
            return response
        else:
            response = self.cache[url].response
            response.from_cache = True
            logger.debug(f'Response from cache: {response} ')
            return response


# class JsonCache(DictCache):
#     def __init__(self, filename='json_cache'):
#         super().__init__()
#         self.filename = filename
#         if os.path.exists(filename):
#             with open(self.filename) as file:
#                 cache = json.load(file)
#                 self.cache = cache
#
#     def cached_get(self, url, wait=5.0):
#         response = super().cached_get(url, wait)
#         with open(self.filename, 'w') as file:
#             json.dump(self.cache, file, cls=MyEncoder)


class PickleCache(DictCache):
    def __init__(self, filename='.cache'):
        super().__init__()
        self.filename = filename
        if os.path.exists(filename):
            with open(self.filename, 'rb+') as file:
                cache = pickle.load(file)
                self.cache = cache
            logger.debug(f'Loaded cache from {filename}. Cache: {cache}')

    def cached_get(self, url, wait=5.0):
        response = super().cached_get(url, wait)
        with open(self.filename, 'wb') as file:
            pickle.dump(self.cache, file)
        return response


# cache: Dict[str, CacheEntry] = {}

if __name__ == '__main__':
    cache = DictCache()
    print(cache.cached_get("http://worldtimeapi.org/api/timezone/Europe/Warsaw").status_code)
