import requests
import urllib3
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
import time
import datetime
import random

urllib3.disable_warnings()  # to disable warning messages

courseno = 0

url = {
    "login": "https://courseselection.ntust.edu.tw/Account/Login",
    "extrajoin": "https://courseselection.ntust.edu.tw/AddAndSub/B01/ExtraJoin",
    "captcha": "https://courseselection.ntust.edu.tw/Account/GetValidateCode",
    "checking": "https://courseselection.ntust.edu.tw/ChooseList/D03/D03"
}

headers = {
    "Content-Type": "text/html; charset=utf-8"
}

headers_extrajoin = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

data_login = {}

data_extrajoin = {
    "CourseNo": courseno,
    "type": "3"
}


def text_read(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip() for line in file]  # write lines into list
        return lines


def verifycode(filename):
    img = Image.open('img.png')
    imgry = img.convert('L')
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    text = pytesseract.image_to_string(out)
    verifycode = text.replace(' ', '').replace('\n', '').replace(':', '')\
        .replace('+', '').replace('-', '').replace('*', '').replace('/', '')\
        .replace('.', '').replace('|', '').replace('"', '').replace('=', '')\
        .replace('_', '')
    # print(captcha)
    return verifycode


def login():
    while True:
        response = session.get(url["login"], headers=headers, verify=False)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content, features='html.parser')
            soup.encoding = 'utf-8'
            token = soup.select('body > div > div > div > div > div > div > form > input[type=hidden]')[0].get('value')
            # print(token)
            response = session.get(url["captcha"], verify=False)
            open('img.png', 'wb').write(response.content)
            captcha = verifycode('img.png')

            # print(captcha)
            data_login["__RequestVerificationToken"] = token
            data_login["UserName"] = studentno
            data_login["Password"] = password
            data_login["VerifyCode"] = captcha

            r_temp = session.post(url["login"], data=data_login)
            if r_temp.status_code == requests.codes.ok:
                soup = BeautifulSoup(r_temp.content, features='html.parser')
                soup.encoding = 'utf-8'
                try:
                    if(token != soup.select('body > div > div > div > div > div > div > form > input[type=hidden]')[0].get('value')):
                        print(datetime.datetime.now().strftime("%H:%M:%S") + " Wrong Captcha")
                except:
                    print("login complete")
                    # print(r_temp.text)
                    break


with requests.Session() as session:
    lines = text_read("login_data.txt")
    course_list = lines[0].split()
    studentno = lines[1]
    password = lines[2]
    credit_current = int(lines[3])
    credit_course = int(lines[4])

    login()

    count = 1

    while True:
        courseno = course_list[random.randint(0, len(course_list) - 1)]
        print(courseno)
        print(datetime.datetime.now().strftime("%H:%M:%S") + " Attempts : ", count)
        # print(datetime.datetime.now().strftime("%H:%M:%S") + " Attempts : %d" % count)
        response = session.post(url["extrajoin"], headers=headers_extrajoin, data=data_extrajoin)

        count = count + 1

        if (count % 10) == 0:
            checking = session.get(url["checking"], headers=headers)
            soup = BeautifulSoup(checking.content, features='html.parser')
            credit_after = int(soup.select('#PrintArea > div.modal-body > div')[0].string.replace(' ','').replace('\n','').replace('\r','').replace('總學分數:',''))
            # print(credit_after)
            if (credit_current + credit_course) == credit_after:
                print("Mission Complete")
                break
        time.sleep(1)
