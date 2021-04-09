import json

import pandas as pd
from pip._internal.utils.misc import tabulate
from pymongo import MongoClient

# my_server program
import sys

from bson.json_util import dumps
import datalink
from ml import ml_driver
# import rpc module
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

def _connect_mongo(db):
    """ A util for making a connection to mongo """

    mongo_uri = "mongodb+srv://manish:manish@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    l_count = 0
    while (l_count < 5):
        print("Attempt to connect mongodb atlas (", l_count, ") times")
        try:
            my_client = MongoClient(mongo_uri, connectTimeoutMS=200, retryWrites=True)
            print(my_client.stats)
            print("Notice: connected to mongodb atlas")
            print(my_client.list_database_names())
            print("Notice: connected to MovieRating Database")
            movie_rating_database = my_client["MovieRating"]
            return movie_rating_database
        except:
            l_count += 1
            print("Error: can't connect to mongodb atlas or connection timeout, please try again")

    return my_client[db]

def get_collection(collection, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    db = 'MovieRating'
    # Connect to MongoDB
    db = _connect_mongo(db=db)

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

def update(file,collection):
    pd.options.display.max_columns = None
    pd.options.display.width=None
    db = 'MovieRating'
    # Connect to MongoDB
    db = _connect_mongo(db=db)
    collections = db[collection]


    with open(file) as f:
        file_data = json.load(f)

    collections.insert_many(file_data)

    print("Data inserted on mongodb atlas")

"""
field data
"""
movie_rating_database = None
movie_metadata_collection = None


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/',)


def serverSetUp():
    """
    Server initialization
    """
    global movie_rating_database
    global movie_metadata_collection
    movie_rating_database = datalink.connect_to_MongoDB()
    # print(movie_rating_database.list_collection_names())
    movie_metadata_collection = movie_rating_database["movies_metadata"]
    print("my_server database setup ready..")


def searchHandler(p_input_movie):
    """
    simple search function here
    :param p_input_movie:
    :return: str
    """
    print("Retrieving document for movie: " + p_input_movie)
    return movie_metadata_collection.find({"title": p_input_movie})


def getRecommMovieList(p_input_str):
    """
    the ml get Recommend Movie List function here
    :param p_input_str:
    :return: str list
    """

    str_list = retrievingDetailsOfMovies(ml_driver.ml_run(p_input_str))
    return str_list


def retrievingDetailsOfMovies(movie_title_list):
    """
    read the list of movies and return details of each movie as a document from MongoDb
    :return: movie list
    """
    movies_list = []
    # mongodb = DatasetUpload.MongoDB(dBName='MoviesRating', collectionName='movies_metadata')
    for movie in movie_title_list:
        movie_doc = movie_metadata_collection.find({"title": movie})
        movies_list.append(movie_doc)
        print("Retrieving document for movie: " + movie)
        for document in movie_doc:
            print(dumps(document))
    return movies_list


if __name__ == "__main__":
    serverSetUp()
    with SimpleXMLRPCServer(('localhost', 8000),
                            requestHandler=RequestHandler) as my_server:
        my_server.register_introspection_functions()
        my_server.register_function(searchHandler, 'searchmovie')
        my_server.register_function(getRecommMovieList, 'getrecommend')
        # title_list = ['Toy Story', 'Jumanji', 'Grumpier Old Men', 'Father of the Bride Part II']
        # title_list = getRecommMovieList('Toy Story')
        # retrievingDetailsOfMovies(title_list)
        # Run the my_server's main loop
        try:
            path = "C:\\MovieRatingDS-main\\resource\\test.json"
            update(file=path,collection='xyz')
            mongodb = get_collection(collection='xyz')
            print(mongodb.head())
            print("my_server setup ready..")
            my_server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
