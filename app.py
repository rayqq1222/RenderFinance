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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run()