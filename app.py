from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_db"
mongo=PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template(
        "index.html",
        mars=mars,
    )

@app.route("/scrape")
def scraper():
    mars=mongo.db.mars
    mars_update = scrape_mars.scrape()
    mars.update({},mars_update,upsert=True)
    return redirect(url_for('index'),code=302)

if __name__=="__main__":
    app.run(debug=True)