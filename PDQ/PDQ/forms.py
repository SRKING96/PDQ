from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from PDQ.models import User, Store

class RegistrationForm(FlaskForm):
	firstname= StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
	lastname= StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
	title= SelectField('Title', choices=[('Mr.','Mr.'), ('Mrs.','Mrs.'), ('Ms.','Ms.')], validators=[DataRequired()])
	email= StringField('Email', validators=[DataRequired(), Email()])
	userrole= SelectField('User Role', choices=[('Manager','Manager'), ('Admin','Admin')], validators=[DataRequired()])
	password= PasswordField('Password', validators=[DataRequired()])
	confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit= SubmitField('Sign up')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is already in use.')
	
class LoginForm(FlaskForm):
	email= StringField('Email', validators=[DataRequired(), Email()])
	password= PasswordField('Password', validators=[DataRequired()])
	remember= BooleanField('Remember Me')
	submit= SubmitField('Login')
	
class StockForm(FlaskForm):
	stock= StringField('Stock Name', validators=[DataRequired(), Length(min=2, max=20)])
	unit= SelectField('Unit', choices=[('L','L'), ('lb','lb'), ('oz','oz'), ('boxes','boxes')], validators=[DataRequired()])
	stock_for= SelectField('Stock for', choices=[('Factory','Factory'), ('Store','Store')], validators=[DataRequired()])
	submit= SubmitField('Add Stock')
	
class StockUpdateForm(FlaskForm):
	amount= DecimalField('Amount', places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
	submit= SubmitField('Update Stock')

class StoreForm(FlaskForm):
	branch= StringField('Branch', validators=[DataRequired(), Length(min=2, max=20)])
	address= StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
	type= SelectField('Type', choices=[('Factory','Factory'), ('Store','Store')], validators=[DataRequired()])
	TQvalue= DecimalField('Threshold value ', places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
	managerID= StringField('Input manager ID', validators=[DataRequired(), Length(min=1, max=20)])
	submit= SubmitField('Create Store/Factory')
	
	def validate_id(self, managerID):
		id = User.query.filter_by(id=managerID.data).first()
		if id=='':
			raise ValidationError('ID not found.')
			
	def validate_id_repeat(self, managerID):
		id = User.query.filter_by(id=managerID.data).first()
		if id:
			raise ValidationError('Manager already assigned')
			
class UpdateVenderForm(FlaskForm):
	type= SelectField('Type', choices=[('Factory','Factory'), ('Supplier','Supplier')], validators=[DataRequired()])
	email= StringField('Email', validators=[DataRequired(), Email()])
	address= StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
	contact= StringField('Contact', validators=[DataRequired(), Length(min=2, max=20)])
	submit= SubmitField('Update Vender')
