from file_handler import *
from bs4 import BeautifulSoup


    # Constantes 
BTS_HOME = "http://books.toscrape.com/index.html"
BTS_BASE = "http://books.toscrape.com/"
BTS_CATALOGUE = "http://books.toscrape.com/catalogue/"

def addBookData(url):
    # fonction qui récupere les donées d"un livre depuis son url

    response = get(url)

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
    number_avaible = search('\d+',number_avaible).group()

    rating = soup.find('article').findAll('p')
    for node in rating:
        if search('star-rating' , str(node['class'])):
            rating = node['class']
            rating = rating[1]
            break

    img_url = soup.find('img')
    img_url = img_url['src']
    img_url = BTS_BASE + sub("../","",img_url,2)
    
    category = soup.find('ul' , {'class' : 'breadcrumb'}).findAll('li')
    category = category[2].find('a').text

    desc_proof = soup.find('div', {'id' : "product_description"})
    product_description = ''
    if desc_proof != None:
        description_finder = soup.find('article')
        description_finder = description_finder.findAll('p')
        for x in description_finder:
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

def getAllBooksFromCategory(url, category_name, index):
    # fonction permettant de parcourire tous les livres d'une categories depuis son url et d'en sortir le lien de chaque livre

    response = get(url)

    if not response.ok:
        print('Error response is not 200')
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    nbr_result = soup.find('form').find('strong').text

    bookList = soup.find('ol').findAll('li')
    
    if index == 0:
        createCsv(category_name)

    for book in bookList:
        book = book.find('a')
        book = book['href']
        bookUrl = search('[\w,.,-]*[/][\w,.,-]*$' , book)
        bookUrl = BTS_CATALOGUE + bookUrl[0]
        print(bookUrl)
        addBookData(bookUrl)
    
    if int(int(nbr_result)/20 - (index)) > 0:   # c'est bien la partie entière et non le reste que je veux, je ne peux pas donc utiliser le modulo (meme si mon calcul est de la forme a = bx + q qui semble ressembler a un modulo mais c'est un piege)
        pager = soup.findAll('ul')                 # ex: avec 35 résultat : 35%20 = 15 alors que l'on veux 35/20 = 1 car 35 = 20 * 1 + 15 (div Euclidienne)                                   
        page_link = ''                             # Par ailleur le modulo me donne donc le nombre de resultat sur la denriere page et non le nombre de page
        for page in pager:
            if page.get('class') != None and page.get('class') == ['pager']:
                page_link = page.findAll('li')
                for link in page_link:
                    if link.get('class') != None and link.get('class') == ['next']:
                        page_link = link.find('a')
                        page_link = page_link['href']
                        break
                break
        
        url = sub("[\w,.,-]*$",page_link,url,1)
        getAllBooksFromCategory(url,category_name, index+1)
    

def getAllBookFromAllCategory():
    # Fonction qui parcoure les categories de livres du site et en sort chaque lien de chaque categorie

    response = get(BTS_HOME)

    if not response.ok:
        print('Error response is not 200')
        return
    
    soup = BeautifulSoup(response.text,'html.parser')

    nav = soup.find('aside').find('ul').find('ul').findAll('li')

    for category in nav:
        category = category.find('a')
        category_name = search('([\w]+[ {1}]*)+' , category.text).group()
        category_link = BTS_BASE + str(category['href'])
        getAllBooksFromCategory(category_link , category_name , 0)

print(__name__ + " was imported")