from requests import get
from csv import writer
from re import search
from re import sub

def createCsv(file_name):
    # Fonction permettant de creer le fichier csv et d'initialiser les colonnes

    file_name = sub("\s","_",file_name)
    with open("./BookData/" + str(file_name) + '.csv','w',newline='') as csv_file:
        f_writer = writer(csv_file)
        f_writer.writerow([
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
    # Ecrit le contenu d'un tableau dans un fichier csv avec son nom passer en parametre

    file_name = sub("\s","_",file_name)
    with open("./BookData/" + str(file_name) + '.csv','a',newline='') as csv_file:
        f_writer = writer(csv_file)
        f_writer.writerow([
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
    # Telecharge et ecrit une image depuis son url

    book_name = sub("\s","_",book_name)
    with open("./Img/" + book_name + ".jpg","wb") as f:
        f.write(get(img_url).content)


print(__name__ + " was imported")