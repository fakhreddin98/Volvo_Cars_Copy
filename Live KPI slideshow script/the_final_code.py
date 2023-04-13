# Importera nödvändiga bibliotek och moduler
import tkinter  # för att skapa GUI
from tkinter import ttk  # för att använda tkinter-teman
from selenium import webdriver  # för att automatisera webbläsare
from selenium.webdriver.common.action_chains import ActionChains  # för att utföra mus- och tangentbordsåtgärder
from selenium.webdriver.common.by import By  # för att identifiera element på sidan
from selenium.webdriver.support.ui import WebDriverWait  # för att vänta på att vissa villkor uppfylls
from selenium.webdriver.support import expected_conditions as EC  # för att specificera villkor som ska uppfyllas
from selenium.webdriver.edge.service import Service  # för att starta Microsoft webbläsarens service
from selenium.webdriver.edge.options import Options  # för att konfigurera inställningar för Edge
import time  # för att lägga till väntetider i koden
import requests  # för att skicka HTTP-begäran och ta emot svar från en webbserver
from selenium.webdriver.common.keys import Keys


# Hämta länkarna från en textfil på GitHub
text = 'https://raw.githubusercontent.com/fakhreddin98/Volvo_Cars_projects/main/Live%20KPI%20slideshow%20script/links.txt'
response = requests.get(text)
link_lines = response.text.strip().split('\n')

# Hämta fördröjningarna från en annan textfil på GitHub
delay_txt = "https://raw.githubusercontent.com/fakhreddin98/Volvo_Cars_projects/main/Live%20KPI%20slideshow%20script/delay.txt"
response = requests.get(delay_txt)
dealy_lines = response.text.strip().split('\n')

#Skapa tomma listor för länkar och fördröjningar
urls_lists = []
urls_list  = []
delay_list = []


def scroll_to_bottom_and_back(driver):
    # Hämta höjden på webbsidan och höjden av webbläsarfönstret
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    driver.execute_script("window.scrollTo(0, %d);" % (total_height * 0.2))

# Funktion som rensar inputfälten
def clear_item():
    delay_spinbox.delete(0, tkinter.END)
    delay_spinbox.insert(0, "10")
    Url_entry.delete(0, tkinter.END)

# Funktion som lägger till en länk och dess fördröjning i trädet och i listorna
def add_item():
    Url = Url_entry.get().replace(" ", "").replace("\n","")
    delay = int(delay_spinbox.get())
    urls = [Url, delay]
    tree.insert('',0, values=urls)

    urls_lists.append(urls)
    urls_list.append(urls[0])
    delay_list.append(urls[1])

    clear_item()


# Funktion som rensar trädet och listorna samt inputfälten
def clear_all():
    global urls_lists, urls_list, delay_list
    clear_item()
    tree.delete(*tree.get_children())

    print(urls_lists)    
    print(urls_list)
    print(delay_list)
    urls_lists = []    
    urls_list  = []
    delay_list = []

# Funktion som fyller listorna med länkar och fördröjningar från GitHub-textfilerna
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

''' 
Funktion Start startar Selenium-webbläsaren, öppnar webbläsarfönster med angivna länkar och väntar
sedan på att sidorna ska laddas klart enligt angivna tidsfördröjningar. 
Därefter går den igenom webbläsarflikarna, uppdaterar sidan och väntar igen enligt angivna tidsfördröjningar. 
Om en flik inte kan uppdateras väntar den på angiven tidsfördröjning och fortsätter sedan till nästa flik.
'''
def Start():
    urls = urls_list
    delays = [int(delay) for delay in delay_list] # antar att delay_list är en lista med förseningar för varje URL i urls_list

    edge_path = r"C:\Users\kkpi1\Downloads\edgedriver_win64\Driver_Notes\msedgedriver.exe"
    edge_options = Options()
    edge_options.add_argument('user-data-dir=C:\\Users\\kkpi1\\AppData\\Local\\Microsoft\\Edge\\User Data')
    edge_options.add_argument('--start-maximized')

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
        scroll_to_bottom_and_back(driver)
        try:
            # hitta knappen
            button = driver.find_element(By.ID, "app-nav-toggle")

            # titta på om nav toggle är öppen eller stängd
            aria_expanded = button.get_attribute("aria-expanded")

            # tryck på knappen ifall det är öppet
            if aria_expanded == "true":
                ActionChains(driver).move_to_element(button).click(button).perform()
            time.sleep(delays[current_tab])

        except:
            time.sleep(delays[current_tab])
            continue

        try:
            refresh_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "reportAppBarRefreshBtn")))
            ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
            print("refresh utförd")
            time.sleep(delays[current_tab])
        except:
            time.sleep(delays[current_tab])
            continue

# GUI design
# Skapa huvudfönstret och ge det en titel
window = tkinter.Tk()
window.title("Url chooser")

# Skapa en ram och placera den i huvudfönstret med viss marginal
frame = tkinter.Frame(window)
frame.pack(padx=20, pady=10)

# Skapa en etikett för Url och placera den i ramen
Url_label = tkinter.Label(frame, text="Ange Url")
Url_label.grid(row=0, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)

# Skapa en inmatningsruta för Url och placera den i ramen
Url_entry = tkinter.Entry(frame)
Url_entry.grid(row=1, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)

# Skapa en etikett för fördröjning i sekunder och placera den i ramen
delay_label = tkinter.Label(frame, text="delay in sec")
delay_label.grid(row=2, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)

#Skapa en spinbox för fördröjning i sekunder och placera den i ramen
delay_spinbox = tkinter.Spinbox(frame, from_=10, to=100)
delay_spinbox.grid(row=3, column=0 ,columnspan=3, sticky="news", padx=20, pady=5)

# Skapa en knapp för att lägga till en URL och placera den i ramen
add_url_button = tkinter.Button(frame, text = "Add item", command = add_item)
add_url_button.grid(row=4, column=2, columnspan=3, sticky="news", padx=20, pady=5)

# Skapa kolumner för trädvyen
columns = ('Url', 'delay')

# Skapa en trädvy för att visa URL:er och dess fördröjning och placera den i ramen
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('Url', text='Url')
tree.heading('delay', text='delay')
    
tree.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

# Skapa en knapp för att starta visningen av URL:er och placera den i ramen
start_button = tkinter.Button(frame, text="Börja visningen", command=Start)
start_button.grid(row=6, column=0, columnspan=3, sticky="news", padx=20, pady=5)

# Skapa en knapp för att ladda standard webbsidor och placera den i ramen
default_button = tkinter.Button(frame, text="Standard webbsidor", command=default_list)
default_button.grid(row=7, column=0, columnspan=3, sticky="news", padx=20, pady=5)

# Skapa en knapp för att ta bort alla URL:er och placera den i ramen
Clear_button = tkinter.Button(frame, text="Rensa listan", command=clear_all)
Clear_button.grid(row=8, column=0, columnspan=3, sticky="news", padx=20, pady=5)

# Startar koden
window.mainloop()
