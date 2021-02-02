# -*- coding: utf-8 -*-
from dataclasses import dataclass
from flask import Flask, jsonify, abort, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from producer import publish
from functools import wraps


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@db/main'
CORS(app)

db=SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id:int
    title:str
    image:str
    id=db.Column(db.Integer, primary_key=True,autoincrement=False)
    title=db.Column(db.String(200))
    image=db.Column(db.String(200))
    
               

    
    
   

@app.route('/api/products')

def index():
    content=json.dumps(Product.query.all())
    
    
    publish('product list sent',content )
    
    return jsonify(Product.query.all())
   



    

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')

































