import pymongo
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def scrape(): 
    
    # NASA MARS NEWS 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")

    header = results.find('div',class_ = "content_title") 
    headers = header.find('a').text
    
    summary = results.find('div',class_ = "rollover_description")
    summaries= summary.find('div').text
    
    # JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')
    link1 = soup1.find('article', class_='carousel_item')
    link_a = link1.find('a')
    link = link_a['data-fancybox-href'] 

    featured_image_url = 'https://www.jpl.nasa.gov' + link

     browser.quit()

    # Mars Weather

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(15)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    tweet1 = soup2.find_all('div',
            class_ = 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_vector = tweet1[0]

    mars_weather = mars_vector.find('span',
            class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    browser.quit()

    #Mars Facts 

    url3 = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(url3)
    mars_tables_df = mars_tables[0]

    mars_tables_df = mars_tables_df.rename(columns = {0:'Parameters', 1:'Value'})

    #Mars Hemispheres 

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)  

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    images2 = soup3.find_all('img',class_='thumb')  

    hemisphere_image_urls = []
    for image in images2: 
        title1 = image['alt']
        urls = image['src']
    
        hemisphere_image_urls.append({'title': title1, 'image_url': urls})

     browser.quit()

    return Complete_Dictionary = { 'Title': headers, 'summary':Summaries, 'Image_URL' : featured_image_url, 'Tweet' : mars_weather, 'Table' : mars_tables_df, "URLS" : hemisphere_image_urls }
