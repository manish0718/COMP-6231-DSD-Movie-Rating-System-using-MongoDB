# my_server program
import sys
from socketserver import ThreadingMixIn

import pymongo
import warnings

warnings.filterwarnings("ignore")

sys.path.append('../')

import database
from ml import ml_driver
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

"""
field data
"""
movie_rating_database = None
movie_metadata_collection = None


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client host and current date/time are prefixed to
        every message.

        """

        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def serverSetUp():
    """
    Server initialization
    """
    global movie_rating_database
    global movie_metadata_collection
    movie_rating_database = database._connect_mongo()
    movie_metadata_collection = movie_rating_database["movies_metadata"]
    print("my_server database setup ready..")


def searchHandler(p_input_movie):
    """
    simple search function here
    :param p_input_movie:
    :return: str
    """
    print("***************************************************")
    print("RPC CALL: SEARCH REQUEST")
    print("***************************************************")
    print("Retrieving document for movie: " + p_input_movie)
    if(database.searchMovie(p_input_movie)):
        print("***************************************************")
        print("Movie Is Present In The Database")
        print("***************************************************")
        return True
    else:
        print("***************************************************")
        print("Movie Is Not Present In The Database")
        print("***************************************************")
        return False
    


def getRecommMovieList(p_input_str):
    """
    the ml get Recommend Movie List function here
    :param p_input_str:
    :return: str list
    """

    # str_list = retrievingDetailsOfMovies(ml_driver.ml_run(p_input_str))
    str_list = ml_driver.ml_run(p_input_str)
    return str_list


def mongo_instance(username, password):
    Response = False
    try:
        print("***************************************************")
        print("RPC CALL: Verify The Credentials For Successful login")
        print("***************************************************")
        Response=database.mongoLogin(username,password)
        if (Response):
            print("***************************************************")
            print(username + " Successfully Loged In")
            print("***************************************************")
        else:
            print("***************************************************")
            print(username + " Incorrect Credentials")
            print("***************************************************")

    except:
        print("***************************************************")
        print("Connection Failed With MongoDb Cloud")
        print("User Was not able to successfully log in")
        print("***************************************************")

    finally:
        if(Response==True):
            return True
        else:
            return False


def mongo_register(username, password, ID):
    Response = False
    try:
        print("***************************************************")
        print("RPC CALL: Verify The Credentials For Registration and Register The New User")
        print("***************************************************")
        Response = database.registerWithMongo(username,password,ID)
        if (Response):
            print("***************************************************")
            print(username + " Successfully Registered With Us")
            print("***************************************************")
        else:
            print("***************************************************")
            print(username + " Unuccessfully Registration")
            print("***************************************************")

    except:
        print("***************************************************")
        print("Connection Failed With MongoDb Cloud")
        print("User was not able to successfully register with us")
        print("***************************************************")

    finally:
        if(Response==True):
            return True
        else:
            return False


def retrievingDetailsOfMovies(movie_title_list):
    """
    read the list of movies and return details of each movie as a document from MongoDb
    :return: movie list
    """
    movies_list = []
    # mongodb = DatasetUpload.MongoDB(dBName='MoviesRating', collectionName='movies_metadata')
    for movie in movie_title_list:
        movie_doc = movie_metadata_collection.find({"title": movie})
        # movies_list.append(json.dumps(movie_doc))
        print("Retrieving document for movie: " + movie_doc)
        print(movies_list)
    return movie_title_list


def data_validator(dict):
    """

    :param dict:
    :return: True if dict contain all five k,v
                False if dict contains less than five k,v
    """
    for l_each in dict:
        # check whether value is null
        if bool(dict[l_each]):
            # id and movieId are the same object
            if l_each == "id":
                dict[l_each] = dict["movieId"]
            elif l_each == "movieId":
                dict[l_each] = dict["id"]
            # if other obj value is null, return false, ask user to input again
            else:
                return False
    return True


def insertRequest(dict):
    """
    insert a new movie and its rating to database
    :param dict: dataToinsert = {
        "id": "12345",
        "title": "example",
        "userId": "5",
        "movieId": "12345",
        "timestamp": "9999999"
    }
    :return:
    """
    print("RPC CALL: INSERT REQUEST")
    data_validator(dict)

    if database.insertUserData(dict):
        return True
    else:
        return False
    return True


def updateRequest(dict):
    """
    update current movie data in database
    :param dict: dataToinsert = {
        "id": "12345",
        "title": "example",
        "userId": "5",
        "movieId": "12345",
        "timestamp": "9999999"
    }
    :return:
    """

    print("RPC CALL: UPDATE REQUEST")

    data_validator(dict)

    if database.updateUserData(dict):
        return True
    else:
        return False


def deleteRequest(dict):
    """
    delete the movie from the database
    :param movie_name_to_del:
    :return:
    """
    print("RPC CALL: DELETE REQUEST")

    if database.deleteUserData(dict):
        return True
    else:
        return False


def run_server(host="192.168.0.194", port=8000):
    serverSetUp()
    server_addr = (host, port)
    with SimpleThreadedXMLRPCServer((server_addr), logRequests=True, allow_none=True) as my_server:
        my_server.register_introspection_functions()
        my_server.register_function(searchHandler, 'searchmovie')
        my_server.register_function(getRecommMovieList, 'getrecommend')
        my_server.register_function(mongo_instance, 'atlas_instance')
        my_server.register_function(mongo_register, 'register')
        my_server.register_function(insertRequest, 'insert')
        my_server.register_function(deleteRequest, 'delete')
        my_server.register_function(updateRequest, 'update')

        try:
            print("*******************************************************")
            print("my_server setup ready..")
            print("*******************************************************")
            my_server.serve_forever()
        except KeyboardInterrupt:
            print("*******************************************************")
            print("\nKeyboard interrupt received, exiting.")

            sys.exit(0)


if __name__ == "__main__":
    run_server()


