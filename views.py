import json
import os
import uuid
from urllib.parse import parse_qsl

import pymongo
from bson import ObjectId, json_util
from werkzeug import Response
from werkzeug.exceptions import abort

from models import Product
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_pymongo import PyMongo


# app = Flask(__name__, template_folder={path of template directory})
app = Flask(__name__)
client = MongoClient("mongodb://0.0.0.0:27017")
# app.config["MONGO_URI"] = "mongodb://localhost:27017/products"
# mongo = PyMongo(app)
db_name = 'products'

# for db_info in client.list_database_names():
#     print(db_info)

# Test mongo

# client.db.products.insert_one({'good_id': 0, 'product_name': 'smartPhone1', 'description': "new sf from Rus", 'params': [{'1': '3', '3': '8'}]}).inserted_id

client.db.products.create_index([("good_id", pymongo.ASCENDING)], unique=True)  # step 1
print(list(client.db.products.index_information()))  # print ['_id_', 'good_id_1']
# print(list(client.db.products.find({"age": 35})))
# print(list(client.db.products.find())) # поиск всего содержимого

# Test of writing in db
# new = Product(id=next(Product._ids), product_name="sds", description="wewe", params=[{'1': '2', '3': '4'}])
# new2 = Product(id=next(Product._ids), product_name="sds2", description="wewe", params=[{'1': '2', '3': '4'}])
# new.save_data(client, new.serialize)
# new2.save_data(client, new2.serialize)

# for _ in range(3):
#     dto = {
#         "id": str(uuid),
#         'payload': str(uuid),
#     }
#     pr.save_data(dto)


# i = 0
# for data in list(client.db.products.find()):
#     # print(i, data['_id'])
#     print(data)
#     i += 1

# with app.app_context():
#     print([jsonify(i) for i in list(client.db.products.find())])

@app.route('/')
def mainPage():
    return render_template('index.html')


@app.route('/products', methods=['GET', 'POST'])
def allProducts():
    """ Get all the goods that are in stock or Add goods in DB """
    # Прикрутить сортировку
    if request.method == 'GET':
        return getAllProducts()

    elif request.method == 'POST':
        print("Making new good")
        all_datas = request.get_json()
        # print(all_datas, type(all_datas))
        product_name = all_datas["product_name"]
        description = all_datas["description"]
        params = all_datas["params"]
        # print(product_name, description, params)
        return makeANewProduct(product_name, description, params)


@app.route('/products/')
def sortProducts():
    """ Sort Products by <sort> """
    return getSortProduct(request.full_path.split('?')[1])


@app.route('/products/<int:id>', methods=['GET'])
def productsDetailsId(id):
    """ Return all details of goods """
    return getProductById(id)


def getAllProducts():
    # Получить все данные
    all_products = [i for i in list(client.db.products.find())]
    return json.dumps(all_products, default=str)


def makeANewProduct(product_name, description, params):
    good = Product(id=next(Product._ids), product_name=product_name, description=description, params=params)
    client.db.products.insert_one(good.serialize)
    return jsonify(good.serialize)


def getProductById(id):
    try:
        json.dumps(list(client.db.products.find({'good_id': id}))[0], default=str)
    except Exception as e:
        print(e)
        error_message = json.dumps({'message': 'good with id ' + str(id) + ' not found'})
        abort(Response(error_message, 415))

    return json.dumps(list(client.db.products.find({'good_id': id}))[0], default=str)
    # return Product.db.products.find(ObjectId(id))


def getSortProduct(sort):
    # fragment = urldefrag(url).fragment
    # params = dict(parse_qsl())
    params = parse_qsl(sort)
    if len(params) == 1 and params[0][1] == 'product_name':
        docs = list(client.db.products.find())
        res = sorted(docs, key=lambda product: product['product_name'])
        return json.dumps(res, default=str)
    elif len(params) == 2:
        try:
            mean_of_param = int(params[1][1])
        except TypeError:
            mean_of_param = int(params[1][1])
        return json.dumps(list(client.db.products.find({params[0][1]: mean_of_param})), default=str)
    else:
        error_message = json.dumps({'message': 'parameters in URL: ' + str(sort) + ' not valid'})
        abort(Response(error_message, 415))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
