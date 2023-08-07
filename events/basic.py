from line_bot_api import *


    # 自動回覆相同訊息
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)

    # 自己設定回覆訊息
def about_us_event(event):
    emoji = [
            {
                "index": 0,
                "productId": "5ac21c46040ab15980c9b442",
                "emojiID": "025"
            },
            {
                "index": 17,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiID": "215"
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
def push_msg(event,msg):
    try:
        user_id = event.source.user_id
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    except:
        room_id = event.source.room_id
        line_bot_api.push_message(room_id, TextSendMessage(text=msg))
def Usage(event):
    push_msg(event, '💛查詢方法💛 \
    \n\
    \n👻小幫手可以查詢油價、匯率、股價\
    \n\
    \n👻 油價通知--輸入查詢油價\
    \n👻 匯率通知--換匯USD/TWD\
    \n👻 股價通知--輸入股票代號')
    
                                   