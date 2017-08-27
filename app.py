# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

from datetime import datetime
import pytz

import requests
import urllib
from lxml import etree

app = Flask(__name__)

line_bot_api = LineBotApi('3bh4V8siG/f1u9liIXqi/0002hSE4332/106XyUZ8tfYRXNrKpV/9fDpvPWO1I+ewd5fNvAImy6Tkao025DlWpXhp23R0hbvo16i/CXfVoY4Siwy0Zjrvgw6DWK/9k3GhjoHanOUV3bPSLOrx+6FOQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('f52cabf61fb026df7b0703761876d96e') #Your Channel Secret

# try:
#     line_bot_api.push_message('U1ac9f0d549ee83537dc724c47df451bf', TextSendMessage(text='Hello World!'))
# except linebot.exceptions.LineBotApiError as e:
#     print(e.status_code)
#     print(e.error.message)
#     print(e.error.details)

# buttons_template_message = TemplateSendMessage(
#     alt_text='Buttons template',
#     template=ButtonsTemplate(
#         thumbnail_image_url='https://raw.githubusercontent.com/nellymilk/line-bot-python-heroku/master/images/img.jpg',
#         title='Menu',
#         text='Please select',
#         actions=[
#             PostbackTemplateAction(
#                 label='postback',
#                 text='postback text',
#                 data='action=buy&itemid=1'
#             ),
#             MessageTemplateAction(
#                 label='message',
#                 text='message text'
#             ),
#             URITemplateAction(
#                 label='uri',
#                 uri='http://example.com/'
#             )
#         ]
#     )
# )
#try:

#line_bot_api.push_message('U1ac9f0d549ee83537dc724c47df451bf', buttons_template_message)


# except LineBotApiError as e:
#     print(e.status_code)
#     print(e.error.message)
#     print(e.error.details)
 

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

def crawler(url):
    header = {    
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }    
    response = requests.get(url,headers=header)
    html = response.content.decode('utf-8')

    page = etree.HTML(html)
    temp = []
    name_value = {}
    for i in page.xpath("//table[@id='tblStockList']//tr[@id]"):
        temp.extend(i.xpath("./td[position()<2]//text()"))
        name_value[i.xpath("./td[1]//text()")[0]]=[i.xpath("./td[1]//text()")[0],i.xpath("./td[2]//text()")[0],i.xpath("./td[3]//text()")[0]]

    return temp,name_value   

def findStock():

    link = [
        'http://goodinfo.tw/stockinfo/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=5%E6%97%A5%2F10%E6%97%A5%2F%E6%9C%88%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%405%E6%97%A5%2F10%E6%97%A5%2F%E6%9C%88%E7%B7%9A&SHEET=%E7%A7%BB%E5%8B%95%E5%9D%87%E7%B7%9A&SHEET2=%E7%9B%AE%E5%89%8D%E4%BD%8D%E7%BD%AE%28%E5%85%83%29&RPT_TIME=',
        'http://goodinfo.tw/stockinfo/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E8%82%A1%E5%83%B9%E5%89%B5%E4%B8%80%E5%80%8B%E6%9C%88%E9%AB%98%E9%BB%9E%40%40%E8%82%A1%E5%83%B9%E5%89%B5%E5%A4%9A%E6%97%A5%E9%AB%98%E9%BB%9E%40%40%E4%B8%80%E5%80%8B%E6%9C%88&SHEET=%E6%BC%B2%E8%B7%8C%E5%8F%8A%E6%88%90%E4%BA%A4%E7%B5%B1%E8%A8%88&SHEET2=%E6%9C%80%E9%AB%98%2F%E6%9C%80%E4%BD%8E%E8%82%A1%E5%83%B9%E7%B5%B1%E8%A8%88%285%E6%97%A5%2F10%E6%97%A5%2F%E4%B8%80%E5%80%8B%E6%9C%88%29&RPT_TIME=',
        'http://goodinfo.tw/stockinfo/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E9%80%A3%E8%B2%B7+%28%E6%97%A5%29%40%40%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85%40%40%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85+%28%E6%97%A5%29&SHEET=%E6%B3%95%E4%BA%BA%E8%B2%B7%E8%B3%A3&SHEET2=%E9%80%A3%E8%B2%B7%E9%80%A3%E8%B3%A3%E7%B5%B1%E8%A8%88%28%E6%97%A5%29&RPT_TIME=',
        'http://goodinfo.tw/stockinfo/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E9%80%A3%E7%BA%8C%E5%A4%9A%E6%97%A5%E4%B8%8A%E6%BC%B2%40%40%E9%80%A3%E7%BA%8C%E4%B8%8A%E6%BC%B2%40%40%E9%80%A3%E7%BA%8C%E5%A4%9A%E6%97%A5%E4%B8%8A%E6%BC%B2&SHEET=%E6%BC%B2%E8%B7%8C%E5%8F%8A%E6%88%90%E4%BA%A4%E7%B5%B1%E8%A8%88&SHEET2=%E9%80%A3%E6%BC%B2%E9%80%A3%E8%B7%8C%E7%B5%B1%E8%A8%88%28%E6%97%A5%29&RPT_TIME='
    ]

    for i in range(4):
        temp,name_value = crawler(link[i])
        if i == 0:
            result = temp

        result = set(result) & set(temp)

    print('crawler successfully!')    

    output = list(filter(lambda x: len(x)<=4, list(result))) 
    print(output)

    for index in output:
        industry = find_Industry('http://goodinfo.tw/stockinfo/StockDetail.asp?STOCK_ID='+index)
        name_value[index].extend(industry)

    #page.xpath("//table[@class='solid_1_padding_3_2_tbl']//td[2]//text()")[4]
    
    return sorted(list(map(lambda x: name_value[x], output)), key=lambda x: float(x[2]))

def find_Industry(url):

    header = {    
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }    
    response = requests.get(url,headers=header)
    html = response.content.decode('utf-8')

    page = etree.HTML(html)
    
    industry = page.xpath("//table[@class='solid_1_padding_3_2_tbl']//td[2]//text()")[4]
        
    return industry

def find_Name(url):

    header = {    
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }    
    response = requests.get(url,headers=header)
    html = response.content.decode('utf-8')

    page = etree.HTML(html)
    name = page.xpath("//table[@class='std_tbl']//td//a//text()")[0]
    
    return name


@handler.add(MessageEvent)
def handle_text_message(event):    

    if event.message.type == 'text':
        # tz = pytz.timezone('Asia/Taipei')
        # time_now = datetime.fromtimestamp(event.timestamp/1000).replace(tzinfo=pytz.utc)            
        
        # time_tw = time_now.astimezone(tz)
        # time = time_tw.strftime(' %Y-%m-%d %H:%M:%S')    

        # text = event.message.text + time + '\n ID: ' + event.source.user_id #message from user

        if event.message.text == 'help':
            result = findStock()
            #print('123')

            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=str(result))
            )
        else:    
            buttons_template_message = TemplateSendMessage(
               # name, industry = findName_Industry('http://goodinfo.tw/stockinfo/StockDetail.asp?STOCK_ID=' + event.message.text),
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://raw.githubusercontent.com/nellymilk/line-bot-python-heroku/master/images/stock.jpg',
                    title='Stock detail',
                    text='Please click following link',
                    actions=[            
                        URITemplateAction(
                            label=find_Name('http://goodinfo.tw/stockinfo/StockDetail.asp?STOCK_ID=' + event.message.text)+'  '+find_Industry('http://goodinfo.tw/stockinfo/StockDetail.asp?STOCK_ID=' + event.message.text),
                            uri='http://goodinfo.tw/stockinfo/StockDetail.asp?STOCK_ID=' + event.message.text
                        )
                    ]
                )
            )
            line_bot_api.reply_message(
                event.reply_token,buttons_template_message
            ) #reply the same message from user
        #TextSendMessage(text=text)

    elif event.message.type == 'location':
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(title='my location',
                address=event.message.address,
                latitude=event.message.latitude,
                longitude=event.message.longitude)
        ) #reply the same message from user     
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    