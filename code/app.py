from flask import Flask,request
from flask_restful import Resource,Api,reqparse
#reqparse is used to only pass specific itmes through json payload
from flask_jwt import JWT,jwt_required

from security import authentication,identity

app = Flask(__name__) #resource is just a thing you api can be mapped to that the subject of data


app.secret_key = "kushal" #secrete key for api authentication

api = Api(app) #to handle the resources easily get,post etc

#we dont have to add jsonify with flask restful since it automatically does that so we can only pass dictionary

jwt = JWT(app,authentication,identity) #all three thing will be sed for the authentication of users 
#jwt will create a new endpoint /auth
#we will send the password and username with this if the username and password mathce in the secuirty
#authentication it will return the user then the jwt will provide a token to the user
#the identity function then uses that token to identify the user
#which will mean the user is authnticated an the id is valid 


items = []

class Item(Resource): #will inherit from class resource
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help='cant be blank')
	data = parser.parse_args()

	@jwt_required()
	def get(self,name):
		item = next(filter(lambda x:x['name'] == name , items),None) 
		#gives the first item found byr the filter function
		#we can also use list typecast we have to return multiple objects with th esame name
		return {"item":item}, 200 if item is not None else 404

	def post(self,name):
		if next(filter(lambda x: x['name']== name , items),None) is not None:
				return {'message': "an item with the {} already exists".format(name)},400

		data = Item.parser.parse_args() #this will convert the type to json
		#silent = true if client does not want to pass json this wil simplty return a null instead of an error
		item = {'name':name, 'price': data['price']}
		items.append(item)
		return item,201

	def delete(delf,name):
		global items #since we have to use the global 
		items = list(filter(lambda x: x['name']!= name,items))
		return {'message':'item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = next(filter(lambda x:x['name'] == name , items),None)
		if item:
			# item['price'] = data['price']
			item.update(data)
		else:
			item = {'name':name , 'price':data['price']}
			items.append(item)
		return item

class Items(Resource): #will inherit from class resource
	def get(self):
		return {'items':items}

api.add_resource(Items, '/items')

api.add_resource(Item, '/item/<string:name>')

app.run(debug=True)
