from itertools import count
from pymodm import MongoModel, fields


class Product(MongoModel):
    ids = count(0)

    id = fields.IntegerField(primary_key=True)
    product_name = fields.CharField()
    description = fields.CharField()
    params = fields.ListField()

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
