#載入LineBot 所需套件
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

#Channel Access Token
line_bot_api = LineBotApi('upr+6OP3/a/J7V+T28oio32wXywUXu/I1Z1l2ovQyzv5PNuwQavFWoJeJpnIByEvD+cGSdir/rOx4NS1OcUGgHERPbk9dAtTw2OooE3jXjY8c++OJ5otmspm4IwTjRtC6X2KZYjQ6OGTMRnBIDF37QdB04t89/1O/w1cDnyilFU=')
#Channel Secret
handler = WebhookHandler('7fece3ad5ce2609fa114f486b245083e')

#監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 自動回覆相同訊息
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)

    # 自己設定回覆訊息
    emoji = [
            {
                "index": 0,
                "productId": "5ac2280f031a6752fb806d65",
                "emojiID": "005"
            },
            {
                "index": 17,
                "productId": "5ac2280f031a6752fb806d65",
                "emojiID": "005"
            }
    ]

    text_message = TextSendMessage(text='''$ Finance Widget $
Hello! 歡迎您成為 Finance Widget 的好友！ 
                                       
我是 小愛同學
                                       
-這裡有股票、油價和匯率資訊喔~
-請直接點選下方【Finance Widget】的選單功能
-期待您的使用！ ''', emojis = emoji)
    
    sticker_message = StickerSendMessage(
        package_id = '11539',
        sticker_id ='52114118'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message])
                                   

if __name__ == "__main__":
    app.run()