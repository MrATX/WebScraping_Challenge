from flask import Flask, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/NAMEOFDBHERE"
mongo=PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars_intel.find_one()
    return render_template("index.html",mars_intel=mars_intel)

@app.route("/scrape")
def scraper():
    mars_intel=mongo.db.mars_intel
    mars_update = scrape_mars.scrape()
    mars_intel.update({},mars_update,upsert=True)
    return redirect(url_for('index'),code=302)

if __name__=="__main__":
    ap.run(debug=True)