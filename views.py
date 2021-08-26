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


@app.route('/products/<int:id>', methods=['GET'])
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
    return dumps(list(client.db.products.find({'good_id': id}))[0], default=str)


def get_sort_product(sort):
    """ Get sorted list using 'sort' parameters """
    def filter_func(param, key, value):
        """ filter list of parameters """
        i = 0
        while i < len(param):
            try:
                if param[i][key] == value:
                    return True
            except KeyError:
                i += 1
                continue
            i += 1

    # params is a list of tuples (key-value)
    params = parse_qsl(sort)
    # print(params[0][0])
    # if we get request like "/products" we will show all goods (without filter)
    if not params:
        docs = list(client.db.products.find())
        return dumps(docs)

    # if the passed parameter exists in 'parameters' list, we sort our db by key (params[0][0])
    if params[0][0] in parameters:
        docs = list(client.db.products.find())
        print(docs)
        # res = sorted(docs, key=lambda product: product[params[0][0]] == params[0][1])
        res = filter(lambda product: product[params[0][0]] == params[0][1], docs)
        return dumps(res)

    # if the passed parameter not exists in 'parameters' list, we sort our db by 'params'
    if params[0][0] not in parameters:
        docs = list(client.db.products.find())
        print(docs)
        res = list(filter(lambda x: filter_func(x['params'], params[0][0], params[0][1]), docs))
        return dumps(res)

    error_message = dumps({'message': 'parameters in URL: ' + str(sort) + ' are not valid'})
    abort(Response(error_message, 415))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
