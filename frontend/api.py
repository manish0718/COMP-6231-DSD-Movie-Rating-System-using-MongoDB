from flask import Flask , jsonify, request , render_template , flash  
import pymongo 
  

connection_url = 'mongodb+srv://m001-student:M001MongoBasics@sandbox.punqd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 

db = client.get_database('sample_airbnb') 
db1 = client.get_database('Clients')

app.secret_key = "key"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("Home.html")

@app.route("/Contact")
def contact():
    return render_template("Contact.html")

@app.route("/About")
def about():
    return render_template("About.html")

@app.route("/Search")
def ML():
    return render_template("Machine Learning.html")

@app.route("/SignUp")
def SignUp():
    return render_template("SignUp.html")


@app.route('/login', methods=['GET','POST'])
def authentication():
    
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        if(username and password):
            queryObject = {'Name':username,'Password':password}
            query = db1.users.find_one(queryObject)
            if(query):
                try:
                    print(query)                
                except:
                    print("Error")
                finally:
                    return render_template("Home.html")
                
            else:
                flash("Incorrect Credentials")
                return render_template("login.html")
        else:
            flash("Empty Credentials")
            return render_template("login.html")
                

    
@app.route("/Movie_Name",methods=['GET','POST'])
def fetch():
    if request.method == "POST":
        name = request.form["MovieName"]
        if name:
            try:
                queryObject = {name: 361} 
                query = db.listingsAndReviews.find_one(queryObject) 
                query.pop('_id') 
                query = jsonify(query) 
            except:
                return render_template("Home.html")
            finally:
                return render_template("Result.html", data = query)
            

@app.route("/Register",methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        ID = request.form["ID"]
        if username and password and ID:
            try:
                db = client.Clients
                user = {            
                    "id": ID,
                    "Name":username,
                    "Password":password                     
                    }
        
                db.users.insert_one(user)
            except:
                flash("Something Went Wrong")
                return render_template("SignUp.html")
            finally:
                flash("Successfully Registered")
                return render_template("login.html")
        else:
            flash("Something Went Wrong")
            return render_template("SignUp.html")
        
  

  
if __name__ == '__main__': 
    app.run() 