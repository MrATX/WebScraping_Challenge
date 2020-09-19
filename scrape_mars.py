def scrape():
    from splinter import Browser
    from bs4 import BeautifulSoup
    import cssutils
    import pandas as pd
    #Retrieve Article Info
    executable_path = {'executable_path':'C:/Users/JayDub/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find('li', class_='slide')
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
    #Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_container = soup.find('article', class_='carousel_item')
    featured_image_url = image_container['style']
    style = cssutils.parseStyle(featured_image_url)
    featured_image_url = style['background-image']
    featured_image_url = featured_image_url.replace('url(', '').replace(')', '')
    featured_image_url = (f'{url}{featured_image_url}')
    featured_image = {
        'featured_img_url':featured_image_url
    }
    #Facts Table
    url = "https://space-facts.com/mars/"
    fact_table = pd.read_html(url)
    fact_table = fact_table[0]
    fact_table.columns=["Parameter","Mars"]
    fact_table.set_index("Parameter",inplace=True)
    fact_table_HTML = fact_table.to_html()
    fact_table_HTML = fact_table_HTML.replace("\n","")
    fact_table_HTML = fact_table.to_html("mars_facts_table.html")
    #Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemispheres_list = []
    for item in hemispheres:
        descrip = item.find('div',class_='description')
        image_title = descrip.find('h3')
        image_title = image_title.text.strip()
        image_url = item.find('img',class_='thumb')
        image_url = image_url['src']
        image_url = (f'{url}{image_url}')
        descrip = descrip.find('p')
        descrip = descrip.text.strip()
        hemis_dict = {
            'hemi_title':image_title,
            'hemi_img_url':image_url,
            'hemi_img_descrip':descrip
        }
        hemispheres_list.append(hemis_dict)
        #Assemble Master Dictionary
        dict_of_dict = {"article_info":news_article,"featured_image":featured_image,"hemispheres":hemispheres_list}

        return dict_of_dict