from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import qrcode
import os

app = Flask(__name__)
sslify = SSLify(app)

token = 'token'
URL = 'https://api.telegram.org/bot' + token + '/'  # need to concatenate with necessary method (API Telegram bot)


# recording server response to json file
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


# sending text message to user
def send_massage(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    resp = requests.post(url, json=answer)
    return resp.json()


# sending image to user
def send_image(chat_id, filename, caption):
    url = URL + 'sendPhoto'
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id': chat_id, 'caption': caption}
    resp = requests.post(url, files=files, data=data)
    return resp.json()


# generation QR-code
def qr_generation(data, filename):
    img = qrcode.make(data)
    img.save(filename)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        resp = request.get_json()
        chat_id = resp['message']['chat']['id']

        try:
            data = resp['message']['text']

            if data == '/start':
                send_massage(chat_id, 'Welcome!')

            else:
                qr_generation(data, filename=str(chat_id)+'.png')
                send_image(chat_id, filename=str(chat_id)+'.png', caption=data)  # next remove png file

                try:
                    os.remove('/home/VipPro/'+str(chat_id)+'.png')

                except:
                    pass

        except:
            send_massage(chat_id, 'Please, send text')

        return jsonify(resp)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
