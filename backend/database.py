import json

import pandas as pd
from pip._internal.utils.misc import tabulate
from pymongo import MongoClient


def _connect_mongo(db_name="MovieRating"):
    """ A util for making a connection to mongo """

    mongo_uri = "mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    l_count = 0
    while (l_count < 5):
        print("*******************************************************")
        print("Attempt to connect mongodb atlas (", l_count, ") times")
        print("*******************************************************")
        try:
            my_client = MongoClient(mongo_uri, connectTimeoutMS=2000000, retryWrites=True)
            print("*******************************************************")
            print(my_client.stats)
            print("*******************************************************")
            print("Notice: connected to mongodb atlas")
            print("*******************************************************")
            print(my_client.list_database_names())
            print("*******************************************************")
            print("Notice: connected to MovieRating Database")
            movie_rating_database = my_client[db_name]
            return movie_rating_database
        except:
            l_count += 1
            print("******************************************************************************")
            print("Error: can't connect to mongodb atlas or connection timeout, please try again")
            print("******************************************************************************")



def get_collection(collection, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    db_name = 'MovieRating'
    # Connect to MongoDB
    db = _connect_mongo(db_name)

    # Make a query to the specific DB and Collection
    cursor = db[collection]

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor.find()))


    # Delete the _id
    if no_id:
        del df['_id']

    pd.options.display.max_columns = None
    pd.options.display.width = None

    return df


def update(file, collection):
    pd.options.display.max_columns = None
    pd.options.display.width = None
    db = 'MovieRating'
    # Connect to MongoDB
    db = _connect_mongo(db=db)
    collections = db[collection]

    with open(file) as f:
        file_data = json.load(f)

    collections.insert_one(file_data)

    print("Data inserted on mongodb atlas")
    
    
 def insertUserData(insertData):
    # Connect to MongoDB
    db = _connect_mongo("MovieRating")

    movie_collection = db["movies_metadata"]
    myMoviesData = { "id": insertData['id'], "title": insertData['title']}
    insertedMovieID = movie_collection.insert_one(myMoviesData)

    rating_collection = db["ratings_small"]
    myRatingsData = {"userId": insertData['userId'], "movieId": insertData['movieId'], "timestamp": insertData['timestamp']}
    insertedRatingId = rating_collection.insert_one(myRatingsData)

    if insertedMovieID.acknowledged and insertedRatingId.acknowledged:
        print("Data successfully inserted.")
        return True

    return False

