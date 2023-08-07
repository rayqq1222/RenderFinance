#載入LineBot 所需套件
from line_bot_api import *
from events.basic import *
from events.oil import *
app = Flask(__name__)

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
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id  # 使用者id
    message_text = str(event.message.text).lower()


    if message_text == '@小愛同學':
        about_us_event(event)
        Usage(event)
    elif event.message.text != '油價查詢' or event.message.text != '@使用說明' or event.message.text != '股價查詢':
        free_msg(event)

################### 使用說明 ###################
    if message_text == '@使用說明':
        about_us_event(event)
        Usage(event)
    if message_text == '油價查詢':
        content = oil_price()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(content))
################# 股票查詢 #####################
    if message_text == '股價查詢':
        line_bot_api.push_message(uid, TextSendMessage('請輸入#股票代號..(例如：#2330)'))

@handler.add(FollowEvent)
def handel_follow(event):
    welcome_msg = """好久不見! 小愛好想你🥺 
還記得小愛嗎                                                                     
-小愛能幫您查詢股票、油價和匯率資訊喔~
-請點選下方【Finance Widget】的選單功能
-期待您的使用！"""
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)

    

if __name__ == "__main__":
    app.run()