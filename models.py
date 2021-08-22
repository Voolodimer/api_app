from itertools import count

from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from pymongo import MongoClient


class Product(MongoModel):
    _ids = count(0)

    # def __init__(self):
    #     self.id = next(self._ids)
    #     self.product_name = product_name
    #     self.description = description
    #     self.params = params

    id = fields.IntegerField(primary_key=True)
    product_name = fields.CharField()
    description = fields.CharField()
    params = fields.ListField()

    # write_concern = WriteConcern(j=True)

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


