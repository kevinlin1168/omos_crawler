from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import sqlite3
import datetime

def cwbCrawler(number = None):

    driver = webdriver.Chrome()

    driver.get('https://www.cwb.gov.tw/V8/C/W/week.html')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 以 BeautifulSoup 解析 HTML 程式碼
    tbodys = soup.find_all('tbody')
    for tbody in tbodys:
        countryName = tbody.find('span', class_='heading_3').text

        trs = tbody.find_all('tr')
        dayData = []
        for tr in trs:
            daytime = []
            for i in range(1, 8):
                day = tr.find('td', headers=f'day{i}')
                signal = day.find('img')['alt']
                temperature = day.find('span', class_='tem-C').text.replace('\u2002', '').split('-')
                lowerTemperature = temperature[0]
                upperTemperature = temperature[1]
                obj = {
                    'signal': signal,
                    'lowerTemperature': lowerTemperature,
                    'upperTemperature': upperTemperature
                }
                daytime.append(obj)
            dayData.append(daytime)
        insertData(dayData, countryName)

def createTable():
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS weather(date text,time integer, country text, signal text, lower_temperature real, upper_temperature real)''')
    con.commit()
    con.close()

def insertData(data, countryName):
    today = datetime.date.today()
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    for i in range(len(data)):
        for j in range(len(data[i])):
            try:
                weatherData = data[i][j]
                date = today + datetime.timedelta(days=j)
                cur.execute(f"INSERT INTO weather (date, time, country ,signal, lower_temperature, upper_temperature) VALUES ('{date}', '{i}', '{countryName}', '{weatherData['signal']}', '{weatherData['lowerTemperature']}', '{weatherData['upperTemperature']}')")
                con.commit()
            except:
                print("An exception occurred")
    cur.close()
    

if __name__ == '__main__':
    # try:
        createTable()
        cwbCrawler()
    # except:
    #     print("An exception occurred")
    