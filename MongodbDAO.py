import pymongo

def getMongoDB(mongoConnectString = "mongodb://localhost:27017/", databaseName = 'huwebshop'):
    myclient = pymongo.MongoClient(mongoConnectString)
    return myclient[databaseName]

def getCollection(collectionName):
    return getMongoDB().get_collection(collectionName)

def getDocuments(collectionName, filter = {}):
    return getCollection(collectionName).find(filter)