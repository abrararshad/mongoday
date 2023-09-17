# mongoday

`mongoday` is a Python library that simplifies document creation in MongoDB. It does not depend on specific library as it is agnostic but built using `pymongo` library. This README provides a brief overview of how to use `mongoday` to work with documents in MongoDB. 

Its development is undergoing but it provides a good starting point for creating documents in MongoDB.

## Installation

You can install `mongoday` using pip:

```bash
pip install mongoday
```

# Getting Started

To get started with `mongoday`, you'll need to create a model for your MongoDB documents. Here's an example of how to create a simple model using `mongoday`:

```
from mongoday.field import BaseField, MongoIDField, StringField
from mongoday.model import BaseModel
from pymongo import MongoClient

class User(BaseModel):
    def __init__(self, collection):
        self.username = StringField()
        super(User, self).__init__(collection)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["users"]

# Initialize a User document
user = User(collection)
user.username = "John"
user.save()

# Retrieve a User document
retrieved_user = User(collection).get(user.id)
print("Username:", retrieved_user.username)
```

## Indexes
To specify indexes, add an indexes attribute to your model class. Here's an example:

````
class User(BaseModel):
    indexes = [
        [('username', 1)],  # Create an ascending index on the 'username' field
        [('created', -1)]  # Create a descending index on the 'created' field
    ]
````
Or could be specified in the constructor, this way it won't override the default indexes specified by the BaseModel class but will be added to them.
````
class User(BaseModel):
    def __init__(self, collection):
        .....
        
        # Specify indexes
        indexes = [
            [('username', 1)],  # Create an ascending index on the 'username' field
            [('created', -1)]   # Create a descending index on the 'created' field
        ]
        self.add_indexes(indexes)
````

# Contribution
Feel free to contribute to this project by opening issues or submitting pull requests on [GitHub](https://github.com/abrararshad/mongoday).

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.