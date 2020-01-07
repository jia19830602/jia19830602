from flask import (render_template, request as rq, abort)
from apps import main_app
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from bs4 import BeautifulSoup
import requests
import configs

line_bot_api = LineBotApi(configs.CHANNEL_ACCESS_TOKEN)  #
handler = WebhookHandler(configs.CHANNEL_SECRET)  #


# Homepage
@main_app.route('/', methods=["POST", "GET"])  #
def index():
	return render_template('index.html')  # apps.send_static_file


@main_app.route('/callback', methods=["POST"], endpoint='callback')  #
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


# # 基本複誦訊息&關鍵字打招呼
# @handler.add(MessageEvent, message=TextMessage)


# 基本回傳貼圖
@handler.add(MessageEvent)
def handle_sticker_message(sticker_event):
	p_id = sticker_event.message.package_id
	s_id = sticker_event.message.sticker_id
	line_bot_api.reply_message(
			sticker_event.reply_token,
			StickerSendMessage(package_id=p_id, sticker_id=s_id)
	)


@handler.add(MessageEvent, message=TextMessage)
def find_news(mgs_event):

	def tech_news():
		target_url = 'https://technews.tw/'
		print('Start parsing movie ...')
		rs = requests.session()
		res = rs.get(target_url, verify=False)
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text, 'html.parser')
		_content = ""

		for aa, data in enumerate(soup.select('article div h1.entry-title a')):
			if aa == 12:
				return _content
			title = data.text
			link = data['href']
			_content += '{}\n{}\n\n'.format(title, link)
		return _content

	user_msg = mgs_event.message.text

	if user_msg == "新聞":
		content = tech_news()
		line_bot_api.reply_message(
				mgs_event.reply_token,
				TextSendMessage(text=content)
		)


def handle_messages(mgs_event):
	_id = mgs_event.source.user_id  # get user ID
	profile = line_bot_api.get_profile(_id)  # get personal info
	_name = profile.display_name  # storage user display name
	user_msg = mgs_event.message.text  # read text which user passed in

	greet_list = ['你好', '嗨', '哈囉', 'hi', 'hey']

	if user_msg in greet_list:
		greet_user = f'Hello! {_name} '
		reply = greet_user

	else:
		reply = user_msg

	reply_msg = TextSendMessage(text=reply)
	line_bot_api.reply_message(
			mgs_event.reply_token,
			reply_msg
	)


# @handler.add(FollowEvent)  # catch FollowEvent
# def followed(follow_event):
# 	_id = follow_event.source.user_id  # get user ID
# 	profile = line_bot_api.get_profile(_id)  # get personal info
# 	_name = profile.display_name  # storage user display name
#
# 	follow_greet = f"It's good to meet you, my dear {_name}! "
# 	reply_msg = TextSendMessage(text=follow_greet)
# 	line_bot_api.reply_message(
# 			follow_event.reply_token,
# 			reply_msg
# 	)
