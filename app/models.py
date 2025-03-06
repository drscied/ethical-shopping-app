from .extensions import db
from datetime import datetime
import json

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    political_affiliation = db.Column(db.String(50))
    trump_support_score = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='company', lazy=True)
    donations = db.relationship('PoliticalDonation', backref='donor_company', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    alternatives = db.relationship(
        'Product',
        secondary='product_alternative',
        primaryjoin='Product.id==ProductAlternative.product_id',
        secondaryjoin='Product.id==ProductAlternative.alternative_product_id',
        backref=db.backref('alternative_to', lazy='dynamic'),
        lazy='dynamic'
    )
    retail_locations = db.relationship('RetailLocation', backref='product', lazy=True)

class ProductAlternative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    alternative_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    similarity_score = db.Column(db.Float)
    _price_comparison = db.Column('price_comparison', db.Text)

    @property
    def price_comparison(self):
        return json.loads(self._price_comparison) if self._price_comparison else {}

    @price_comparison.setter
    def price_comparison(self, value):
        self._price_comparison = json.dumps(value)

class RetailLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    retailer_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)
    availability = db.Column(db.Boolean, default=True)
    location_type = db.Column(db.String(20))  # 'physical' or 'online'
    address = db.Column(db.String(200))
    url = db.Column(db.String(200))

class PoliticalDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recipient = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(200))
