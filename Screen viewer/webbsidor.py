# pip install selenium måste installeras
# https://msedgedriver.azureedge.net/111.0.1661.51/edgedriver_win64.zip

from selenium import webdriver
import time

# Skapa en instans av webbläsaren
#driver = webdriver.Ie()

# Ange sökvägen till Edge-driver
driver_path = r"C:\Users\fkabawe\Documents\msedgedriver.exe"
driver = webdriver.Edge(executable_path=driver_path)
options = webdriver.EdgeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")


# Skapa en lista med webbsidorna att visa
urls = ["https://www.mrfixare.se/", "https://intranet.volvocars.net/"]

# Loopa oändligt och byt mellan webbsidorna med 10 sekunders intervall
while True:
    for url in urls:
        # Ladda webbsidan
        driver.get(url)
        
        # Vänta i 10 sekunder
        time.sleep(10)

# Stäng webbläsaren
driver.quit()
