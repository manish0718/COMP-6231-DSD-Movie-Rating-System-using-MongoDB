# my_server program
import sys

from bson.json_util import dumps
import datalink
from ml import ml_driver
# import rpc module
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

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
            print("my_server setup ready..")
            my_server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

