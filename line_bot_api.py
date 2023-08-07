from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

#Channel Access Token
line_bot_api = LineBotApi('upr+6OP3/a/J7V+T28oio32wXywUXu/I1Z1l2ovQyzv5PNuwQavFWoJeJpnIByEvD+cGSdir/rOx4NS1OcUGgHERPbk9dAtTw2OooE3jXjY8c++OJ5otmspm4IwTjRtC6X2KZYjQ6OGTMRnBIDF37QdB04t89/1O/w1cDnyilFU=')
#Channel Secret
handler = WebhookHandler('7fece3ad5ce2609fa114f486b245083e')
