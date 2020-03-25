# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt

#Define Functons

#Define mian Scraping system
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title, 
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.now()
            } 

    # Get Images for hemispheres        
    Hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris' ]
    DataHemispheres = {}
    for Mars_hemispheres in Hemispheres:
        DataHemispheres.update({Mars_hemispheres.replace(" ", "_"): Hem_URL(Mars_hemispheres, browser)})
    browser.quit()
    return data, DataHemispheres

def Hem_URL(Mars_hemispheres, browser):
    print(Mars_hemispheres)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    browser.is_element_present_by_text(Mars_hemispheres + 'Hemisphere Enhanced', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text(Mars_hemispheres + ' Hemisphere Enhanced')
    more_info_elem.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    img_url_rel = img_soup.select_one('div.downloads ul li a').get("href")
    return img_url_rel
    
    
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=3)
    
    
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:       
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        print(news_title)
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None
    return news_title, news_p


# Featured Images
def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
        
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    
    # Use the base URL to creae an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0] #1 has two columns
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']#, 'Earth']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
