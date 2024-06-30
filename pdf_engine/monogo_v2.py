import os
from dotenv import load_dotenv
load_dotenv()

# from mongo import Mongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoDBHandler:
    def __init__(self, db_name='pdf_engine', collection_name='pdf_collection'):
        uri = f"mongodb+srv://{os.environ.get('user_heroku')}:{os.environ.get('pass_heroku')}@cluster0.mtiz1sj.mongodb.net/?retryWrites=true&w=majority"
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = client[db_name]
        self.collection = self.db[collection_name]
        # Ensure text index is created
        self.collection.create_index([('children_text', 'text')])
    def insert(self, data):
        self.collection.insert(data)
    def search(self, query):
        results = self.collection.find(
            {'$text': {'$search': query}},
            {'score': {'$meta': 'textScore'}, '_id': 0, 'id': 1, 'mimeType': 1, 'title': 1, 'quotaBytesUsed': 1, 'owners': 1, 'children_list': 1}
        ).sort([('score', {'$meta': 'textScore'})])
        return list(results)
    # def delete_collection(self):
    #     self.collection.
    def bulk_insert(self, data):
        """Insert multiple documents into the collection."""
        if type(data) == list:
            self.collection.insert_many(data)
        elif type(data) == dict:
            # Prepare a list of documents with custom _id values
            documents_to_insert = [
                {'_id': doc_id, 'data': doc_data} for doc_id, doc_data in data.items()
            ]
            # Insert documents into the collection
            result = self.collection.insert_many(documents_to_insert)
            # Print the inserted document ids
            print(f"Inserted documents with ids: {result.inserted_ids[:10]}")
            # Close the MongoDB connection
            client.close()
    def delete():
        # Delete from 'test' collection
        self.collection.delete_many({})

if __name__=="__main__":
    searcher = MongoDBHandler('pdf_engine', collection_name='pdf_collection')
    searcher.search('engineering physics')