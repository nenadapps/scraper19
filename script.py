from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen

def get_html(url):
    
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #hdr)
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('.PriceUser p')[0].get_text().strip()
        stamp['price'] = price.replace('Your Price US $', '').replace(',', '').strip()
    except: 
        stamp['price'] = None

    try:
        title = html.select('.DetailTitle')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        sku = html.select('.invNumberDetail')[0].get_text().strip()
        stamp['sku'] = sku.replace('Item #:', '').strip()
    except:
        stamp['sku'] = None    
        
    try:
        condition = html.select('.LabelText')[0].get_text().strip()
        stamp['condition'] = condition.replace('Condition', '').strip()
    except:
        stamp['condition'] = None 
        
    try:
        country_cont = html.select('.BreadCrumb')[0]
        country = country_cont.select('a')[2].get_text().strip()
        stamp['country'] = country
    except:
        stamp['country'] = None        

    stamp['currency'] = "USD"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('form td td img')
        for image_item in image_items:
            img_src = image_item.get('src')
            img = 'https://www.huntstamps.com/' + img_src
            if img not in images and '.gif' not in img_src:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    try:
        raw_text = html.select('.ProductDetails')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('td a.head2'):
            item_link = 'https://www.huntstamps.com' + item.get('href').replace('&amp;', '&').strip()
            if item_link not in items:
                items.append(item_link)
    except:
        pass

    try:
        next_items = html.select('a.NavBar')
        for next_item in next_items:
            next_item_text = next_item.get_text().strip()
            if 'Next' in next_item_text:
                next_url = 'https://www.huntstamps.com' + next_item.get('href')
                break
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories(category_url, check_string, cat_class):
    
    items = []

    try:
        html = get_html(category_url)
    except:
        return items

    try:
        for item in html.select('a.' + cat_class):
            item_link = 'https://www.huntstamps.com/' + item.get('href')
            if check_string in item.get('href'):
                items.append(item_link)
    except: 
        pass

    shuffle(items)
    
    return items

item_dict = {
'United States':'https://www.huntstamps.com/rhome1d.asp?Header=UnitedStates&x=',
'GB-Areas and British Colonies':'https://www.huntstamps.com/rhome1d.asp?Header=GB-AreasandBritish%20Coloni&x=',
'France-Areas and French Colonies':'https://www.huntstamps.com/rhome1d.asp?Header=France-AreasandFrenchColo&x=',
'Germany-Areas and German Colonies':'https://www.huntstamps.com/rhome1d.asp?Header=Germany-AreasandGermanCol&x=',
'Italy-Areas and Italian Colonies':'https://www.huntstamps.com/rhome1d.asp?Header=Italy-AreasandItalianColo&x=',
'Other Worldwide Regions':'https://www.huntstamps.com/rhome1d.asp?Header=OtherWorldwideRegions&x='
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose country: ')
            
category_url = item_dict[selection]
categories = get_categories(category_url, 'redirect1.asp', 'HeadCat')
for category in categories:
    categories2 = get_categories(category, 'redirect2.asp', 'HeadSub')
    for category2 in categories2:
        page_items, page_url = get_page_items(category2)
        for page_item in page_items:
            stamp = get_details(page_item)