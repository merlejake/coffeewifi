from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def to_dict(self):
	dictionary = {}
	for column in self.__table__.columns:
		dictionary[column.name] = getattr(self,column.name)
	return dictionary

##Cafe TABLE Configuration
class Cafe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), unique=True, nullable=False)
	map_url = db.Column(db.String(500), nullable=False)
	img_url = db.Column(db.String(500), nullable=False)
	location = db.Column(db.String(250), nullable=False)
	seats = db.Column(db.String(250), nullable=False)
	has_toilet = db.Column(db.Boolean, nullable=False)
	has_wifi = db.Column(db.Boolean, nullable=False)
	has_sockets = db.Column(db.Boolean, nullable=False)
	can_take_calls = db.Column(db.Boolean, nullable=False)
	coffee_price = db.Column(db.String(250), nullable=True)


@app.route('/')
def home():
	return render_template("index.html")
    

## HTTP GET - Read Record
@app.route('/random',methods=['GET','POST'])
def random_cafe():
	if request.method == 'GET':
		cafes = db.session.query(Cafe).all()
		random_cafe =(random.choice(cafes))
		cafe = to_dict(random_cafe)
	return jsonify(cafe)

@app.route('/all')
def get_all_cafes():
	cafes = db.session.query(Cafe).all()
	return jsonify(cafes=[to_dict(cafe) for cafe in cafes])

@app.route('/search', methods=['GET','POST'])
def find_cafe():
	if request.method == 'POST':
		form_location = (request.form['location']).capitalize()
		
		cafes = db.session.query(Cafe).filter_by(location=form_location)
		searched_cafe = [to_dict(cafe) for cafe in cafes]
		print(searched_cafe)
		if searched_cafe:
			return jsonify(searched_cafe)
		else:
			return '<h1>No cafe found</h1>'

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record



if __name__ == '__main__':
	app.run(
		debug=True,
		host = '0.0.0.0',
		port=8080
		)
