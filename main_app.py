from flask import (Flask, render_template, request as rq, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import config

main_app = Flask(__name__, static_folder='.', static_url_path='')  #
# main_app.debug = True
line_bot_api = LineBotApi('YXeGjBJc3YAcQoa2BkNl2+34VpPGczVRn76/WUGm24WV9pKB1a+ndqnF0zhLuM0Sr2lp8m1tasxeEf0XgdMLloCQCIDiR9lzPExqtbKxii/YMtPGlBp9zVUBeSbUdEwaKYUobRES+9H7P5JtNoFl6wdB04t89/1O/w1cDnyilFU=')  # getenv('CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('0300c17210cfea52f0499e9cf80d7984')  # ?  318797af646feaa757db0b6c6e08561c getenv('CHANNEL_SECRET')


# Homepage
@main_app.route('/', methods=["POST", "GET"])
def index():
	return render_template('index.html')  # main_app.send_static_file


@main_app.route('/callback', methods=["POST", "GET"])
def callback():
	signature = rq.headers['X-Line-Signature']
	body = rq.get_data(as_text=True)

	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'


@handler.default()
def default(default_event):
	print(f'{default_event} event catched')


# 基本複誦訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_messages(mgs_event):
	_id = mgs_event.source.user_id  # get user ID unicode
	profile = line_bot_api.get_profile(_id)  # get personal info
	_name = profile.display_name  # storage info
	user_msg = mgs_event.message.text  # read text which user passed in

	if (user_msg == 'hi') or (user_msg == '你好'):
		greet_user = f'hello{_name}'
		reply = greet_user

	else:
		reply = user_msg

	reply_msg = TextSendMessage(text=reply)
	line_bot_api.reply_message(
			mgs_event.reply_token,
			reply_msg 
	)


# 基本回傳貼圖
@handler.add(MessageEvent)
def handle_sticker_message(event_sticker):
	p_id = event_sticker.message.package_id
	s_id = event_sticker.message.sticker_id
	line_bot_api.reply_message(
			event_sticker.reply_token,
			StickerSendMessage(package_id=p_id, sticker_id=s_id)
	)


if __name__ == "__main__":
	main_app.run()  # debug=True, host='127.0.0.1', port=80
