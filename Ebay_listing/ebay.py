from requests_html import HTMLSession
import csv
s = HTMLSession()
def product_links(page):
    url = f"https://www.ebay.com/b/Fragrances-for-Women/11848/bn_693859?_pgn={page}"

    r =s.get(url)
    links = []
    products = r.html.find("ul.b-list__items_nofooter li")

    for item in products:
        links.append(item.find("a", first=True).attrs["href"])
    return links

def parse(url):

    r = s.get(url)
    try:
        title = r.html.find("h1.x-item-title__mainTitle", first=True).text
    except AttributeError as err:
        title = "None"
    try:
        price = r.html.find("div.x-bin-price__content", first=True).text
    except AttributeError as err:
        price = "None"
        
    try:
        quantity = r.html.find("div.d-quantity__availability", first=True).text
    except AttributeError as err:
        quantity = "None"
        
    try:
        feedback =  r.html.find("div.d-stores-info-categories__container__info__section__item", first=True).text
    except AttributeError as err:
        feedback = "None"
        
    try:
        seller =  r.html.find("div.d-stores-info-categories__container__info__section__title", first=True).text
    except AttributeError as err:
        seller = "None"
    
    product = {
        "title": title,
        "price": price,
        "quantity": quantity,
        "seller": seller,
        "feedback": feedback
        
    }
    return product

def save_to_csv(results):
    keys = results[0].keys()
    
    with open("fragrance.csv", 'w', encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
results = []
for x in range(1,2):
    print(f"getting page: {x}")
    links = product_links(x)
    for url in links:
        results.append(parse(url))
        print(results)
    save_to_csv(results)