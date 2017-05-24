# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('3bh4V8siG/f1u9liIXqi/0002hSE4332/106XyUZ8tfYRXNrKpV/9fDpvPWO1I+ewd5fNvAImy6Tkao025DlWpXhp23R0hbvo16i/CXfVoY4Siwy0Zjrvgw6DWK/9k3GhjoHanOUV3bPSLOrx+6FOQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('f52cabf61fb026df7b0703761876d96e') #Your Channel Secret

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = str(event.message.text)+' OK!' #message from user

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)) #reply the same message from user


@handler.add(MessageEvent, message=LocationMessage)
def handle_position_message(event):
    #text = str(event.message.text)+' OK!' #message from user

    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title='my location',
            address='Taiwan',
            latitude=event.message.latitude,
            longitude=event.message.longitude
        )
    ) #reply the same message from user    
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])