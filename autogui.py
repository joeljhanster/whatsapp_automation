from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import pickle
from emoji import emojize
from tkinter import *
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def linebreak():
    linebreak = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
    return linebreak

driver_path = './chromedriver'

window = Tk()
window.title("Welcome to HiMart Whatsapp Automation!")
window.geometry('650x800')

lbl = Label(window, text="Create Product List for Whatsapp", font=("Arial Bold", 28))
lbl.grid(column=0,row=0)

txt = Entry(window, width=50)
txt.grid(column=0,row=1)

product = Label(window, text='', font=("Arial", 14))
product.grid(column=0,row=2)

def clicked():
    # print(product['text'])
    product['text'] += txt.get() + '\n'
    txt.delete(0, 'end')
    product.configure(text=product['text'])

btn = Button(window, text="Add Product Link", font=("Arial"), command=clicked)
btn.grid(column=1,row=1)

def clear():
    txt.delete(0, 'end')
    product.configure(text='')

reset_btn = Button(window, text="Clear", font=("Arial"), command=clear)
reset_btn.grid(column=2,row=1)

product_lst = Label(window, text="", font=("Arial", 14))
product_lst.grid(column=0,row=4)

def product_list():
    lst = product['text'].split('\n')
    
    msg = "This is the product list:\n\n"

    for site in lst:
        if site == '':
            break
        try:
            req = Request(site, headers = {"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(urlopen(req), features='lxml')
            get_title = soup.title.string

            get_title = get_title.replace('&/&', '*\n*')
            get_title = get_title.replace(' - hiMart', '')

            msg = msg + '*' + get_title + '*\n' + site + '\n\n'

        except Exception as e:
            print (e)
            print("Invalid website")
    
    product_lst["text"] = msg

done_btn = Button(window, text="Done", font=("Arial"), command=product_list)
done_btn.grid(column=0,row=3)

lbl2 = Label(window, text="Choose Whatsapp Groups to send message", font=("Arial Bold", 18))
lbl2.grid(column=0,row=5)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
chk1 = Checkbutton(window, text="Toa Payoh Blk124", variable=var1)
chk2 = Checkbutton(window, text="Toa Payoh Group 3", variable=var2)
chk3 = Checkbutton(window, text="Lalala", variable=var3)
chk4 = Checkbutton(window, text="Test", variable=var4)
chk1.grid(column=0,row=6)
chk2.grid(column=0,row=7)
chk3.grid(column=0,row=8)
chk4.grid(column=0,row=9)

lbl3 = Label(window, text="Do you want to add image?", font=("Arial Bold", 18))
lbl3.grid(column=0,row=10)

selected = IntVar()
img_chk = Checkbutton(window, text="Add Image", variable=selected)
img_chk.grid(column=0,row=11)

def send_message(message, wait):
    # Input message
    input_path = '//div[@class="_2S1VP copyable-text selectable-text"][@data-tab="1"]'
    msg_box = wait.until(EC.presence_of_element_located((By.XPATH, input_path)))

    msg_box.send_keys(message)
    msg_box.send_keys(Keys.ENTER)

def add_image(wait):
    # Click attachment clip
    attachment = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@title,"Attach")]')))
    attachment.click()

    time.sleep(3)

    # Click to upload file
    photo = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@class,"_1azEi")]')))
    photo.click()

def checker(actual_msg, wait):
    if upload_var.get() == 1:
        send_message(actual_msg, wait)
        return True
    return False

def execute_whatsapp():
    try:
        # Save log in details
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=./User_Data')

        # Open Chrome browser
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        driver.get('https://web.whatsapp.com/')
        
        wait = WebDriverWait(driver=driver,timeout=60)

        group_lst = []
        # if var1.get():
        #     group_lst.append(chk1["text"])
        # if var2.get():
        #     group_lst.append(chk2["text"])
        if var3.get() == 1:
            group_lst.append(chk3["text"])
        if var4.get() == 1:
            group_lst.append(chk4["text"])
        
        print (group_lst)

        actual_msg = product_lst['text']
        actual_msg = actual_msg.replace("This is the product list:\n\n", '')
        actual_msg = actual_msg.replace('\n',linebreak())

        for groupname in group_lst:
            user = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@title,"{}")]'.format(groupname))))
            time.sleep(3)
            user.click()

            if (selected.get() == 1):
                add_image(wait)
                photo_uploaded = wait.until(EC.presence_of_element_located((By.XPATH, '//img[contains(@class,"_1a4Ru")]')))
                send_message(actual_msg, wait)
            else:
                send_message(actual_msg,wait)

        time.sleep(5)
        driver.quit()

    except Exception as e:
        print (e)
        time.sleep(10)
        driver.quit()

confirm_btn = Button(window, text="Confirm & Send", font=("Arial"), command=execute_whatsapp)
confirm_btn.grid(column=0,row=13)

window.mainloop()