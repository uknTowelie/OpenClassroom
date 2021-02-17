import requests
from bs4 import BeautifulSoup
from os.path import basename
import csv
import re

def createCsv(file_name):
    file_name = re.sub("\s","_",file_name)
    with open("./BookData/" + str(file_name) + '.csv','w',newline='') as csv_file:
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

def addToCsv(table, file_name):
    file_name = re.sub("\s","_",file_name)
    with open("./BookData/" + str(file_name) + '.csv','a',newline='') as csv_file:
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

def writeImg(img_url,book_name):
    book_name = re.sub("\s","_",book_name)
    with open("./Img/" + book_name + ".jpg","wb") as f:
        f.write(requests.get(img_url).content)

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
        if re.search('star-rating' , str(x['class'])):
            rating = x['class']
            rating = rating[1]
            break

    img_url = soup.find('img')
    img_url = img_url['src']
    img_url = "http://books.toscrape.com/" + re.sub("../","",img_url,2)
    
    category = soup.find('ul')
    category = category.findAll('li')
    category = category[2].find('a').text

    desc_proof = soup.findAll('h2')
    for x in desc_proof:
        if x.text == ['Product Description']:
            desc_proof = True
        else:
            desc_proof = False

    product_description = ''
    if desc_proof == True:

        description_finder = soup.find('article')
        description_finder = description_finder.findAll('p')

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

    addToCsv(table,category)
    writeImg(img_url,title)

def getAllBooksFromCategory(url, category_name , index):

    response = requests.get(url)

    if not response.ok:
        print('Error response is not 200')
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    nbr_result = soup.find('form')
    nbr_result = nbr_result.find('strong').text

    bookList = soup.find('ol')
    bookList = bookList.findAll('li')
    
    if index == 0:
        createCsv(category_name)

    for x in bookList:
        x = x.find('h3')
        x = x.find('a')
        x = x['href']
        bookUrl = re.search('[\w,.,-]*[/][\w,.,-]*$' , x)
        bookUrl = 'http://books.toscrape.com/catalogue/' + bookUrl[0]
        print(bookUrl)
        addBookData(bookUrl)
    
    if int( int(nbr_result) / 20 - (index)) > 0:
        pager = soup.findAll('ul')
        page_link = ''
        for x in pager:
            if x.get('class') != None and x.get('class') == ['pager']:
                page_link = x.findAll('li')
                for y in page_link:
                    if y.get('class') != None and y.get('class') == ['next']:
                        page_link = y.find('a')
                        page_link = page_link['href']
                        break
                break
        
        url = re.sub("[\w,.,-]*$",page_link,url,1)
        getAllBooksFromCategory(url,category_name, index+1)
    

def getAllBookFromAllCategory():

    url = 'http://books.toscrape.com/index.html'

    response = requests.get(url)

    if not response.ok:
        print('Error response is not 200')
        return
    
    soup = BeautifulSoup(response.text,'html.parser')

    nav = soup.find('aside')
    nav = nav.find('ul')
    nav = nav.find('ul')
    nav = nav.findAll('li')

    for x in nav:
        x = x.find('a')
        
        category_name = re.search('([\w]+[ {1}]*)+' , x.text).group()
        
        category_link = 'http://books.toscrape.com/' + str(x['href'])
        
        getAllBooksFromCategory(category_link , category_name , 0)

        
        

# ---------- Main -----------#


#addBookData('http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html')

#getAllBooksFromCategory('http://books.toscrape.com/catalogue/category/books/default_15/index.html','Default',0)

getAllBookFromAllCategory()
    





