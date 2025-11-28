from pymongo import MongoClient
import configparser
from pymongo.errors import ConnectionFailure
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

class MongodbOperations: 
    def __init__(self, db_name):
        try:
            # Connect to MongoDB
            self.db_name = db_name
            host_name = config['MONGODB']['host']
            port = config['MONGODB']['port']
            self.client = MongoClient(f'mongodb://{host_name}:{port}/')
            self.db = self.client[self.db_name]
        except ConnectionFailure as cf:
            print(f"MongoDB connection failed: {cf}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if 'client' in locals() and client:
                client.close()
                print("MongoDB connection closed.")

    def get_collection(self, collection_name):
        """
        Retrieves a specific collection from the database.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            pymongo.collection.Collection: The specified MongoDB collection.
        """
        return self.db[collection_name]

    def insert_one(self, collection_name, document):
        """
        Inserts a single document into a specified collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to insert.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def insert_many(self, collection_name, documents):
        """
        Inserts multiple documents into a specified collection.

        Args:
            collection_name (str): The name of the collection.
            documents (list): A list of documents to insert.

        Returns:
            pymongo.results.InsertManyResult: The result of the insert operation.
        """
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)

    def find(self, collection_name, query=None, projection=None):
        """
        Finds documents in a specified collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (dict, optional): The query to filter documents. Defaults to None (returns all documents).
            projection (dict, optional): Specifies which fields to include or exclude. Defaults to None.

        Returns:
            pymongo.cursor.Cursor: A cursor to iterate over the matching documents.
        """
        collection = self.get_collection(collection_name)
        print(query)
        return collection.find(query, projection)

    def find_one(self, collection_name, query):
        """
        Finds a single document in a specified collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.

        Returns:
            dict or None: The first matching document, or None if no document matches.
        """
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def update_one(self, collection_name, query, new_values):
        """
        Updates a single document in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to find the document to update.
            new_values (dict): The new values to set. Use MongoDB operators like '$set'.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        collection = self.get_collection(collection_name)
        return collection.update_one(query, new_values)

    def update_many(self, collection_name, query, new_values):
        """
        Updates multiple documents in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to find the documents to update.
            new_values (dict): The new values to set. Use MongoDB operators like '$set'.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        collection = self.get_collection(collection_name)
        return collection.update_many(query, new_values)

    def delete_one(self, collection_name, query):
        """
        Deletes a single document from a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to find the document to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result

    def delete_many(self, collection_name, query):
        """
        Deletes multiple documents from a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to find the documents to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        collection = self.get_collection(collection_name)
        return collection.delete_many(query)

    def close_connection(self):
        """
        Closes the MongoDB client connection.
        """
        self.client.close()

# sm_data = pd.read_csv('data/smmh.csv')
# sm_data['user_id'] = sm_data.index + 1
# records = sm_data.to_dict('records')

# mdo = MongodbOperations("social_media_analysis")
# mdo.insert_many("raw_data", records)


                


