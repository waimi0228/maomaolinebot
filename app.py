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

from linebot.models import *

import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve 

app = Flask(__name__)


line_bot_api = LineBotApi('wuxSRsXCcOwSbvjnu8jDCRCf9S1nItqJYrrRz0MX+FhmAzes7kEcfA1+TgmXULjIrsQ1wlFAbp7R5VBea8eB6bFJEjA9oJfZfjXzSKIS7geV+4S+Ysb337QJRfC9WnhpTcZRgl3k56XbUJ5xrNQJzQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a259360df6e480fc0d7e092d98f08009')

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    msg = msg.encode('utf-8')
    if event.message.text == msg:
        a=movie()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))

def movie():
    target_url = 'https://movies.yahoo.com.tw/movie_intheaters.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.release_movie_name a')):
        if index == 20:
            return content       
        title = data.text.lstrip().rstrip()
        content += '{}\n'.format(title)
    return content
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)