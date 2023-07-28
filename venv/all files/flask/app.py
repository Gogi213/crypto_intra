# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import pika
import threading
import json

# Create a Flask application
app = Flask(__name__, template_folder=r'C:\\Users\\Redmi\\PycharmProjects\\crypto_intra\\venv\\all files\\flask\\templates')

# Create a SocketIO application
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

# Define a callback function to handle messages
def callback(ch, method, properties, body):
    message = json.loads(body)
    # Handle the message here
    print(f'Received {message}')
    transformed_message = {
        'symbol': message['s'],
        'askprice': message['a'],
        'askqty': message['A'],
        'bidprice': message['b'],
        'bidqty': message['B']
    }
    socketio.emit('binance update', {'data': transformed_message})

# Define a function that will run in each thread
def worker():
    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='binance_queue')

    channel.basic_consume(queue='binance_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Create and start threads
for i in range(60):
    threading.Thread(target=worker).start()

# Import binance_pulsar
import binance_pulsar