from selenium import webdriver
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from conf import *
import NTUST_verification_code_to_text 
import time
now = 1
pre = 0


chrome_path = "../chromedriver"  
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
web = webdriver.Chrome(options =chrome_options , executable_path = chrome_path)

try:
    web.get('https://stuinfo8.ntust.edu.tw/ntust_stu/stu.aspx')
except:
    alert = web.switch_to.alert
    alert.accept()

try:
    alert = web.switch_to.alert
    alert.accept()
except:
    pass
time.sleep(1)
print("Web Loaded")


studentno = web.find_element_by_name("studentno")
idcard = web.find_element_by_name("idcard")
DropMonth = web.find_element_by_name("DropMonth")
DropDay = web.find_element_by_name("DropDay")
password = web.find_element_by_name("password")
code_box = web.find_element_by_name("code_box")
verify_code = web.find_element_by_id("Image2")

web.get_screenshot_as_file("temp.png")
left = verify_code.location['x']
right = verify_code.location['x'] + verify_code.size['width']
top = verify_code.location['y']
bottom = verify_code.location['y'] + verify_code.size['height']

img = Image.open("temp.png")
img = img.crop((left, top, right, bottom))
verification_code = NTUST_verification_code_to_text.main(img)

studentno.send_keys(studentno_)
idcard.send_keys(idcard_)
DropMonth.send_keys(DropMonth_)
DropDay.send_keys(DropDay_)
password.send_keys(password_)


code_box.send_keys(verification_code)
web.find_element_by_id("Button1").click()
print("Login OK")

web.find_element_by_id("Button5").click()
print("Search Page")
done = False
while (now >= pre):
    web.find_element_by_name("courseno").send_keys(courseid)
    verify_code = web.find_element_by_id("Image2")
    web.get_screenshot_as_file("temp.png")
    left = verify_code.location['x']
    right = verify_code.location['x'] + verify_code.size['width']
    top = verify_code.location['y']
    bottom = verify_code.location['y'] + verify_code.size['height']

    img = Image.open("temp.png")
    img = img.crop((left, top, right, bottom))
    verification_code = NTUST_verification_code_to_text.main(img)
    print(verification_code)

    web.find_element_by_name("rand_box").clear()
    web.find_element_by_name("rand_box").send_keys(verification_code)
    web.find_element_by_id("Button1").click()

    restrict2 = web.find_element_by_id("restrict2")
    now_peop = web.find_element_by_id("now_peop")
    pre = int(restrict2.text.replace('人', ''))
    now = int(now_peop.text.replace('人', ''))
    print("預設", pre, "人")
    print("目前", now, "人")
    if pre > now:
        #print("進ㄌ!")
        web.get('https://stuinfo8.ntust.edu.tw/ntust_stu/stu_menu.aspx')
        web.find_element_by_id("Button1").click()
        time.sleep(0.3)
        if len(web.find_elements_by_id("Button1"))!= 0:
            web.find_element_by_id("Button1").click()
            courseno = web.find_element_by_name("courseno")
            courseno.send_keys(courseid)
            web.find_element_by_id("B_add").click()
            break
        else:
            print("網站錯誤!!")
            web.get('https://stuinfo8.ntust.edu.tw/ntust_stu/query_course.aspx')
            pre  = 0
            now  = 1
    else:
        print("嗚嗚")
    
print("YA")
