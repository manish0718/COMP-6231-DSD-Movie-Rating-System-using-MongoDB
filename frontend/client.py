import xmlrpc.client
import pymongo
import http.client

    
def connect_with_mongoDb():
    try:
        connection_url = 'mongodb+srv://Manjit:Manjit@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connection_url)  
        db = client.get_database('Clients')
        db1 = client.get_database('MovieRating')
    except:
        print("Connection Failed With MongoDb Cloud")
    finally:
        return db,db1
    

def conncet_with_server():
    try:
        proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
    finally:
        return proxy