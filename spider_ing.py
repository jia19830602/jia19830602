import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

from imgurpython import ImgurClient
import pyimgur
import ENV

client_id = ENV.CLIENT_ID
client_secret = ENV.CLIENT_SECRET
access_token = ENV.ACCESS_TOKEN
refresh_token = ENV.REFRESH_TOKEN
client = ImgurClient(client_id, client_secret, access_token, refresh_token)

x = input("請輸入關鍵字:")
x = x.replace("%", "")

# Chrome Options

# prefs = {"profile.managed_default_content_settings.images": 2}
# options = webdriver.ChromeOptions()
# options.add_experimental_option("prefs", prefs)
# options.binary_location = ENV.GOOGLE_CHROME_BIN
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path=ENV.CHROMEDRIVER_PATH, chrome_options=options)

url = f'https://www.letao.com.tw/yahoojp/auctions/history.php?category=0&p={x}&seller='
driver_path = r'D:\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(driver_path)
driver.get(url)
time.sleep(3)

# amounts = driver.find_element_by_class_name("m2ItemPosVsCnt")
# ats = amounts.text
# ats = ats.split(' ')[2]
# ats = ats.replace("件", "")
# ats = ats.replace(" ", "")
# if ats == "":
#     print("未收到關鍵字，請輸入「關鍵字」搜尋...")
#     driver.close()
#     time.sleep(2)
#     exit()
# ats = int(ats)
# print(ats)
# if ats > 200:
#     ats = str(ats)
#     print(f"共找到 {ats} 項拍賣品：您搜尋的項目太多了，請改用其他「關鍵字」搜尋...")
#     driver.close()
#     time.sleep(2)
#     exit()
# elif ats == 0:
#     print("沒找到項目，請改用其他「關鍵字」搜尋...")
#     driver.close()
#     time.sleep(5)
#     exit()
# else:
#     ats = str(ats)
#     print(f"共找到 {ats} 項拍賣品，請稍候...")

url_part = '//html/body/div[11]/div[2]/div/div[2]/table/tbody/'
price_list = []
price = ''
while True:
    driver.find_element_by_xpath('/html/body/div[11]/div[2]/div/div[3]/span[*]/a[contains(@title,"下一頁")]').click()
    url = driver.current_url
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.find('a', title='下一頁')
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
        price += f'\n{_str}'
    if next_page == None:break

print(price)

PATH = "my_fig.png"


def img():
    plt.figure(figsize=(8.000, 6.000), dpi=100)
    # plt.rcParams['font.sans-serif']=['SimHei']  # 正常顯示中文
    plt.rcParams["axes.unicode_minus"] = False   # 正常顯示負數
    plt.xlabel("Price(JPY)", fontsize=14)
    plt.ylabel("counts", fontsize=14)
    plt.grid(axis='x', linestyle='-.')  # 畫格線
    plt.grid(axis='y', linestyle='-.')
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    n, bins, patches = plt.hist(price_list, 15)  #
    plt.title(f"  {x}  PriceTable", fontsize=24)
    plt.savefig('my_fig.png', dpi=80)  # 解析度

    im = pyimgur.Imgur(client_id)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link


img_url = img()
print(img_url)

plt.show()
driver.close()
