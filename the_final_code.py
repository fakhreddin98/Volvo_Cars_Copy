# Det här är en kod som flyttar filer från en ansluten USB-enhet till en specifik mapp på datorns skrivbord. 
# Koden är skriven för att köra i bakgrunden och utföra kopiering automatiskt utan att användaren behöver göra något.
# Koden börjar med att importera nödvändiga moduler och definiera funktionen move_files() som används för att kopiera
# filer och mappar från källmappen till destinationsmappen.
# Sedan finns en while-loop som går igenom alla tillgängliga enheter och letar efter nya anslutna USB-enheter. 
# När en ny enhet hittas skapas en mapp på skrivbordet och filerna i USB-enheten kopieras till den nya mappen. 

# Observera att du kan behöva redigera koden om din dator har fler än en hårddisk eller serveranslutning.
# Koden är anpassat efter att datorn har bara C som är datorns hårddisk
# Har datorn eller servern fler skivor behöver man redigera koden där det står alla bokstäver 
# i While satsen där det såtr 'DEFGHIJKLMNOPQRSTUVWXYZ' ta bort bokstäverna som är hårddiskar 
# eller servers bokstäver. 

# Om du vill ändra var filerna ska flyttas till, kan du redigera raden där mappen drive_folder skapas:

# Från:
# desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'testing')
# drive_folder = os.path.join(desktop_path, volume_info[0], shift_str, date_str, f"Kl {time_str}")

# Till:
# destination_path = "D:\\Backup"
# drive_folder = os.path.join(destination_path, volume_info[0], shift_str, date_str, f"Kl {time_str}")

# Koden är gjort av Fakhreddin kabawe
# Om du behöver hjälp med koden, kontakta mig på [fakhreddin.kabawe@icloud.com] Eller på [+46721270123]
# en detaljerad rapport om koden finns på https://docs.google.com/document/d/1zs4iZ8eTRHo7vqXMQJBo3UMa03LaC13MpeIjZ2uMUOc/edit?usp=sharing

# win32api är inte installerad på alla datorer av sig själv och "pip install pypwin32" behöver köras
# Koden flyttar bort filerna om man vill att den ska kopiera filerna då ska man byta "shutil.move" till "shutil.copy2"
# Och ta bort koden som ta bort mapparna.

import os                 # Importerar funktioner för att interagera med operativsystemet
import shutil             # Importerar funktioner för att hantera filer och mappar
import filecmp            # Importerar funktioner för att jämföra filer
import win32api           # Importerar funktioner för att interagera med Windows-API:et
import time               # Importerar funktioner för att hantera tid och vänta mellan operationer

#Funktion för att flytta filer från en källmapp till en målmapp
def move_files(source_folder, dest_parent_folder):
    # Hämta namnet på den källmapp som ska flyttas
    dest_folder_name = os.path.splitext(os.path.basename(source_folder))[0].split('_')[0]
    # Skapa sökvägen till målmappen
    dest_folder = os.path.join(dest_parent_folder, dest_folder_name)
    # Skapa målmappen om den inte redan finns
    os.makedirs(dest_folder, exist_ok=True)

    # Loopa igenom alla objekt i källmappen
    for item in os.listdir(source_folder):
        # Skapa sökvägar till källobjektet och motsvarande målobjekt
        source_item = os.path.join(source_folder, item)
        dest_item = os.path.join(dest_folder, item)

        # Hoppa över vissa filer/mappar som inte ska flyttas
        if item.lower() in ('system volume information', 'recycler', '$txrajnl.dat'):
            continue

        # Om objektet är en mapp, rekursivt anropa funktionen för att flytta innehållet i mappen till målmappen
        if os.path.isdir(source_item):
            move_files(source_item, dest_folder)
        # Om objektet är en fil, kopiera filen till målmappen
        elif os.path.isfile(source_item):
            # Hämta filstorleken
            size = os.path.getsize(source_item)
            # Sätt en räknare för att hålla koll på hur mycket som har flyttats
            progress = 0
            # Skriv ut en statusmeddelande om filen som flyttas
            print(f"Flyttar filen: {item} ({size} bytes)", end='\r')

            # Om en identisk fil redan finns i målmappen, radera källfilen
            if os.path.exists(dest_item) and filecmp.cmp(source_item, dest_item):
                print(f"Fil redan flyttad: {item}")
                os.remove(source_item)
            # Annars, öppna källfilen och målfilen och kopiera innehållet från källfilen till målfilen
            else:
                try:
                    with open(source_item, 'rb') as fsrc:
                        with open(dest_item, 'wb') as fdst:
                            while True:
                                buf = fsrc.read(1024 * 1024)
                                if not buf:
                                    break
                                fdst.write(buf)
                                # Uppdatera räknaren och skriv ut statusmeddelande med hur mycket som har flyttats
                                progress += len(buf)
                                percent = progress / size * 100
                                print(f"\033[91mDo not unplug the USB driver while files are moving...\033[0m ({percent:.2f}%)", end='\r')
                    # Radera källfilen efter att kopiering har slutförts
                    os.remove(source_item)
                    # Skriv ut en bekräftelse om att filen har kopierats
                    print(f"\033[92mFile copied: {item}\033[0m{' '*50}")
                # Om kopiering misslyckas, skriv ut ett felmeddelande
                except Exception as e:
                    print(f"Misslyckades med att kopiera filen: {item}")
                    print(e)


    # Ta bort eventuella tomma undermappar i källmappen
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        if os.path.isdir(source_item) and not os.listdir(source_item):
            try:
                os.rmdir(source_item)
            except Exception as e:
                print(e)

                
# Skapar en tom mängd som håller koll på anslutna enheter
connected_drives = set()
# Loopar kontinuerligt
while True:
    # Skapar en lista med nya enheter som inte finns i mängden "connected_drives"
    new_drives = [d for d in 'EFGHIJKLMNOPQRSTUVWXYZ' if d not in connected_drives and win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
    # Om det finns nya enheter, läggs de till i mängden "connected_drives"
    if new_drives:
        connected_drives.update(new_drives)
    # Skapar en lista med borttagna enheter från mängden "connected_drives"
    disconnected_drives = connected_drives - {d for d in connected_drives if win32api.GetLogicalDrives() & (1 << ord(d) - 65)}
     # Om det finns borttagna enheter, skrivs ett meddelande ut med enheternas bokstäver och de tas bort från mängden "connected_drives"
    if disconnected_drives:
        print("Usb(s) frånkopplad:", ", ".join(disconnected_drives))
        connected_drives -= disconnected_drives

    time.sleep(1)
    # Loopar igenom alla nya enheter
    for new_drive in new_drives:
        try:
            # Hämtar information om enheten och skriver ut dess namn            
            volume_info = win32api.GetVolumeInformation(new_drive + ':\\')
            print(f"Hittade enhet: {volume_info[0]}")
            # Sätter sökvägen till enheten och listar alla filer i sökvägen
            source_folder = new_drive + ':\\'
            items = os.listdir(source_folder)
            # Om det finns filer, skapas en mapp på skrivbordet och filerna flyttas dit
            if items:
                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'testing')
                drive_folder = os.path.join(desktop_path)
                os.makedirs(drive_folder, exist_ok=True)
#                move_files(drive_folder, source_folder)
                move_files(source_folder, drive_folder)
            else:
                print("Inga filer att Flytta på enheten: " + new_drive)
        except Exception as e:
            print()
