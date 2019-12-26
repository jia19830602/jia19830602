from flask import (Flask, request as rq, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError

main_app = Flask(__name__)

line_bot_api = LineBotApi(
		'YXeGjBJc3YAcQoa2BkNl2+34VpPGczVRn76/WUGm24WV9pKB1a+ndqnF0zhLuM0Sr2lp8m1tasxeEf0XgdMLloCQCIDiR9lzPExqtbKxii/YMtPGlBp9zVUBeSbUdEwaKYUobRES+9H7P5JtNoFl6wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('318797af646feaa757db0b6c6e08561c')


@main_app.route('/')
def index():
	return 'welcome to this app'


@main_app.route('/callback, methods=["POST"]')
def callback():
	signature = rq.headers['X-Line-Signature']
	body = rq.get_data(as_text=True)

	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'


@handler.default()
def default(event):
	print(f'{event} event catched')


if __name__ == "__main__":
	main_app.run(debug=True, host='0.0.0.0', port=80)

