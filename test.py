from itertools import count
from pprint import pprint
import pymongo
from flask_pymongo import MongoClient
from bson.json_util import dumps
from pymodm import connect, fields, MongoModel
from pymongo import WriteConcern


class Product(MongoModel):
    _ids = count(0)

    id = fields.IntegerField()
    product_name = fields.CharField()
    description = fields.CharField()
    params = fields.ListField()

    # write_concern = WriteConcern(j=True)
    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'myApp'

    @property
    def serialize(self):
        """ return object data """
        return {
            'good_id': self.id,
            'product_name': self.product_name,
            'description': self.description,
            'params': self.params
        }

    def save_data(self, client_db, dto):
        return client_db.db.products.insert_one(dto)

    def get_data(self, client_db):
        return list(client_db.db.products.find())


client = MongoClient("mongodb://0.0.0.0:27017")
connect('mongodb://localhost:27017/myDb', alias='myApp')

db = client.myDb
cursor = db.myApp.find()
for document in cursor:
    print(document)

client.db.myApp.create_index([("good_id", pymongo.ASCENDING)], unique=True)  # step 1
print(list(client.db.products.index_information()))  # print ['_id_', 'good_id_1']

i = 0
print(list(client.myDb.myApp.find()))
for data in list(client.myDb.myApp.find()):
    # print(i, data['_id'])
    print('data: ', data)
    i += 1

# for _ in range(1):
#     dto = {
#         "good_id": 6,
#         'product_name': "Book",
#         'description': "best book",
#         'params': [{'1x': '2yw'}, {'33w': 'w4df'}, {'qf3': "fse"}]
#     }
#     client.db.products.insert_one(dto)

# sort
# docs = list(client.db.products.find())
#
# res = sorted(docs, key=lambda product: product['product_name'])
# for el in res:
#     print(el)

# print(client.db.products.find({'good_id': 0}))

# cursor = client.db.products.find({'good_id': 0})
# json_data = dumps(cursor)
# print(type(json_data))

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

for db_info in client.list_database_names():
    print(db_info)

# client.db.products.insert_one({'good_id': 0, 'product_name': 'smartPhone1', 'description': "new sf from Rus", 'params': [{'1': '3', '3': '8'}]}).inserted_id

# app.config["MONGO_URI"] = "mongodb://localhost:27017/products"
# mongo = PyMongo(app)


new_pr4 = Product(product_name='phone', description='new phone', params='all params').save()
print(new_pr4.serialize)

# print(new_pr4)
# new_pr1 = Product(id=1, product_name='phone', description='new phone', params='all params').save()
# new_pr2 = Product(id=1, product_name='phone', description='new phone', params='all params').save()
# print(new_pr2.serialize)
# print(new_pr4.serialize, new_pr1.serialize)
