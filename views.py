import sys
from itertools import count
from urllib.parse import parse_qsl

from bson.json_util import dumps
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from werkzeug import Response
from werkzeug.exceptions import abort
from flask import Flask, request, jsonify

from models import Product

app = Flask(__name__)
client = MongoClient("mongodb://0.0.0.0:27017")
client.db.products.create_index([("good_id", pymongo.ASCENDING)], unique=True)  # step 1
# print(list(client.db.products.index_information()))  # ['_id_', 'good_id_1']
parameters = ['good_id', 'product_name', 'description', 'params']
len_db = len(list(client.db.products.find()))
Product.ids = count(len_db)


@app.route('/')
def main_page():
    return jsonify({'main': 'page'})


@app.route('/products', methods=['GET', 'POST'])
def all_products():
    """ Get all the goods that are in database or Add goods in DB """
    if request.method == 'GET':
        # Sort Products by parameters or name. For example:
        #     </products?good_id=0> or </products?battery=li-ion>
        return get_sort_product(request.full_path.split('?')[1])

    if request.method == 'POST':
        # start to create a new product
        all_datas = request.get_json()
        try:
            product_name = all_datas["product_name"]
            description = all_datas["description"]
            params = all_datas["params"]
        except KeyError as key_err:
            error_message = dumps({'message': 'element with parameters: '
                                              + str(key_err) + ' not found'})
            abort(Response(error_message, 415))
        return make_a_new_product(product_name, description, params)

    error_message = dumps({'message': 'Method ' + request.method + ' is not supports'})
    return jsonify(error_message)


@app.route('/products/<int:product_id>', methods=['GET'])
def products_details_id(product_id):
    """ Return all details of product by id"""
    return get_product_by_id(product_id)


def make_a_new_product(product_name, description, params):
    """ Make a new product """
    try:
        good = Product(id=next(Product.ids), product_name=product_name,
                       description=description, params=params)
    except DuplicateKeyError as dke:
        error_message = dumps({'message': 'duplicated key errpr: ' + str(dke)})
        abort(Response(error_message, 415))
    good.save_data(client, good.serialize)
    return jsonify(good.serialize)


def get_product_by_id(product_id):
    """ get products by unique id """
    try:
        dumps(list(client.db.products.find({'good_id': product_id}))[0])
    except (TypeError, IndexError):
        error_message = dumps({'message': 'good with id ' + str(product_id) + ' not found'})
        abort(Response(error_message, 415))
    return dumps(list(client.db.products.find({'good_id': product_id}))[0], default=str)


def get_sort_product(sort):
    """ Get sorted list using 'sort' parameters """
    # params is a list of tuples (key-value)
    params = dict(parse_qsl(sort))
    query_keys = list(params.keys())
    docs = list(client.db.products.find())

    # if we get request like "/products" we will show all goods (without filter)
    if not params:
        if not docs:
            return jsonify({'message': 'Nothing found'})
        return dumps(docs)

    # checks all keys, and rename rename keys that are not in the 'parameter' list
    for key in query_keys:
        if key not in parameters:
            new_key = 'params.' + key
            params[new_key] = params.pop(key)

    docs = list(client.db.products.find({'$or': [params]}))

    if not docs:
        return jsonify({'message': 'Nothing found'})

    return dumps(docs)


if __name__ == '__main__':
    host_port = False
    try:
        host = sys.argv[1]
        port = sys.argv[2]
        host_port = True
    except IndexError:
        print("need to pass host and port")

    if host_port:
        app.debug = True
        app.run(host=host, port=port)

    else:
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
