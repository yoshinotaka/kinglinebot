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

app = Flask(__name__)

line_bot_api = LineBotApi('a9wq8oYltxx4+s2ebaSHKL48pDGnJcbyGuq3ZuLqy+EJzFvm4WhYNSqEStL20bVsKuDIC9QwKo/WdVedCxu9hKVQS8bIMcmrJwqbtohTgc+vsfk2fou6diEtnOrjiWwCR7i28g91afwCqHt579+YdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('41ffe2b4e5016d11dabd5694a9d9c771')

@app.route('/')
def test():
    return "ok!!"

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
        print(handler)
        print(line_bot_api)
        
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()