import os
import json
import redis
# from pdf_engine.mongo_db_handler import MongoDBHandler
from pdf_engine.monogo_v2 import MongoDBHandler
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
        self.redis_client = redis.Redis(
            host=os.environ.get('redis_host'),
            port=int(os.environ.get('redis_port')),
            password=os.environ.get('redis_password')
        )
        self.threshold_num_keys = 15

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
    def redis_set(self, query, search_results):
        

        # Get the current number of keys
        num_keys = self.redis_client.dbsize()

        # Check if the number of keys exceeds the threshold
        if num_keys > self.threshold_num_keys:
            # Determine how many keys to deleteq
            keys_to_delete = num_keys - self.threshold_num_keys
            
            print(f'\n Number of keys exceeds the threshold: {num_keys}')
            print(f'\n\n keys_to_delete: {keys_to_delete}\n\n')
            
            # Get the oldest keys based on creation time (use appropriate key patterns if needed)
            # oldest_keys = self.redis_client.zrange('custom_timestamps', 0, keys_to_delete - 1)

            for n, key in enumerate(reversed(self.redis_client.keys('*'))):
                # print(n, key)
                if n < keys_to_delete:
                    self.redis_client.delete(key)
        self.redis_client.set(query, json.dumps(search_results))
    
    def search(self, query):
        '''
        query -> str: search query

        # Pseudo Code:
        
        if query in redis:
            querys = redis.get(query)
            data = get_db(querys)
        else:
            search_results = search_mongo()
            redis.set(query, search_results, expire)
            return search_result

        '''
        try:

            results = self.redis_client.get(query)
            if results is None:
                print(f'\n\n no-found \'{query}\' in redis\n')
                results = self.parallel_search(query)
                if results:
                    try:
                        # Save if results are not empty
                        self.redis_set(query, results)
                        # print(f'\n\n saved \'{query}\' in redis\n')
                    except Exception as e:
                        print(f'\n\n Error: {e} \n\n')
            else:
                results = json.loads(results)
                print(f'\n\n fouqnd \'{query}\' in redis\n')
        except Exception as e:
            print(f'\n\n Error: {e} \n\n')
            results = self.parallel_search(query)
            if results:
                try:
                    # Save if results are not empty
                    self.redis_set(query, results)
                    # print(f'\n\n saved \'{query}\' in redis\n')
                except Exception as e:
                    print(f'\n\n Error: {e} \n\n')
        return results

    def parallel_search(self, query):
        ignore_words = ["engineering", 'how', 'whatever', 'him', 'would', 'they', 'whichever', 'what', 'whysoever', 'have', 'why', 'can', 'our', 'whosoever', 'her', 'whatsoever', 'wherever', 'whyever', 'and', 'whoever', 'that', 'when', 'this', 'which', 'whenever', 'them', 'been', 'his', 'for', 'whensoever', 'the', 'their', 'was', 'but', 'one', 'whosesoever', 'whomsoever', 'whom', 'not', 'all', 'howsoever', 'will', 'you', 'your', 'were', 'with', 'has', 'she', 'from', 'are', 'wheresoever', 'whose', 'had', 'who', 'where', 'there', 'whomever', 'best']
        # query_parts = [query]
        query_parts = [word for word in list(set([query] + query.split())) if ( (word not in ignore_words) and len(word)>=3)]   # ['Engineering', 'Physics', 'Engineering Physics']
        # print(query_parts)
        with ThreadPoolExecutor() as executor:
            # Use ThreadPoolExecutor to execute search function for each query part
            results = [result for sublist in executor.map(self.search_mongo, query_parts) for result in sublist]
        
        return results

if __name__ == "__main__":
    # Instantiate the RedisCache
    redis_cache = RedisCache()
    result = redis_cache.get("math")
    print(result)

if __name__ == "__main__":

    data = list(mongo_handler.collection.find(
        {'$text': {'$search': query}},
        {
            'score': {'$meta': 'textScore'}, 
            'id': 1,
            '_id': 0,  # This excludes _id from the results
            'mimeType': 1, 
            'title': 1, 
            'quotaBytesUsed': 1, 
            'owners': 1, 
            'children_list': 1
        }
    ).sort([('score', {'$meta': 'textScore'})]))
    print(data[0])