import pandas as pd
from pymongo import MongoClient


def _connect_mongo(db):
    """ A util for making a connection to mongo """

    mongo_uri = "mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    conn = MongoClient(mongo_uri)


    return conn[db]


def read_mongo(db, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df
