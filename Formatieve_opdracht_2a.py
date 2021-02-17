import MongodbDAO

# Informatie tonen over wat data
db = MongodbDAO.getMongoDB()
collectionsNames = db.list_collection_names()
for collectionName in collectionsNames:
    collection = db.get_collection(collectionName)
    #print(f'Collection {collectionName} contains {collection.estimated_document_count()} documents')


"""shows the first document in the Mongodb database"""
products = MongodbDAO.getDocuments('products')
# products is een cursor
print(f'the first document in the database : {products.next()["name"]} price: {products.next()["price"]["selling_price"]}')


"""shows the first product starting with the letter "R" in de database"""
products = MongodbDAO.getDocuments("products")
for product in products:
    if product['name'][0] == 'R':
        print(f'the first product in the list starting with the letter "R" : {product["name"]}')
        break


"""calculates the avrage price of all the items in the database in cents"""
products = MongodbDAO.getDocuments("products")
total = 0
for product in products:
    try :
        total += product["price"]["selling_price"]
    except:
        continue
print(f"average price of all the items in the database in cents : {round(total/db.get_collection('products').estimated_document_count())}")
