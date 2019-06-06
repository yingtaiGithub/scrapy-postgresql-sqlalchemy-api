from collections import OrderedDict

from flask import Flask, jsonify
from flask_restful import Api
from flask_restful import Resource, reqparse, abort
from sqlalchemy.orm import sessionmaker

from scrapy_spider.models import db_connect, Products


class GetProducts(Resource):
    def __init__(self, **kwargs):
        super(GetProducts, self).__init__(*kwargs)
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def get(self):
        all_products = self.Session().query(Products).all()
        results = [OrderedDict([('url', product.url), ('min_price', product.min_price), ('avg_price', product.avg_price)]) for
                   product in all_products]
        data = {'status': 200, 'result': results}

        return data

        # parser = reqparse.RequestParser()
        # parser.add_argument('title', type=str)
        # parser.add_argument('image_path', type=str)
        # title = parser.parse_args().get('title')
        # image_path = parser.parse_args().get('image_path')
        # print(title, image_path)


app = Flask(__name__)
api = Api(app)

api.add_resource(GetProducts, '/products')

app.run(debug=True)
