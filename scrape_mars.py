from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    
    executable_path = {"executable_path": "C:/chromedriver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html_link = browser.html
    soup_file = bs(html_link,'html.parser')

    nasa_news_title = soup_file.find('div',class_='content_title').text
    print(f"News Title: {nasa_news_title}")

    # Extract Paragraph text
    nasa_news_paragraph=soup_file.find('div',class_='article_teaser_body').text
    print(f"News Paragraph: {nasa_news_paragraph}")

    jurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jurl)

    jhtml = browser.html
    print(jhtml)

    img_soup = bs(jhtml,"html.parser")
    print(jpl_soup)

    main_url ='https://www.jpl.nasa.gov'
    #get image url from the soup object.
    featured_image_url = img_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    #Create one full image url link
    featured_image_url=main_url+featured_image_url
    print(featured_image_url )

    facts_url = "https://space-facts.com/mars/"
    tables_facts = pd.read_html(facts_url)

    df_mars_facts = tables_facts[1]
    df_mars_facts

    html_table = df_mars_facts.to_html()
    html_table

    USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_url)
    html = browser.html

    soup = bs(html, 'html.parser')
    main_url = soup.find_all('div', class_='item')

    base_url = "https://astrogeology.usgs.gov"
    titles=[]
    hemi_urls=[]

    for url in main_url:
        title = url.find('h3').text
        url = url.find('a')['href']
        comb_url = base_url + url
    
        browser.visit(comb_url)
        html = browser.html
        img_soup = bs(html, 'html.parser')
        new_img = img_soup.find('div', class_ = 'downloads')
        new_img_url = new_img.find('a')['href']
    
        print(new_img_url)
        img_data=dict({'title':title, 'img_url':new_img_url})
        hemi_urls.append(img_data)

        print(hemi_urls)

    browser.quit()

    mars_data = {}

    # Append news_title and news_paragraph to mars_data.
    mars_data['news_title'] = nasa_news_title
    mars_data['news_paragraph'] = nasa_news_paragraph

    # Append featured_image_url to mars_data.
    mars_data['featured_image_url'] = featured_image_url

    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = df_mars_facts

    # Append hemisphere_image_urls to mars_data.
    mars_data['hemisphere_image_urls'] = hemi_urls

    print("Finished Scraping")

    return mars_data