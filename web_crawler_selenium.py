import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import datetime
import time

search_item = mgs_event.message.text
search_item = search_item.replace("%", "")

url = f'https://www.letao.com.tw/yahoojp/auctions/history.php?category=0&p={search_item}&seller='

driver_path = r'D:\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(driver_path)
# driver = webdriver.Chrome()


driver.get(url)
time.sleep(3)

df = pd.DataFrame()
linkList = []  # 建立一個空的 list 來放置連結
itemIdList = []  # 建立一個空的 list 來放置產品

amounts = driver.find_element_by_class_name("m2ItemPosVsCnt")
ats = amounts.text 
ats = ats.split(' ')[2]
ats = ats.replace("件", "")
ats = ats.replace(" ", "")
if ats == "":
    print("未收到關鍵字，請輸入「關鍵字」搜尋...")
    driver.close()
    time.sleep(2)
    exit()
ats = int(ats)
print(ats)
if ats > 500:
    ats = str(ats)
    print("共找到"+ats+"項拍賣品：您搜尋的項目太多了，請改用其他「關鍵字」搜尋...")
    driver.close()
    time.sleep(2)
    exit()
elif ats == 0:
    print("沒找到項目，請改用其他「關鍵字」搜尋...")
    driver.close()
    time.sleep(5)
    exit()
else:
    ats = str(ats)
    print("共找到"+ats+"項拍賣品，請稍候...")

pcount = 1
while True:
    driver.find_element_by_xpath('/html/body/div[11]/div[2]/div/div[3]/span[*]/a[contains(@title,"下一頁")]').click()
    url = driver.current_url
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.find('a', title='下一頁')

    a_tag_all = driver.find_elements_by_xpath('//html/body/div[11]/div[2]/div/div[2]/table/tbody/*/td[2]/table/tbody/tr[1]/td/a[@href]')
    # while a_tag != None: (本來想用此做迴圈，但因driver.find_elements_by_xpath不能==None，會報錯，無法使用。可改搭配try與except)
    for f in range(len(a_tag_all)):
        y = f * 5 + 3
        y = str(y)
        a_tag = driver.find_element_by_xpath('//html/body/div[11]/div[2]/div/div[2]/table/tbody/tr['+y+']/td[2]/table/tbody/tr[1]/td/a')
        link1 = a_tag.get_attribute('href')
        itemID = link1.replace('https://www.letao.com.tw/yahoojp/auctions/item.php?aID=', '')
        f = f + 1
        linkList.append(link1)
        itemIdList.append(itemID)
    
    if next_page != None:
        print("第 %s 頁" % pcount)
        datas = pd.read_html(url, encoding='unicode')  # 用 unicode才能解決亂碼問題
        data4 = (datas[4])
        # df = df.append(data4, ignore_index=True ,sort=True)
        df = df.append(data4, ignore_index=True)
        pcount = pcount + 1
        time.sleep(3)
    else:
        print("第 %s 頁" % pcount)
        datas = pd.read_html(url, encoding='unicode')  # 用 unicode才能解決亂碼問題
        data4 = (datas[4])
        # df = df.append(data4, ignore_index=True, sort=True)
        df = df.append(data4, ignore_index=True)
        break

print("沒有下一頁")
df2 = df.iloc[:, 2:3]
df3 = df2.dropna(how="any")
df4 = df3[~df3[2].isin(["得標價"])]  # 通过~取反，选取"2"列中不包含"得標價"的行
# df2.drop(df.index[[0,1]], inplace = True) 刪第 index = 0,1行
df5 = df4.rename(columns={2:'temp'})  # python——修改Dataframe列名的方法(2-->'temp': 舊換成新)
# df2=df2.columns = ['temp']
df6 = df5.reset_index()
df7 = df6.drop(["index"], axis=1)
# train_data = np.array(df8)#np.ndarray()
df8 = df7.values
pricesList = []
timeList = []
for i in range(0, len(df8)):
    str1 = df8[i]
    str1 = str(str1)
    i = i + 1
    if "円" in str1:
        str_split = str1.split('円')[0]
        strNoDot_price = str_split.replace(",", "")
        strNoDot_price = strNoDot_price.replace("['", "")
        int_price = int(strNoDot_price)
        int_price = int(int_price*0.28) 
        pricesList.append(int_price)
        
        times = str1.split('円')[1]
        times_split = times.split('  ')[2]
        time1 = times_split.split('\\')[0]
        # regex = r'(\d+\/\d+)'
        # time1 = re.findall(regex, times)
        timeList.append(time1)    
    else:
        print()
print(pricesList)
print(timeList)
print(linkList)
print(itemIdList)
# 将列表a，b转换成字典
dictData = {"itemID": itemIdList, "price": pricesList, "time": timeList, "link": linkList, }
df10 = pd.DataFrame(dictData)  # 将字典转换成为数据框
df10 = df10.drop_duplicates()

_time = datetime.date.today()
_time = str(_time)

driver.close()
