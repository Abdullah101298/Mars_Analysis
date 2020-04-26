from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
     
    mars_dict = mongo.db.mars_dict.find_one()

    return render_template("index.html", mars_dict = mars_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_data():
    mars_dict = mongo.db.mars_dict 

    mars_data = scrape_mars.scrape_data()
    mars_dict.replace_one({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
