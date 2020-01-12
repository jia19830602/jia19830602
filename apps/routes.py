from flask import (render_template, request as rq, abort)
from apps import main_app
from linebot.exceptions import InvalidSignatureError
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import *
# from imgurpython import ImgurClient
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
# import pyimgur
import time
import ENV

# line bot
line_bot_api = LineBotApi(ENV.CHANNEL_ACCESS_TOKEN)  #
handler = WebhookHandler(ENV.CHANNEL_SECRET)  #
# imgur
client_id = ENV.CLIENT_ID
client_secret = ENV.CLIENT_SECRET
access_token = ENV.ACCESS_TOKEN
refresh_token = ENV.REFRESH_TOKEN
# client = ImgurClient(client_id, client_secret, access_token, refresh_token)


# Chrome Options

prefs = {"profile.managed_default_content_settings.images": 2}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
options.binary_location = ENV.GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=ENV.CHROMEDRIVER_PATH, chrome_options=options)


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
			if _index == 5: return _content
			title = data.text
			link = data['href']
			_content += f'{title}\n{link}\n\n'
		return _content

	def apple_news():
		target_url = 'https://tw.appledaily.com/new/realtime'
		rs = requests.session()
		res = rs.get(target_url, verify=False)
		soup = BeautifulSoup(res.text, 'html.parser')
		_content = ""
		for _index, data in enumerate(soup.select('.rtddt a'), 0):
			if _index == 5: return _content
			link = data['href']
			_content += f'{link}\n\n'
		return _content

	def selenium_crawler():

		def enter():

			while True:
				_item = 'sony w810'  # 'sony w810'
				_item = _item.replace("%", "")
				if user_msg != "":
					break
				else:
					print('請重新輸入')
					continue

			_url = f'https://www.letao.com.tw/yahoojp/auctions/history.php?category=0&p={_item}&seller='
			return _url, _item

		url, item = enter()
		driver.get(url)
		time.sleep(1)

		amounts = driver.find_element_by_class_name("m2ItemPosVsCnt")
		ats = amounts.text
		ats = ats.split(' ')[2]
		ats = ats.replace("件", "")
		ats = ats.replace(" ", "")

		url_part = '//html/body/div[11]/div[2]/div/div[2]/table/tbody/'
		price_list = []
		price = ''
		page_counter = 0
		while True:
			page_counter += 1
			driver.find_element_by_xpath(
				'/html/body/div[11]/div[2]/div/div[3]/span[*]/a[contains(@title,"下一頁")]').click()
			url = driver.current_url
			# html = requests.get(url).text
			# soup = BeautifulSoup(html, 'html.parser')
			# next_page = soup.find('a', title='下一頁')
			a_tag_all = driver.find_elements_by_xpath(f'{url_part}*/td[2]/table/tbody/tr[1]/td/a[@href]')
			for f in range(len(a_tag_all)):
				y = f * 5 + 3
				y = str(y)
				a_tag = driver.find_element_by_xpath(f'{url_part}tr[{y}]/td[3]/table/tbody/tr[1]/td[1]/span[1]')
				_str = a_tag.text
				str_split = _str.split('円')[0]
				_price = str_split.replace(",", "")
				int_price = round(int(_price))
				price_list.append(int_price)
				if page_counter == 1: price += f'\n{_str}'
			if page_counter > 1: break

		# path = "my_fig.png"
		#
		# def img():
		# 	plt.figure(figsize=(8.000, 6.000), dpi=100)
		# 	plt.rcParams["axes.unicode_minus"] = False  # 正常顯示負數 plt.rcParams['font.sans-serif']=['SimHei']  # 正常顯示中文
		# 	plt.xlabel(" Price (JPY) ", fontsize=14)
		# 	plt.ylabel("counts", fontsize=14)
		# 	plt.grid(axis='x', linestyle='-.')  # 畫格線
		# 	plt.grid(axis='y', linestyle='-.')
		# 	plt.xticks(fontsize=18)
		# 	plt.yticks(fontsize=18)
		# 	plt.hist(price_list, 15)  # n, bins, patches = plt.hist(price_list, 15)
		# 	plt.title(f"  {item}  PriceTable", fontsize=24)
		# 	plt.savefig('my_fig.png', dpi=80)  # 解析度
		#
		# 	# im = pyimgur.Imgur(client_id)
		# 	uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
		# 	return uploaded_image.link

		# _img_url = img()
		_selenium_msg = f"共找到 {ats} 項拍賣品，價格如下，{price}"
		driver.close()
		return _selenium_msg  # , _img_url

	if user_msg == "新聞":
		content = tech_news()
		line_bot_api.reply_message(reply, TextSendMessage(text=content))

	if user_msg == "蘋果新聞":
		apple = apple_news()
		line_bot_api.reply_message(reply, TextSendMessage(text=apple))

	if user_msg == f'價格':
		img_url, msg = selenium_crawler()
		line_bot_api.reply_message(reply, [

				TextSendMessage(text=msg)
			]
		)  # ImageSendMessage(base_url=img_url),

	msg = reply_messages()
	line_bot_api.reply_message(
			reply, [
				TextSendMessage(text=msg)
				]
	)


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
