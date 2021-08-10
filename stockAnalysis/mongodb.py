from pymongo import MongoClient
import pprint

def find_all_tickers(collection):
    stocks = []
    for row in collection.find({}, {'tiker':1, '_id':0}):
        stocks.append(row['tiker'])
    return stocks


if __name__ == "__main__":
    client = MongoClient('mongodb+srv://host:1314@clusterstock.uemua.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    #get database
    mongodb = client.stock
    #get collection
    stocks = mongodb.stocks
    #find by colum
    stocks = find_all_tickers(stocks)
    print(stocks)