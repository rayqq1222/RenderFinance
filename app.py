# 載入LineBot所需的套件
from line_bot_api import *
from events.basic import *
from events.oil import *
from events.EXRate import *
from events.Msg_Template import *
from model.mongodb import *
import re
import twstock
import datetime

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('y183jnCciIWryNOI+kTjMm80wyo/KStYQCOLMlqrz4UZ62jOrdkaKMZ/N51MWbMfeqPB6pLdVbTxBim+pn6HExanDVsx7N994f0uOPVrVE/iBJiwBCWexTrbmIFrf5P3CG8LbKBseyKInUlkvynGgwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('b0d867b52ea2085d294fbf521e2119d6')

# 監聽所有來自 /callback 的 Post Request
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
    uid = profile.user_id
    message_text = str(event.message.text).lower()
    msg = str(event.message.text).upper().strip()
    # 使用者輸入的內容
    emsg = event.message.text
    user_name = profile.display_name #使用者名稱

    ############################## 使用說明 選單 基德 油價查詢 ##############################
    if message_text == '@使用說明':
        about_us_event(event)
        Usage(event)

    if event.message.text == "@基德":
        buttons_template = TemplateSendMessage(
            alt_text = '你已得到基德的幫助',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://imgur.com/mBwctnk.jpg',
                actions=[
                    MessageTemplateAction(
                        label="油價查詢",
                        text = '想知道油價'
                    ),
                    MessageTemplateAction(
                        label="匯率查詢",
                        text = '匯率查詢'
                    ),
                    MessageTemplateAction(
                        label="股價查詢",
                        text = '股價查詢'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    if event.message.text == '想知道油價':
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)

        )
    ############################## 股票區 ##############################
    if event.message.text == "股價查詢":
        line_bot_api.push_message(uid, TextSendMessage("請輸入#股票代號"))
        # 用push_message方式回覆話語

    # 股價查詢
    if re.match("想知道股價", msg):
        btn_msg = stock_reply_other(msg)
        line_bot_api.push_message(uid, btn_msg)
        return 0
    
    if re.match("想知道股價[0-9]", msg):
        msg = msg[5:]
        btn_msg = stock_reply_other(msg)
        line_bot_api.push_message(uid, btn_msg)
        return 0
    
    # 新增使用者關注的股票到mongodb
    if re.match('關注[0-9]{4}[<>][0-9]', msg):
        # 使用者新增股票質股票清單
        stockNumber = msg[2:6]
        line_bot_api.push_message(uid, TextSendMessage("加入股票代碼"+stockNumber))
        content = write_my_stock(uid, user_name, stockNumber, msg[6:7], msg[7:])
        line_bot_api.push_message(uid, TextSendMessage(content))
    # else:
    #     content = write_my_stock(uid, user_name, "未設定", "未設定")
    #     line_bot_api.push_message(uid, TextSendMessage(content))
        return 0
    
    if (emsg.startswith('#')):
        text = emsg[1:]
        content =''

        stock_rt = twstock.realtime.get(text)
        my_datetime = datetime.datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
        my_time = my_datetime.strftime('%H:%M:%S')

        content +='%s (%s) %s\n' % (
            stock_rt['info']['name'],
            stock_rt['info']['code'],
            my_time)
        
        content += '現價: %s / 開盤: %s\n'%(
            stock_rt['realtime']['latest_trade_price'],
            stock_rt['realtime']['open'])
        content += '最高: %s / 最低:%s\n'%(
            stock_rt['realtime']['high'],
            stock_rt['realtime']['low'])
        content += '量: %s\n'%(stock_rt['realtime']['accumulate_trade_volume'])

        stock = twstock.Stock(text)
        content += '-----\n'
        content += '最近五日價格: \n'
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range(len(price5)):
            content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=content)
        )
    ############################## 匯率區 ##############################
    if re.match('幣別種類',emsg):
        message = show_Button()
        line_bot_api.reply_message(event.reply_token, message)

    if re.match('換匯[A-Z]{3}/[A-Z]{3}/100',msg):
        line_bot_api.push_message(uid, TextSendMessage("基德將為您做外匯計算"))
        content = getExchangeRate(msg)
        line_bot_api.push_message(uid, TextSendMessage(content))
                                              
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = '''HiHi 歡迎成為基德的夥伴！
                                
- 這裡有股票和匯率資訊哦
- 直接點選下方圖中選單功能
                                   
期待你的使用！'''
                                  
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)

if __name__ == "__main__":
    app.run()