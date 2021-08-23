from urllib.parse import parse_qsl
import pymongo
from bson.json_util import dumps
from pymongo.errors import DuplicateKeyError
from werkzeug import Response
from werkzeug.exceptions import abort
from models import Product
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb://0.0.0.0:27017")
client.db.products.create_index([("good_id", pymongo.ASCENDING)], unique=True)  # step 1
# print(list(client.db.products.index_information()))  # print ['_id_', 'good_id_1']


@app.route('/')
def mainPage():
    return render_template('index.html')


@app.route('/products', methods=['GET', 'POST'])
def allProducts():
    """ Get all the goods that are in database or Add goods in DB """
    if request.method == 'GET':
        """ Sort Products by parameters. For example:
             </products/?arg1=good_id&arg2=0> or
             </products/?arg1=product_name>
             """
        return getSortProduct(request.full_path.split('?')[1])
    elif request.method == 'POST':
        # start to create a new product
        all_datas = request.get_json()
        try:
            product_name = all_datas["product_name"]
            description = all_datas["description"]
            params = all_datas["params"]
        except KeyError as ke:
            error_message = dumps({'message': 'element with parameters: ' + str(ke) + ' not found'})
            abort(Response(error_message, 415))

        return makeANewProduct(product_name, description, params)


@app.route('/products/<int:id>', methods=['GET'])
def productsDetailsId(id):
    """ Return all details of product by id"""
    return getProductById(id)


def makeANewProduct(product_name, description, params):
    """ Make a new product """
    try:
        good = Product(id=next(Product._ids), product_name=product_name, description=description, params=params)
    except DuplicateKeyError as dke:
        error_message = dumps({'message': 'duplicated key errpr: ' + str(dke)})
        abort(Response(error_message, 415))
    good.save_data(client, good.serialize)
    return jsonify(good.serialize)


def getProductById(id):
    """ get products by unique id """
    try:
        dumps(list(client.db.products.find({'good_id': id}))[0])
    except (TypeError, IndexError):
        error_message = dumps({'message': 'good with id ' + str(id) + ' not found'})
        abort(Response(error_message, 415))

    return dumps(list(client.db.products.find({'good_id': id}))[0], default=str)
    # return json.dumps(list(client.db.products.find({'good_id': id}))[0], default=str)
    # return Product.db.products.find(ObjectId(id))


def getSortProduct(sort):
    """ Get sorted list using 'sort' parameters """
    params = parse_qsl(sort)
    if len(params) == 1 and params[0][1] == 'product_name':
        docs = list(client.db.products.find())
        res = sorted(docs, key=lambda product: product['product_name'])
        return dumps(res)
    elif len(params) == 2:
        try:
            mean_of_param = int(params[1][1])
        except TypeError:
            mean_of_param = int(params[1][1])

        element = list(client.db.products.find({params[0][1]: mean_of_param}))
        if not element:
            error_message = dumps({'message': 'element wih parameters: ' + str(sort) + ' not found'})
            abort(Response(error_message, 415))
        return dumps(list(client.db.products.find({params[0][1]: mean_of_param})))
        # return json.dumps(list(client.db.products.find({params[0][1]: mean_of_param})), default=str)
    else:
        error_message = dumps({'message': 'parameters in URL: ' + str(sort) + ' are not valid'})
        abort(Response(error_message, 415))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
