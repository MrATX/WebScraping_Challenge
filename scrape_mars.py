def scrape():
    from splinter import Browser
    from bs4 import BeautifulSoup
    import cssutils
    import pandas as pd
    import pymongo
    import time
    #Setup browser
    executable_path = {'executable_path':'C:/Users/JayDub/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    #Grab news article stuffs
    #Route to site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve Top News Article
    articles = soup.find('li', class_='slide')
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    container = articles.find('div', class_="image_and_description_container")
    text = container.find('div', class_="list_text")
    news_title = text.find('div',class_="content_title")
    news_title = news_title.find('a')
    news_title = news_title.text.strip()
    news_p = container.find('div',class_="article_teaser_body")
    news_p = news_p.text.strip()
    news_article = {
        'article_title':news_title,
        'article_descrip':news_p
    }
    #Get featured image url
    #Route to site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve header containing featured image
    image_container = soup.find('article', class_='carousel_item')
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    featured_image_url = image_container['style']
    style = cssutils.parseStyle(featured_image_url)
    featured_image_url = style['background-image']
    featured_image_url = featured_image_url.replace('url(', '').replace(')', '')
    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image_url}')
    featured_image = {
        'featured_img_url':featured_image_url
    }
    #Get facts table
    url = "https://space-facts.com/mars/"
    fact_table = pd.read_html(url)
    fact_table = fact_table[0]
    fact_table.columns=["Parameter","Mars"]
    fact_table.set_index("Parameter",inplace=True)
    fact_table_HTML = fact_table.to_html()
    fact_table_HTML = fact_table_HTML.replace("\n","")
    facts_table = {
        "table_code":fact_table_HTML
    }
    #Get hemispheres stuffs
    #Route to site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve header containing featured image
    hemispheres = soup.find_all('div', class_='item')
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    #featured_image_url = image_container['style']
    hemispheres_list = []
    for item in hemispheres:
        descrip = item.find('div',class_='description')
        image_title = descrip.find('h3')
        image_title = image_title.text.strip()
        img_url = item.find('a',class_="itemLink product-item")
        img_url = img_url['href']
        img_url = (f"https://astrogeology.usgs.gov{img_url}")
        descrip = descrip.find('p')
        descrip = descrip.text.strip()
        browser.visit(img_url)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('div',class_="downloads")
        img_url = img_url.find('a')
        img_url = img_url['href']
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(5)
        hemis_dict = {
            'hemi_title':image_title,
            'hemi_img_url':img_url,
            'hemi_img_descrip':descrip
        }
        hemispheres_list.append(hemis_dict)
    #Create dictionary of dictionaries to pass
    mars_intel = {"article_info":news_article,"featured_image":featured_image,"hemispheres":hemispheres_list,"facts_table":facts_table}
    #Update MongoDB
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.mars.drop()
    db.mars.insert_one(mars_intel)
    return mars_intel