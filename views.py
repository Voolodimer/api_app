import os
import uuid

from bson import ObjectId

from models import Product
from flask import Flask, request, jsonify
from pymongo import MongoClient

# from flask_pymongo import PyMongo

app = Flask(__name__)
# storage = Product("localhost", 27017)
client = MongoClient("mongodb://0.0.0.0:27017")
Product.db = client.products_db

# for db_info in client.list_database_names():
#     print(db_info)

# Test mongo
pr = Product()

# for _ in range(3):
#     dto = {
#         "id": str(uuid),
#         'payload': str(uuid),
#     }
#     pr.save_data(dto)

i = 0

for data in pr.get_data():
    # print(i, data['_id'])
    Product.db.find(ObjectId('611f952bd8c503ae746f0985'))
    i += 1


# @app.route('/')
# def mainPage():
#     return "Hello!"
#
#
# @app.route('/products', methods=['GET', 'POST'])
# def allProducts():
#     """ Get all the goods that are in stock or Add goods in DB """
#     if request.method == 'GET':
#         return getAllProducts()
#
#     elif request.method == 'POST':
#         print("Making new good")
#         product_name = request.args.get('product_name')
#         description = request.args.get('description')
#         params = request.args.get('params')
#         return makeANewProduct(product_name, description, params)
#
#     return "Add or Show goods"
#
#
# @app.route('/products/<int:id>', methods=['GET'])
# def productsDetailsId(id):
#     """ Return all details of goods """
#     return getProductById(id)
#
#
# def getAllProducts():
#     # puppies = session.query(Puppy).all()
#     # Получить все данные
#     return jsonify(Products=[i.serialize for i in Product.db.statistics.find()])
#
#
# def makeANewProduct(product_name, description, params):
#     good = Product(product_name, description, params)
#     return jsonify(Product=good.serialize)
#
#
# def getProductById(id):
#     return Product.db.find(ObjectId(id))
#
#
# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5000)
