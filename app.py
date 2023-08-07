#載入LineBot 所需套件
from line_bot_api import *
from events.basic import *
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
    message_text = str(event.message.text).lower()

    if message_text == '@使用說明':
        about_us_event(event)
        Usage(event)
    
    if event.message.text == "@小愛同學":
        buttons_template = TemplateSendMessage(
            alt_text = '小愛同學template',
            template=ButtonsTemplate(
            title = "選擇服務",
            text = '請選擇',
            thumbnail_image_url='https://i.imgur.com/decXwFE.jpg',
            actions=[
                MessageTemplateAction(
            label = '油價查詢',
            text = '油價查詢'
            ),
            MessageTemplateAction(
            label = '匯率查詢',
            text = '匯率查詢'
            ),
            MessageTemplateAction(
            label = '股價查詢',
            text = '股價查詢'
            )
            ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    

if __name__ == "__main__":
    app.run()