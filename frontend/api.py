from flask import Flask, jsonify, request, render_template, flash
import client

app = Flask(__name__)

app.secret_key = "key"

db, db1 = client.connect_with_mongoDb()
ClientStub = client.conncet_with_server()


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
        if (username and password and db):
            queryObject = {'Name': username, 'Password': password}
            query = db.users.find_one(queryObject)
            if (query):
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


@app.route("/Movie_Name", methods=['GET', 'POST'])
def fetch():
    if request.method == "POST":
        name = request.form["MovieName"]

        if name:

            try:
                print(ClientStub)
                Movie = ClientStub.getrecommend(name)
                print(Movie)
                json_movie = []
                print("Fetching")

                for movie in Movie:
                    queryObject = {"title": movie}
                    query = db1.movies_metadata.find_one(queryObject, {"revenue": 1, "runtime": 1})
                    query.pop('_id')
                    json_movie.append(query)
                    print(json_movie)

                return json_movie

            except:
                return render_template("Home.html")
            finally:
                return render_template("Result.html", data=json_movie)


@app.route("/Register", methods=['GET', 'POST'])
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
                    "Name": username,
                    "Password": password
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
