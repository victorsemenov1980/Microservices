# -*- coding: utf-8 -*-
import pika,json
from main import Product, db
import requests


params=pika.URLParameters('')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch,method,properties,body):
    print('Received in main')
    data=json.loads(body)
    print(data)
    
    if properties.content_type=='product created':
        product=Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')
    
    elif properties.content_type=='product updated':
        product=Product.query.get(data['id'])
        product.title=data['title']
        product.image=data['image']
        db.session.commit()
        print('Product changed')
    
    elif properties.content_type=='product list requested':
        
        requests.get('http://docker.for.mac.localhost:8001/api/products')
        print('Product list sent')
    
    elif properties.content_type=='product deleted':
        product=Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')

channel.basic_consume(queue='main',on_message_callback=callback, auto_ack=True)

print( 'Started Consuming')
channel.start_consuming()

channel.close()

































