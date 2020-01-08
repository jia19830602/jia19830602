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


# 基本複誦訊息&關鍵字打招呼

@handler.add(MessageEvent, message=TextMessage)
def handle_messages(mgs_event):

	_id = mgs_event.source.user_id  # get user ID
	profile = line_bot_api.get_profile(_id)  # get personal info
	_name = profile.display_name  # storage user display name
	user_msg = mgs_event.message.text  # read text which user passed in
	reply = mgs_event.reply_token

	def reply_messages():
		greet_list = ['嗨', '你好', '哈囉', 'hi', 'hey', 'hello']
		if user_msg.lower() in greet_list:
			greet_user = f' Hello~ {_name} !'
			_reply = greet_user

		else:
			_reply = user_msg
		return _reply

	def tech_news():
		target_url = 'https://technews.tw/'
		rs = requests.session()
		res = rs.get(target_url, verify=False)
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text, 'html.parser')
		_content = ""

		for _index, data in enumerate(soup.select('article div h1.entry-title a')):
			if _index == 5:
				return _content
			title = data.text
			link = data['href']
			_content += '{}\n{}\n\n'.format(title, link)
		return _content

	def apple_news():
		target_url = 'https://tw.appledaily.com/new/realtime'
		rs = requests.session()
		res = rs.get(target_url, verify=False)
		soup = BeautifulSoup(res.text, 'html.parser')
		_content = ""
		for _index, data in enumerate(soup.select('.rtddt a'), 0):
			if _index == 5:
				return _content
			link = data['href']
			_content += '{}\n\n'.format(link)
		return _content

	if user_msg == "新聞":
		content = tech_news()
		line_bot_api.reply_message(reply, TextSendMessage(text=content))

	if user_msg == "蘋果新聞":
		apple = apple_news()
		line_bot_api.reply_message(reply, TextSendMessage(text=apple))

	msg = reply_messages()
	line_bot_api.reply_message(reply, TextSendMessage(text=msg))


# 基本回傳貼圖
@handler.add(MessageEvent)
def handle_sticker_message(sticker_event):
	p_id = sticker_event.message.package_id
	s_id = sticker_event.message.sticker_id
	line_bot_api.reply_message(
			sticker_event.reply_token,
			StickerSendMessage(package_id=p_id, sticker_id=s_id)
	)


@handler.add(FollowEvent)  # catch FollowEvents
def followed(follow_event):
	_id = follow_event.source.user_id  # get user ID
	profile = line_bot_api.get_profile(_id)  # get personal info
	_name = profile.display_name  # storage user display name

	greet = f"It's good to meet you, my dear {_name}! "
	line_bot_api.reply_message(
		follow_event.reply_token, TextSendMessage(text=greet)
	)
