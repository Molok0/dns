import pickle
import time


class DNSCache:
    def __init__(self, cache_file_path):
        self.cache_file_path = cache_file_path
        self.cache = self._start_cache()

    def get_cache(self):
        return self.cache

    def save_cache(self):
        with open(self.cache_file_path, 'wb') as file:
            pickle.dump(self.cache, file)

    def get_response(self, key):
        response = self.cache.get(key)
        if response is None:
            return None
        response_data, ttl = response
        if time.time() > ttl:
            del self.cache[key]
            return None
        return response_data

    def put_answer(self, key, response, ttl):
        result_ttl = time.time() + ttl
        self.cache[key] = (response, result_ttl)

    def _start_cache(self):
        try:
            with open(self.cache_file_path, 'rb') as file:
                data = pickle.load(file)
                return {key: (response, ttl) for key, (response, ttl) in data.items() if time.time() < ttl}
        except FileNotFoundError:
            return {}
