import MongodbDAO

# Informatie tonen over wat data
db = MongodbDAO.getMongoDB()
collectionsNames = db.list_collection_names()
for collectionName in collectionsNames:
    collection = db.get_collection(collectionName)
    #print(f'Collection {collectionName} contains {collection.estimated_document_count()} documents')



products = MongodbDAO.getDocuments('products')
# products is een cursor
print(f'first document = {products.next()["name"]} price: {products.next()["price"]["selling_price"]}')


products = MongodbDAO.getDocuments("products")
for product in products:
    if product['name'][0] == 'R':
        print(product['name'])
        break

products = MongodbDAO.getDocuments("products")
total = 0
for product in products:
    try :
        total += product["price"]["selling_price"]
    except:
        continue

print(f"average price of the database in cents : {round(total/db.get_collection('products').estimated_document_count())}")
