# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationSendMessage,
)
from datetime import datetime
import pytz

app = Flask(__name__)

line_bot_api = LineBotApi('3bh4V8siG/f1u9liIXqi/0002hSE4332/106XyUZ8tfYRXNrKpV/9fDpvPWO1I+ewd5fNvAImy6Tkao025DlWpXhp23R0hbvo16i/CXfVoY4Siwy0Zjrvgw6DWK/9k3GhjoHanOUV3bPSLOrx+6FOQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('f52cabf61fb026df7b0703761876d96e') #Your Channel Secret

try:
    line_bot_api.push_message('U1ac9f0d549ee83537dc724c47df451bf', TextSendMessage(text='Hello World!'))
except linebot.exceptions.LineBotApiError as e:
    print(e.status_code)
    print(e.error.message)
    print(e.error.details)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)       
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent)
def handle_text_message(event):    

    if event.message.type == 'text':
        tz = pytz.timezone('Asia/Taipei')
        #time_now = time.strftime(' %Y-%m-%d %H:%M:%S %Z', time.gmtime(event.timestamp/1000)).replace(tzinfo=pytz.timezone('UTC'))
        time_now = datetime.fromtimestamp(event.timestamp/1000).replace(tzinfo=pytz.utc)    
        #.replace(tzinfo=pytz.timezone('US/Pacific'))
        
        time_tw = time_now.astimezone(tz)
        time = time_tw.strftime(' %Y-%m-%d %H:%M:%S')    

        text = event.message.text + time + '\n ID: ' + event.source.user_id #message from user

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)) #reply the same message from user

    elif event.message.type == 'location':
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(title='my location',
                address='IIS',
                latitude=event.message.latitude,
                longitude=event.message.longitude)
        ) #reply the same message from user     
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    