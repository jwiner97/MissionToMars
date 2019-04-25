from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_App")


@app.route('/')
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()

    mars_dict = {
        "news_title": mars["news_title"],
        "news_p": mars["news_p"],
        "featured_image_url": mars["featured_image_url"],
        "mars_weather": mars["mars_weather"],
        "table_html": mars["table_html"],
        "hemisphere_image_urls": mars["hemisphere_image_urls"]
    } 
    # Insert mars_dict into database
    mongo.db.collection.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)    


if __name__ == "__main__":
    app.run(debug=True)
