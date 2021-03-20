from flask import Flask , jsonify, request , render_template  
import pymongo 
  

connection_url = 'mongodb+srv://m001-student:M001MongoBasics@sandbox.punqd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 

db = client.get_database('sample_airbnb') 

app.secret_key = "key"




@app.route('/')
def index():
    return render_template('Home.html')

@app.route("/Movie_Name",methods=['GET','POST'])
def fetch():
    if request.method == "POST":
        name = request.form["MovieName"]
        if name:
            try:
                queryObject = {name: 361} 
                query = db.listingsAndReviews.find_one(queryObject , {name:1}) 
                query.pop('_id') 
                query = jsonify(query) 
            except:
                print("error")
            finally:
                return render_template("Result.html", data = query)
        
  

  
if __name__ == '__main__': 
    app.run() 