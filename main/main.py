# -*- coding: utf-8 -*-
from dataclasses import dataclass
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from producer import publish
from functools import wraps


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@db/main'
CORS(app)

db=SQLAlchemy(app)



def token_required(controller_function):
    @wraps(controller_function)
    def wrapper_function(*args, **kwargs):
        
        try:
            
            token={"token":request.headers.get('token')}
            #проверить токен в Redis
            response = requests.post('http://docker.for.mac.localhost:8000/api-token-verify/', token)
            
            
            if response.status_code == 200:
                #сохранить токен в Redis
                return controller_function(*args, **kwargs)
            else:
                abort(403, 'Invalid user')
                
        except:
            abort(403, 'Invalid user')
            
    return wrapper_function




@dataclass
class Product(db.Model):
    id:int
    title:str
    image:str
    id=db.Column(db.Integer, primary_key=True,autoincrement=False)
    title=db.Column(db.String(200))
    image=db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id:int
    user_id:int
    product_id:int
    
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)
    
   

@app.route('/api/products')
@token_required 
def index():
    
    return jsonify(Product.query.all())



@app.route('/api/products/<int:id>/choose', methods=['POST'])
@token_required
def choose(id):
    #получаем id радомно, просто для примера коммуникации
    req=requests.get('http://docker.for.mac.localhost:8000/api/user')
    json=req.json()
    try:
        productUser=ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        
        publish('product chosen',id)
    except:
        abort(400, "You already chose this product")
    
    return jsonify({
        'message':'success'
        })
    
    

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')

































