from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('/xKZ5TSGmy6Rajhsgmj78jhBkodFJbIUXH0AD5d0s571200FBFlqN2uhUB7qode70+QwNvbuP90Bvnr3EPjTXrrnFVV79ZS85V4xbcC4tEju04taNE13Qoq0kZRrX9ZDWLEwuhbVGhIfDbhd/L1PWAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ac282083d6d3c9865cc74e021f69abd1')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉,您說什麼'
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return
    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位嗎'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()