from flask import render_template, flash, redirect, url_for, flash, request
from PDQ.forms import RegistrationForm, LoginForm, StockForm, UpdateVenderForm, StockUpdateForm, StoreForm
from PDQ import app, db, bcrypt, mail
from PDQ.models import User, Stock, Vendor, sInventory, fInventory, Store
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('account'))
		else:
			flash('Login unseccessfull. Please check email and password', 'danger')
	return render_template('login.html', title="Login", form=form)
	
@app.route("/stockpage")
def stockPage():
	stocks=Stock.query.all()
	image_file_factory = url_for('static', filename='pep.png')
	image_file_store = url_for('static', filename='pizza.jpg')
	return render_template('stockpage.html', stocks=stocks, image_file_factory=image_file_factory, image_file_store=image_file_store)
	
@app.route("/managerpage")
def managerPage():
	managers=User.query.all()
	image_file = url_for('static',filename='manager.jpg')
	return render_template('managerpage.html', managers=managers, image_file=image_file)

	
@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	form = RegistrationForm()
	if form.validate_on_submit():
		H_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(title=form.title.data, first_name=form.firstname.data, last_name=form.lastname.data, user_role=form.userrole.data, email=form.email.data, password=H_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title="Register", form=form)
	
@app.route("/registermanager", methods=['GET', 'POST'])
def registerManager():
	form = RegistrationForm()
	if form.validate_on_submit():
		H_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(title=form.title.data, first_name=form.firstname.data, last_name=form.lastname.data, user_role=form.userrole.data, email=form.email.data, password=H_password)
		db.session.add(user)
		db.session.commit()
		flash('new manager created!', 'success')
		return redirect(url_for('account'))
	return render_template('register.html', title="Register", form=form)
	
@app.route("/stock",  methods=['GET', 'POST'])
def stock():
	form = StockForm()
	stores=Store.query.all()
	store_inventory=sInventory.query.all()
	factory_inventory=fInventory.query.all()
	if form.validate_on_submit():
		stock = Stock(name=form.stock.data, unit=form.unit.data, stock_for=form.stock_for.data)
		db.session.add(stock)
		db.session.commit()
		flash('{} stock was added!'.format(form.stock.data), 'success')
		if len(store_inventory) or len(factory_inventory) >=1:
			stock=Stock.query.all()
			new_stock=len(stock)
			for s in stock:
				if new_stock==s.id and s.stock_for=='Factory':
					for store in stores:
						if store.type=='Factory':
							id=store.id
							inventory = fInventory(stock_id=new_stock, store_id=id, name=s.name, unit=s.unit, amount='0')
							db.session.add(inventory)
							db.session.commit()
				elif new_stock==s.id and s.stock_for=='Store':
					for store in stores:
						if store.type=='Store':
							id=store.id
							inventory = sInventory(stock_id=new_stock, store_id=id, name=s.name, unit=s.unit, amount='0')
							db.session.add(inventory)
							db.session.commit()
		return redirect(url_for("stock"))
	else:
		flash('something went wrong please check your information', 'danger')
	return render_template('stock.html', title='Stock', form=form, legend="Add Stock")
	
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))
	
def storeFinder():
	stores=Store.query.all()
	for store in stores:
		if store.manager_id==current_user.id:
			St_id=store.id
			return St_id
			
'''def checker():
	inventory=Inventory.query.all()
	stores=Store.query.all()
	st_id=storeFinder()
	for store in stores:
		if current_user.id == store.manager_id:
			for i in inventory:
				if i.store_id == st_id and i.amount < store.TQvalue:
					return send_order_email()'''

def Reorder():
	store=Store.query.all()
	store_inventory=sInventory.query.all()
	factory_inventory=fInventory.query.all()
	reorder=[]
	for s in store:
		if current_user.id == s.manager_id:
			St_id=s.id
			St_tq=s.TQvalue
			if s.type=='Store':
				for i in store_inventory:
					if i.store_id == St_id and i.amount <= St_tq:
						reorder.append(i.name)
			else:
				for i in factory_inventory:
					if i.store_id == St_id and i.amount <= St_tq:
						reorder.append(i.name)
	return reorder

					
@app.route("/account")
def account():
	store_inventory=sInventory.query.all()
	factory_inventory=fInventory.query.all()
	stores=Store.query.all()
	stocks=Stock.query.all()
	St_id=0
	Tq=0
	unit=''
	order_list=(', '.join(Reorder()))
	subject='Re-oder'
	message=''
	image_file_factory = url_for('static', filename='pep.png')
	image_file_store = url_for('static', filename='pizza.jpg')
	for store in stores:
		if store.manager_id==current_user.id:
			St_id=store.id
			Tq=store.TQvalue
			ordering=str(Tq+20)
			for stock in stocks:
				if stock.name in order_list:
					unit=stock.unit
			message='The'+ ' ' +str(store.address)+ ' ' + 'PDQ store would like to order'+ ' ' + order_list+ ' ' + ordering + ' ' + unit + '.'+' '+'Thank you.'
	return render_template('account.html', title='Account', factory_inventory=factory_inventory, store_inventory=store_inventory, stores=stores, St_id=St_id, Tq=Tq, 
							subject=subject, message=message, image_file_factory=image_file_factory, image_file_store=image_file_store)
	
	
@app.route("/selectedpost/<id>")
def selectedpost(id):
	post=Post.query.get(id)
	return render_template('selectedpost.html', title=post.title, post=post)
	
@app.route("/updateStock/<int:stock_id>", methods=['GET', 'POST'])
def updateStock(stock_id):
	store_inventory=sInventory.query.all()
	stocks=Stock.query.all()
	factory_inventory=fInventory.query.all()
	stores=Store.query.all()
	form=StockUpdateForm()
	if form.validate_on_submit():
		for store in stores:
			if current_user.id==store.manager_id:
				st_id=store.id
				type=store.type
				store_update=sInventory.query.filter(sInventory.stock_id==stock_id)
				if type=='Store':
					for s in store_update:
						store_update=s.stock_id
						for inventory in store_inventory:
							if inventory.stock_id==store_update and inventory.store_id==st_id:
								inventory.amount = form.amount.data
								db.session.commit()
								break
				else:
					store_update=fInventory.query.filter(fInventory.stock_id==stock_id)
					for s in store_update:
						store_update=s.stock_id
						for inventory in factory_inventory:
							if inventory.stock_id==store_update and inventory.store_id==st_id:
								inventory.amount = form.amount.data
								db.session.commit()
								break
		return redirect(url_for('account'))
	elif request.method == 'GET':	
		for store in stores:
			if current_user.id==store.manager_id:
				st_id=store.id
				type=store.type
				if type=='Store':
					for inventory in store_inventory:
						if st_id==inventory.store_id:
							form.amount.data = inventory.amount
				else:
					for inventory in factory_inventory:
						if st_id==inventory.store_id:
							form.amount.data = inventory.amount
	return render_template('stockupdatepage.html', title='Update Stock', form=form, legend="Update Stock")


@app.route("/deleteStock<int:id>", methods=['POST'])
def deleteStock(id):
	stock=Stock.query.get(id)
	db.session.delete(stock)
	db.session.commit()
	return redirect(url_for('stockpage'))
	
@app.route("/deleteManager<int:id>", methods=['POST'])
def deleteManager(id):
	user=User.query.get(id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('managerpage'))
 
	
@app.route("/createstore", methods=['GET', 'POST'])
def createStore():
	form = StoreForm()
	stock=Stock.query.all()
	if form.validate_on_submit():
		store = Store(branch=form.branch.data, address=form.address.data, type=form.type.data, TQvalue=form.TQvalue.data, manager_id=form.managerID.data)
		store_type = form.type.data
		db.session.add(store)
		db.session.commit()
		flash('new store created!', 'success')
		'''St_id=Store.query.filter_by(manager_id=form.managerID.data)
		St_id=int(St_id[])'''
		store=Store.query.all()
		St_id=len(store)
		for s in stock:
			if store_type=='Factory' and s.stock_for=='Factory':
				inventory = fInventory(stock_id=s.id, store_id=St_id, name=s.name, unit=s.unit, amount='0')
				db.session.add(inventory)
				db.session.commit()
			elif store_type=='Store' and s.stock_for=='Store':
				inventory = sInventory(stock_id=s.id, store_id=St_id, name=s.name, unit=s.unit, amount='0')
				db.session.add(inventory)
				db.session.commit()
		return redirect(url_for('account'))
	return render_template('createstore.html', title="Create Store", form=form)
	
'''@app.route("/updateVender", methods=['GET', 'POST'])
def updateVender():
	vender=Vendor.query.get()
	form=UpdateVenderForm()
	if form.validate_on_submit():
		vender.type = form.type.data
		vender.email = form.email.data
		vender.address = form.address.data
		vender.contact = form.contact.data
		db.session.commit()
		return redirect(url_for('account'))
	elif request.method == 'GET':	
		form.type.data = vender.type
		form.email.data = vender.email
		form.address.data = vender.address
		form.contact.data = vender.contact
	return render_template('updatevenderpage.html', title='Update Vender', form=form, legend="Update Vender")'''
	

		
	
'''def send_order_email():
	store=Store.query.all()
	for s in store:
		if current_user.id == s.manager_id:
			if s.type == 'Store':
				msg = Message('Order Request', sender='pizzadelivered@yahoo.com', recipients=['lundyshemar@yahoo.com'])
				msg.body = 'The'+ '' +str(s.address)+ '' + 'PDQ store would like to order'+ '' + str(print(Reorder()))+'.'+ '' +'Thank you.'
				mail.send(msg)
				return redirect(url_for('account'))
			else:
				msg = Message('Order Request', sender=current_user.email, recipients=['Vender@yahoo.com'])
				msg.body = 'The'+ '' +s.address+ '' + 'would like to order'+ '' + print(Reorder())+'.'+ '' +'Thank you.'
				mail.send(msg)
				return redirect(url_for('account'))'''
