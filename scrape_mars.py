# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    latest_news = soup.find("li", class_="slide")
    news_title = latest_news.find(class_="content_title").text
    news_p = latest_news.find(class_="article_teaser_body").text

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image = soup.find("li", class_="slide")
    featured_image_fragment = featured_image.find(class_="fancybox")['data-fancybox-href']

    base_url = "https://www.jpl.nasa.gov"

    featured_image_url = base_url + featured_image_fragment

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.find("li", class_="js-stream-item").find("p", class_="tweet-text").text

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # Return a list of dataframes for any tabular data that Pandas found
    table = pd.read_html(url)[0]
    # Rename table columns
    table.rename(columns={0:"description", 1:"value"}, inplace=True)
    table_html = table.to_html(index=False)
    table_html = table_html.replace('\n', '')

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    base_url = "https://astrogeology.usgs.gov"

    links = [base_url + item.find(class_="description").a["href"] for item in soup.find_all("div",class_="item")]

    hemisphere_image_urls = []


    for url in links:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("div", class_="content").find("h2", class_="title").text.replace(" Enhanced","")
        img_url = base_url + soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({"title":title,"img_url":img_url})

    browser.quit()

    mars = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "table_html":table_html,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    return mars