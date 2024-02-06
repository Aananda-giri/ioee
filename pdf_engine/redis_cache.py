import os
import json
import redis
from pdf_engine.mongo_db_handler import MongoDBHandler
from concurrent.futures import ThreadPoolExecutor
import time
import dotenv
dotenv.load_dotenv()

class RedisCache:
    def __init__(self):
        # host=os.environ.get('redis_host')
        # port=os.environ.get('redis_port')
        # password=os.environ.get('redis_password')
        # print(f'\n\n host: {host}, port: {port}, password: {password} \n\n')
        self.redis = redis.Redis(
            host=os.environ.get('redis_host'),
            port=int(os.environ.get('redis_port')),
            password=os.environ.get('redis_password')
        )

    def search_mongo(self, query):
        # get results from mongo db
        mongo_handler = MongoDBHandler(collection_name = "pdf_collection", db_name="pdf_engine")
        try:
            search_result = list(mongo_handler.search(query))
        except:
            # search_result is empty
            search_result = []
        
        # save results fro default query: physics
        # with open("pdf_engine_search_result_physics.json", 'w') as file:
        #     json.dump(list(search_result), file)
        return search_result

    def get(self, key):
        '''
        key -> str: search query

        # Pseudo Code:
        
        if key in redis:
            keys = redis.get(key)
            data = get_db(keys)
        else:
            search_results = search_mongo()
            redis.set(key, search_results, expire)
            return search_result

        '''
        results = self.redis.get(key)
        if results is None:
            results = self.search_mongo(key)
            if results:
                # Save if results are not empty
                self.redis.set(key, json.dumps(results))
                # print(f'\n\n saved \'{key}\' in redis\n')
        else:
            results = json.loads(results)
            # print(f'\n\n fouqnd \'{key}\' in redis\n')
        return results

    def parallel_search(self, query):
        ignore_words = ['how', 'whatever', 'him', 'would', 'they', 'whichever', 'what', 'whysoever', 'have', 'why', 'can', 'our', 'whosoever', 'her', 'whatsoever', 'wherever', 'whyever', 'and', 'whoever', 'that', 'when', 'this', 'which', 'whenever', 'them', 'been', 'his', 'for', 'whensoever', 'the', 'their', 'was', 'but', 'one', 'whosesoever', 'whomsoever', 'whom', 'not', 'all', 'howsoever', 'will', 'you', 'your', 'were', 'with', 'has', 'she', 'from', 'are', 'wheresoever', 'whose', 'had', 'who', 'where', 'there', 'whomever', 'best']
        query_parts = [word for word in list(set(query.split() + [query])) if ( (word not in ignore_words) and len(word)>=3)]   # ['Engineering', 'Physics', 'Engineering Physics']
        print(query_parts)
        with ThreadPoolExecutor() as executor:
            # Use ThreadPoolExecutor to execute search function for each query part
            results = [result for sublist in executor.map(self.get, query_parts) for result in sublist]
        return results

if __name__ == "__main__":
    # Instantiate the RedisCache
    redis_cache = RedisCache()
    result = redis_cache.get("math")
    print(result)