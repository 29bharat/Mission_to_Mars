from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
    executable_path = {"chromedriver.exe"}
    browser = Browser('chrome', executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        # "hemispheres": hemispheres(),
        "last_modified": dt.datetime.now()
    }

    return data
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# def hemispheres():
#     title = ['kitty1','kitty2','kitty3','kitty4']
#     img_url = ['https://live.staticflickr.com/3397/3551189653_501acccd41_b.jpg','https://live.staticflickr.com/3397/3551189653_501acccd41_b.jpg','https://live.staticflickr.com/3397/3551189653_501acccd41_b.jpg','https://live.staticflickr.com/3397/3551189653_501acccd41_b.jpg']

#     dhems = [{k,v} for k ,v in zip(title, img_url)]
    
#     # Convert dataframe into HTML format, add bootstrap
#     df=pd.DataFrame(dhems)
#     return df.to_html

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

# mars_data = scrape_all()
# print(mars_data)