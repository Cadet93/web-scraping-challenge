#!/usr/bin/env python
# coding: utf-8

# In[18]:


#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import time
import pandas as pd
import time


# In[19]:

def init_browser():
    # chrome browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:

def scrape_info():
    browser = init_browser()

    # URL of Mars news page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    browser.visit(url)


    # In[ ]:
    #add timer to prevent error
    time.sleep(2)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # In[ ]:


    # retrieve article title and paragraph text
    article = soup.find('div', class_='list_text')

    print(article)

    news_title = article.find('div', class_='content_title').find('a').text

    print(news_title)

    news_p = article.find('div', class_='article_teaser_body').text

    print(news_p)


    # In[ ]:


    # use splinter to visit JPL Featured Mars Image and store
    # URL of Mars news page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page with the requests module
    browser.visit(url)


    # In[ ]:


    # set html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    # find the featured image
    featured_article_image = soup.find('a', class_='button fancybox')[
        "data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_article_image

    print(featured_image_url)


    # In[ ]:


    # get table data from Mars facts website and store as HTML
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables


    # In[ ]:


    # save table into a DataFrame
    df = tables[0]

    df.head(20)

    table_html = df.to_html(header=False, index=False)



    # In[ ]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # In[ ]:


    # set html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the image and title for each hemisphere
    # Retrieve the parent divs for all articles
    results = soup.find_all('div', class_='item')

    print(results)

    # list to store hemisphere dictionaries
    hemisphere_data = []

    for result in results:
        try:

            # scrape the article header
            title = result.find('h3').text

            browser.click_link_by_partial_text(title)

            # set html.parser
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            image = soup.find('div', class_="downloads").find('a')['href']

            # Dictionary to be inserted into MongoDB
            hemi_dict = {
                'title': title,
                'image_url': image

            }

            print("----------")
            print(title)
            print(image)
            print(hemi_dict)

            hemisphere_data.append(hemi_dict)

            browser.back()

        except Exception as e:
            print(e)

    print("Final results -----------------")
    print(hemisphere_data)


    # In[ ]:


    # Store all scraped data in a dictionary
    mars_data = {
        "title": news_title,
        "paragraph": news_p,
        "featured_image_url": featured_image_url,
        "table_html": table_html,
        "hemisphere_data": hemisphere_data
    }

    print(mars_data)

    # close browser
    browser.quit()

    # return results
    return mars_data
