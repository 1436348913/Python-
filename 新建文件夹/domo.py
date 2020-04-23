import requests
from pyquery import PyQuery as pq
import pymysql
from selenium import webdriver
import time
def save():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='demo')
    cursor = db.cursor()
    sql = 'insert into brand(brand_name) values(%s)'
    sql2 = 'insert into habiliment(h_name,h_price,brand_name) values(%s,%s,%s)'
    sql3 = 'DELETE FROM brand'
    sql4 = 'truncate table habiliment'
    driver = webdriver.Chrome()
    url = "http://category.dangdang.com/cid10010336.html"
    head = {'user-agent': 'Mozilla/5.0'}
    rw = requests.get(url=url, headers=head)
    doc = pq(rw.text)
    lis = doc('.img_list_content_ul a')
    list_price = []  # 商品价格
    list_topic = []  # 商品标题
    list_sort = []  # 商品品牌
    lis_sort = []
    for li in lis.items():
        lis_sort.append(li.text())
        print(lis_sort)
        url_sort = 'http://category.dangdang.com' + str(li.attr('href'))  # 获取每个品牌的url
        driver.implicitly_wait(10)
        driver.get(url_sort)
        s = driver.find_elements_by_css_selector('.paging')  # 筛选有页栏框的页面
        print(url_sort)
        if len(s) != 0:
            rws = requests.get(url=url_sort, headers=head)
            docs = pq(rws.text)
            number = docs('.b').text()
            print(number)
            li_sort = docs('.null:last')  # 获取最后一页页码
            for i in range(0, int(li_sort.text())):
                li_topic = driver.find_element_by_id('search_nature_rg').find_elements_by_class_name('name')
                li_price = driver.find_element_by_id('search_nature_rg').find_elements_by_class_name('price')
                for l in li_topic:
                    list_topic.append(l.find_element_by_tag_name('a').get_attribute("title"))
                for l in li_price:
                    list_price.append(l.find_element_by_tag_name('span').get_attribute("textContent"))
                driver.implicitly_wait(10)
                driver.find_element_by_class_name('next').click()
            for i in range(0, int(number)):
                sort = docs('.block').attr('title')
                list_sort.append(sort)
            print("商品数" + str(len(list_topic)))
            print("价格数" + str(len(list_price)))
            print("品牌数" + str(len(list_sort)))
        if len(s) == 0:
            rws = requests.get(url=url_sort, headers=head)
            docs = pq(rws.text)
            number = docs('.b').text()
            driver.implicitly_wait(10)
            li_topic = driver.find_element_by_id('search_nature_rg').find_elements_by_class_name('name')
            li_price = driver.find_element_by_id('search_nature_rg').find_elements_by_class_name('price')
            for l in li_topic:
                list_topic.append(l.find_element_by_tag_name('a').get_attribute("title"))
            print("现在的长度" + str(len(list_topic)))
            for l in li_price:
                list_price.append(l.find_element_by_tag_name('span').get_attribute("textContent"))
            for i in range(0, int(number)):
                sort = docs('.block').attr('title')
                list_sort.append(sort)
            print("商品数b" + str(len(list_topic)))
            print("价格数b" + str(len(list_price)))
            print("品牌数b" + str(len(list_sort)))
    if len(list_topic) == len(list_price) and len(list_sort) == len(list_price):
        try:
            cursor.execute(sql4)
            db.commit()
        except:
            db.rollback()
        try:
            cursor.execute(sql3)
            db.commit()
        except:
            db.rollback()
        for x in lis_sort:
            try:
                cursor.execute(sql, x)
                db.commit()
            except:
                db.rollback()
        for x in zip(list_topic, list_price, list_sort):
            try:
                cursor.execute(sql2, x)
                db.commit()
            except:
                print("Error: unable to fetch data")
    else:
        print("爬取数目错误！")
    db.close()

def select(name):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='demo')
    cursor = db.cursor()
    subtitle = '%' + name + '%'
    sql = """select h_name,h_price,brand_name from habiliment where h_name like %s"""
    try:
        # 执行SQL语句
        cursor.execute(sql, subtitle)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            h_name = row[0]
            h_price = row[1]
            brand_name = row[2]
            # 打印结果
            print("名称：%s    价格：%s   品牌：%s" % (h_name, h_price, brand_name))
    except:
        print("Error: unable to fetch data")
    db.close()

while 1:
    print("\n如果查询表中已有数据请输入Y，如果需要重新爬取请输入N\n")
    num = input("请输入：")
    if num == 'Y':
        select(input("请输入要查询的衣服种类:"))
    elif num == 'N':
        save()
    else:
        print("输入错误！")
