from flask import Flask, request, render_template, flash
import client

app = Flask(__name__)

app.secret_key = "key"

ClientStub = client.conncet_with_server()

def fetch_db():
    conn = client.connect_with_mongoDb()
    db = conn.get_database('Clients')
    db1 = conn.get_database('MovieRating')
    return db , db1

db,db1 = fetch_db()

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


@app.route('/login', methods=['GET', 'POST'])
def authentication():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        if (username and password):
            l_count=0;
            while(l_count<5):
                print("***************************************************")
                print("Wait... Verifying Your Credentials")
                print("***************************************************")
                try:
                    l_count+=1;
                    Response = ClientStub.atlas_instance(username,password)
                    if (Response == True):                        
                        print("***************************************************")
                        print("Successfully Loged In")
                        print("***************************************************")
        
                    else:                                               
                        print("***************************************************")
                        print("Error Occurred Please Try Again")
                        print("***************************************************")
                        flash("Incorrect Credentials")
                        return render_template("login.html")
                    
                finally:
                    return render_template("Home.html")  
        else:
            print("*******************************************************")
            print("Empty Credentials")
            print("*******************************************************")
            flash("Empty Credentials")
            return render_template("login.html")


@app.route("/Movie_Name", methods=['GET', 'POST'])
def fetch():
    if request.method == "POST":
        name = request.form["MovieName"]
        rating = request.form["MovieRating"]
        if name:
            l_count = 0;
            while(l_count<5):
                print("*******************************************************")
                print("Trying to connect to the Server....")
                print("*******************************************************")
                try:
                    print("I m In")
                    l_count+=1                    
                    print(ClientStub)
                    Movie = ClientStub.getrecommend(name)
                    print(Movie)
                    json_movie = []
                    print("*******************************************************")
                    print("Fetching")
                    print("*******************************************************")
    
                    for movie in Movie:
                        queryObject = {"title": movie}
                        query = db1.movies_metadata.find_one(queryObject)
                        query.pop('_id')
                        json_movie.append(query)
    
                    return json_movie
    
                except:
                    return render_template("Home.html")
                finally:
                    return render_template("Result.html", data=json_movie[0],data1=json_movie[1],data2=json_movie[2],data3=json_movie[3],data4=json_movie[4],data5=json_movie[5],data6=json_movie[6],data7=json_movie[7],data8=json_movie[8],data9=json_movie[9])
        else:
            print("*******************************************************")
            print("Movie Name Not Entered By User")
            print("*******************************************************")
            flash("Please Enter The Movie Name")
            return render_template("Machine Learning.html")


@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        ID = request.form["ID"]
        if username and password and ID:
            l_count=0
            while(True):
                print("*************************************************************************")
                print("Trying To Register With The Server. Please Wait........................")
                print("*************************************************************************")
                try:
                    l_count+=1;
                    Response = ClientStub.register(username,password,ID)
                    if(Response == True):
                        print("*******************************************************")
                        print(username + " You Got Successfully Registered")
                        print("*******************************************************")
                        
                except:
                    print("*******************************************************")
                    print("Something Went Wrong")
                    print("*******************************************************")
                    return render_template("SignUp.html")
                finally:
                    print("*******************************************************")
                    print(username + " You Got Successfully Registered")
                    print("*******************************************************")
                    flash("Successfully Registered")
                    return render_template("login.html")
        else:
            print("*******************************************************")
            print("Please Enter In Every Field")
            print("*******************************************************")
            flash("Please Enter In Every Field")
            return render_template("SignUp.html")


if __name__ == '__main__':
    app.run()
