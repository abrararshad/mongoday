import hashlib
import json


def create_index_hash(indexes):
    index_str = json.dumps(indexes, sort_keys=True)
    return hashlib.sha256(index_str.encode()).hexdigest()


INDEX_STORE_COLLECTION = None


class IndexStore(object):
    def __init__(self, collection=None):
        global INDEX_STORE_COLLECTION

        if collection is None:
            if INDEX_STORE_COLLECTION is None:
                raise ValueError("Index store collection not set")
            self.collection = INDEX_STORE_COLLECTION
        else:
            self.collection = collection
            INDEX_STORE_COLLECTION = collection

    def get_hash(self, collection_name):
        col = self.collection.find_one({'col_name': collection_name})
        if col:
            return col['hash']

        return None

    def set_hash(self, collection_name, index_hash):
        return self.collection.update_one({'col_name': collection_name}, {'$set': {'hash': index_hash}}, upsert=True)

    def delete_hash(self, collection_name):
        return self.collection.delete_one({'col_name': collection_name})
