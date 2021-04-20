import xmlrpc.client
import pymongo
import http.client

    
def connect_with_mongoDb():
    try:
        connection_url = 'mongodb+srv://Manjit:Manjit@cluster0.dfnnv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connection_url)  
    except:
        print("Connection Failed With MongoDb Cloud")
    finally:
        return client
    

def conncet_with_server():
    try:
        proxy = xmlrpc.client.ServerProxy("http://192.168.0.194:8000")
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
    finally:
        return proxy