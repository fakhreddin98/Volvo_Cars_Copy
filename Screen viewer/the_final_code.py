# Importera nödvändiga bibliotek för att skapa GUI och för att automatisera webbläsaren
import tkinter
from tkinter import ttk
import datetime
from tkinter import messagebox
import tkinter as tk
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui


# Funktionen clear_item tar bort innehållet i delay_spinbox och Url_entry,
# och sätter delay_spinbox till standardvärdet "10" igen.
def clear_item():
    delay_spinbox.delete(0, tkinter.END)
    delay_spinbox.insert(0, "10")
    Url_entry.delete(0, tkinter.END)
    
urls_lists = []
urls_list  = []
delay_list = []

# Funktionen "add_item" hämtar url-adressen och fördröjningen från användarens inmatning i gränssnittet
# Den lägger sedan till url-adressen och fördröjningen i en lista och lägger till det i Treeview-fönstret
# Den lägger också till url-adressen i en annan lista med bara url-adresser, för senare användning
# Funktionen anropar sedan "clear_item" för att tömma inmatningsfälten i gränssnittet
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


# Funktionen "remove_url" tar bort den valda URL:en från Treeview och urls_list.
# Om en URL har valts i Treeview så tas den bort från Treeview och urls_list med hjälp av dess index.
def remove_url():
    selection = tree.selection()
    if selection:
        for item in selection:
            index = int(item.split('I')[-1]) - 1
            tree.delete(item)
            del urls_list[index]
  

# Funktionen clear_all tar bort alla url:er från treeview-komponenten och rensar inmatningsfälten.
# clear_item är en annan funktion som rensar delay_spinbox och Url_entry-fälten
# tree.delete (* tree.get_children ()) tar bort alla barnnoder i trädet (treeview)
def clear_all():
    clear_item()    
    tree.delete(*tree.get_children())
    global urls_lists, urls_list, delay_list
    urls_lists = []
    urls_list  = []
    delay_list = []

def scroll_to_bottom_and_back(driver):
    # Hämta höjden på webbsidan och höjden av webbläsarfönstret
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    window_height = int(driver.execute_script("return window.innerHeight"))

    # Bestäm hur mycket som ska scrollas per iteration
    scroll_by = int(window_height / 100)

    # Scrolla sidan långsamt genom att göra flera små scrollningar med mellanrum
    scroll_count = 0
    for i in range(0, total_height, scroll_by):
        driver.execute_script(f"window.scrollTo(0, {i})")
        scroll_count += 1
        if scroll_count % 10 == 0:
            time.sleep(10)
        time.sleep(0.1)    
    # Scrolla tillbaka till toppen av sidan när scrollningen är klar
    driver.execute_script("window.scrollTo(0, 0)")


def mouse_move():
    # Flytta muspekaren 100 pixlar till höger och 100 pixlar nedåt
    pyautogui.moveRel(10, 10)
    pyautogui.moveRel(-10, -10)


# Funktion för att öppna flera flikar och uppdatera en rapport på varje flik
def Start():
    # Hämta en lista med webbadresser
    urls = urls_list
    # Hämta värdet från en spinnbox och använda det som en förseningstid för att uppdatera rapporterna
    delays = [int(delay) for delay in delay_list] # antar att delay_list är en lista med förseningar för varje URL i urls_list
    
    # Ange sökvägen till Edge-webbläsarens drivrutin
    edge_path = r"C:\Users\fkabawe\Documents\msedgedriver.exe"
    # Skriv ut webbadresserna som är sparade i listan 'urls'
    print ("här är urls" ,urls)
    # Skapa en instans av webbläsaren Edge med hjälp av drivrutinen
    driver = webdriver.Edge(executable_path=edge_path)

    # Öppna den första webbadressen i listan i en flik
    driver.get(urls[0])
    delay = delays[0]

    # Loopa genom alla webbadresser i listan och öppna dem i nya flikar
    for url, delay in zip(urls[1:], delays[1:]):
        driver.execute_script(f"window.open('{url}')")
        time.sleep(delay)

    # Hämta en lista med flikhandtag
    tab_handles = driver.window_handles

    # Välj den första fliken som ska uppdateras
    current_tab = 0

    # Loopa tills användaren stänger programmet
    while True:
        # Välj nästa flik i listan med flikhandtag
        current_tab = (current_tab + 1) % len(tab_handles)
        driver.switch_to.window(tab_handles[current_tab])
        mouse_move()
        try:
            # Vänta i upp till 10 sekunder på att uppdateringsknappen blir klickbar
            refresh_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "reportAppBarRefreshBtn")))
            # Klicka på uppdateringsknappen
            ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
            print("refresh utförd")
            # Vänta i 'delay' sekunder innan nästa uppdatering
            time.sleep(delays[current_tab])

        except:
            # Om uppdateringsknappen inte blir klickbar, vänta i 'delay' sekunder innan nästa försök
            scroll_to_bottom_and_back(driver)
            time.sleep(delays[current_tab])
            # Fortsätt till nästa iteration av loopen
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

Clear_button = tkinter.Button(frame, text="Ta bort allt", command=clear_all)
Clear_button.grid(row=8, column=0, columnspan=3, sticky="news", padx=20, pady=5)


window.mainloop()
