from line_bot_api import *

def about_us_event(event):
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
                "index": 16,
                "productId": "5ac2280f031a6752fb806d65",
                "emojiID": "005"
            }
    ]

    text_message = TextSendMessage(text='''$ Kiddo Finance $
HiHi 歡迎成為基德的夥伴！
                                
- 這裡有股票和匯率資訊哦
- 直接點選下方圖中選單功能
                                   
期待你的使用！''', emojis = emoji)
    
    sticker_message = StickerSendMessage(
        package_id = '11539',
        sticker_id ='52114118'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message])
    
def push_msg(event, msg):
    try:
        user_id = event.source.user_id
        line_bot_api.push_message(user_id, TextSendMessage(text = msg))
    except:
        room_id = event.source.room_id
        line_bot_api.push_message(room_id, TextSendMessage(text = msg))

def Usage(event):
    push_msg(event, "                  查詢方法 🔍️       \
             \n     ✄------------------------\
             \n🐱基徳可以查詢油價 匯率 股價\
             \n     ------------------------✄\
             \n💰油價通知 ➜ 輸入查詢油價\
             \n💰匯率通知 ➜ 輸入查詢匯率\
             \n💰匯率兌換 ➜ 換匯USD/TWD\
             \n💰股價查詢 ➜ 輸入#股票代號")
    
