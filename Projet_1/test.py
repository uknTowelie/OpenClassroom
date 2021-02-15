import requests
from bs4 import BeautifulSoup
import csv
import re

def createCsv():

    with open('data.csv','w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            'product_page_url',
            'upc',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url'
        ])

def addToCsv(table):
    
    with open('data.csv','a',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            table[0],
            table[1],
            table[2],
            table[3],
            table[4],
            table[5],
            table[6],
            table[7],
            table[8],
            table[9]
        ])


def addBookData(url):

    response = requests.get(url)

    if not response.ok:
        print('Error response is not 200')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text
        
    table = soup.findAll('tr')

    upc = table[0].find('td').text

    product_type = table[1].find('td').text
        
    price_excluding_tax = table[2].find('td').text
    price_excluding_tax = price_excluding_tax[1:]

    price_including_tax = table[3].find('td').text
    price_including_tax = price_including_tax[1:]

    number_avaible = table[5].find('td').text
    number_avaible = re.search('\d+',number_avaible).group()

    rating = soup.find('article')
    rating = rating.findAll('p')
    for x in rating:
        if re.search('star' , str(x['class'])):
            rating = x['class']
            rating = rating[1]
            break

    img_url = soup.find('img')
    img_url = img_url['src']

    category = soup.find('ul')
    category = category.findAll('li')
    category = category[2].find('a').text

    product_description = soup.find('article')
    product_description = product_description.findAll('p')

    for x in product_description:
        if x.get('class') == None:
            product_description = x.text
            break

    table = []
    table.append(url)
    table.append(upc)
    table.append(title)
    table.append(price_including_tax)
    table.append(price_excluding_tax)
    table.append(number_avaible)
    table.append(product_description)
    table.append(category)
    table.append(rating)
    table.append(img_url)

    addToCsv(table)


# ---------- Main -----------#
createCsv()

addBookData('http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html')



    
    




