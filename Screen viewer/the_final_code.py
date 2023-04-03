

import tkinter
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import requests

pyautogui.FAILSAFE = False


text = 'https://raw.githubusercontent.com/fakhreddin98/Volvo_Cars_projects/main/Screen%20viewer/links.txt'
response = requests.get(text)
link_lines = response.text.strip().split('\n')

delay_txt = "https://raw.githubusercontent.com/fakhreddin98/Volvo_Cars_projects/main/Screen%20viewer/delay.txt"
response = requests.get(delay_txt)
dealy_lines = response.text.strip().split('\n')
pyautogui.FAILSAFE = False

def move_mouse():
    pyautogui.moveTo(150, 150, duration=2)
    pyautogui.moveTo(200, 200, duration=2)



def clear_item():
    delay_spinbox.delete(0, tkinter.END)
    delay_spinbox.insert(0, "10")
    Url_entry.delete(0, tkinter.END)
    
urls_lists = []
urls_list  = []
delay_list = []

def add_item():
    Url = Url_entry.get()
    Url = Url.replace(" ", "").replace("\n","")
    delay = int(delay_spinbox.get())

    urls = [Url, delay]
    tree.insert('',0, values=urls)

    urls_lists.append(urls)
    urls_list.append(urls[0])
    delay_list.append(urls[1])

    clear_item()


def remove_url():
    selection = tree.selection()
    if selection:
        for item in selection:
            index = int(item.split('I')[-1]) - 1
            tree.delete(item)
            del urls_list[index]
  

def clear_all():
    clear_item()    
    tree.delete(*tree.get_children())
    global urls_lists, urls_list, delay_list
    print(urls_lists)    
    print(urls_list)
    print(delay_list)

    urls_lists = []    
    urls_list  = []
    delay_list = []

def default_list():
    global urls_lists, urls_list, delay_list, urls


    urls_lists = []
    urls_list  = []
    delay_list = []
    for delay in dealy_lines:
        for link in link_lines:
            urls_lists.append([link, delay])
            urls_list.append(link)
            delay_list.append(delay)

    # Lägg till länkarna i trädet
    for urls in urls_lists:
        tree.insert('', 0, values=urls)


from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def Start():
    urls = urls_list
    delays = [int(delay) for delay in delay_list] # antar att delay_list är en lista med förseningar för varje URL i urls_list
    
    edge_path = r"C:\Users\fkabawe\Documents\msedgedriver.exe"
    edge_options = Options()
    edge_options.add_argument('user-data-dir=C:\\Users\\fakhe\\AppData\\Local\\Microsoft\\Edge\\User Data')
    edge_options.add_argument('--start-maximized')

    print ("här är urls" ,urls)
    driver = webdriver.Edge(service=Service(executable_path=edge_path), options=edge_options)
    driver.maximize_window()
    driver.get(urls[0])
    delay = delays[0]

    for url, delay in zip(urls[1:], delays[1:]):
        driver.execute_script(f"window.open('{url}')")
        time.sleep(delay)

    tab_handles = driver.window_handles

    current_tab = 0

    while True:
        current_tab = (current_tab + 1) % len(tab_handles)
        driver.switch_to.window(tab_handles[current_tab])
        move_mouse()
        try:
            refresh_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "reportAppBarRefreshBtn")))
            ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
            print("refresh utförd")
            time.sleep(delays[current_tab])

        except:
            
            time.sleep(delays[current_tab])
            continue


#gui design
window = tkinter.Tk()
window.title("Url chooser")

frame = tkinter.Frame(window)
frame.pack(padx=20, pady=10)

Url_label = tkinter.Label(frame, text="Ange Url")
Url_label.grid(row=0, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)

Url_entry = tkinter.Entry(frame)
Url_entry.grid(row=1, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)


delay_label = tkinter.Label(frame, text="delay in sec")
delay_label.grid(row=2, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)
delay_spinbox = tkinter.Spinbox(frame, from_=10, to=100)
delay_spinbox.grid(row=3, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)


add_url_button = tkinter.Button(frame, text = "Add item", command = add_item)
add_url_button.grid(row=4, column=2, columnspan=3, sticky="news", padx=20, pady=5)

columns = ('Url', 'delay')
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('Url', text='Url')
tree.heading('delay', text='delay')
    
tree.grid(row=5, column=0, columnspan=3, padx=20, pady=10)


start_button = tkinter.Button(frame, text="Börja visningen", command=Start)
start_button.grid(row=6, column=0, columnspan=3, sticky="news", padx=20, pady=5)

delete_button = tkinter.Button(frame, text="Ta bort", command=remove_url)
delete_button.grid(row=7, column=0, columnspan=3, sticky="news", padx=20, pady=5)

default_button = tkinter.Button(frame, text="Standard webbsidor", command=default_list)
default_button.grid(row=8, column=0, columnspan=3, sticky="news", padx=20, pady=5)

Clear_button = tkinter.Button(frame, text="Ta bort allt", command=clear_all)
Clear_button.grid(row=9, column=0, columnspan=3, sticky="news", padx=20, pady=5)


window.mainloop()
