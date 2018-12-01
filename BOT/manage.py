from flask import Flask
from flask import request

import json
from config import DevelopmentConfig

from handler import recived_message

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_toke = request.args.get('hub.verify_token', '')
        if verify_toke == app.config['SECRET_KEY']:
            return request.args.get('hub.challenge', '')
        return 'Error al validar el secreto'

    elif request.method == 'POST':
        payload = request.get_data()
        data = json.loads(payload)

        for page_entry in data['entry']:
            for message_event in page_entry['messaging']:

                if 'message' in message_event:
                    
                   recived_message(message_event, app.config['PAGE_ACCESS_TOKEN'])
        
        return "ok"



@app.route('/', methods = ['GET'])
def index():
    return 'Hola al curso de bot!'

if __name__ == '__main__':
    app.run(port = 8000)