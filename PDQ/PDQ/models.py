from PDQ import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	user_role = db.Column(db.String(120), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='restaurant.png')
	password = db.Column(db.String(60), nullable=False)
	store = db.relationship('Store', backref='manager', lazy=True)
	
	
	def __repr__(self):
		return '<User {}>'.format(self.title, self.first_name, self.last_name, self.email, self.user_role)
	
		
class Store(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	branch = db.Column(db.String(100), nullable=False) 
	address = db.Column(db.String(100), nullable=False) 
	type = db.Column(db.String(100), nullable=False)
	TQvalue = db.Column(db.Float, nullable=False)
	manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	factory_inventory = db.relationship('fInventory', backref='place', lazy=True)
	store_inventory = db.relationship('sInventory', backref='place', lazy=True)
	
	def __repr__(self):
		return '<Store {}>'.format(self.branch, self.type, self.TQvalue)
	
		
class Stock(db.Model):
	id = db.Column(db.Integer, primary_key=True,)
	name = db.Column(db.String(100), nullable=False)
	unit = db.Column(db.Text, nullable=False)
	stock_for = db.Column(db.String(100), nullable=False)
	factory_inventory_item = db.relationship('fInventory', backref='item', lazy=True)
	store_inventory_item = db.relationship('sInventory', backref='item', lazy=True)
	
	def __repr__(self):
		return '<Stock {}>'.format(self.name, self.unit)

class sInventory(db.Model):
	stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key=True)
	store_id = db.Column(db.Integer, db.ForeignKey('store.id'), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	unit = db.Column(db.Text, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='pizza.jpg')
	last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Store Inventroy {}>'.format(self.name, self.amount, self.last_update)
		
class fInventory(db.Model):
	stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key=True)
	store_id = db.Column(db.Integer, db.ForeignKey('store.id'), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	unit = db.Column(db.Text, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='pep.png')
	last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Factory Inventroy {}>'.format(self.name, self.amount, self.last_update)
	
class Vendor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	address = db.Column(db.String(120), nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	
	def __repr__(self):
		return '<Vendor {}>'.format(self.email, self.address, self.contact)