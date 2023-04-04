# Koden är ett Python-skript som flyttar filer från en källmapp till en målmapp baserat på filtyp. 
# Koden innehåller en funktion "move_files" som är huvudfunktionen och tar två argument, källmappen och målmappen. 
# Källmappen och dess undermappar genomsöks rekursivt för att hitta filer som sedan flyttas till lämpliga målmappar baserat på deras filtyp. 
# Om filen är en mapp, flyttas filerna i den mappen rekursivt till motsvarande målmapp baserat på filtyp. 
# Funktionen tar också bort tomma mappar i källmappen efter att alla filer har flyttats.

# Koden använder moduler som os, shutil, filecmp, win32api och time för att hantera filer och mappar, jämföra filer, interagera med operativsystemet och hantera tid.
# Det finns också tre hjälpfunktioner, "move_zip_file", "move_mf4_file" och "move_else_file", som flyttar filer med .zip, .mf4 och .dat filtyp, respektive andra filtyper till lämpliga målmappar.
# Slutligen finns det en funktion "remove_empty_folders" som tar bort tomma mappar i en mapp.
# Koden söker också kontinuerligt efter nya anslutna enheter, och om en ny enhet hittas som innehåller en mapp med en viss namnstruktur
# körs huvudfunktionen för att flytta filer från den mappen till lämpliga målmappar.

# Koden är skriven och testad av Fakhreddin kabawe
# Om du behöver hjälp med koden, kontakta mig på [fakhreddin.kabawe@icloud.com] Eller på [+46721270123]
# en detaljerad rapport om koden finns på https://docs.google.com/document/d/1zs4iZ8eTRHo7vqXMQJBo3UMa03LaC13MpeIjZ2uMUOc/edit?usp=sharing

# win32api är inte installerad på alla datorer av sig själv och "pip install pywin32" behöver köras
# Koden flyttar bort filerna om man vill att den ska kopiera filerna då ska man byta "shutil.move" till "shutil.copy2"
# Och ta bort koden som ta bort mapparna.
# [WinError 32] The process cannot access the file because it is being used by another process: 'J:\\bugreport-Jarmo@2023-04-03_20-41-31-SXCSTF.zip'

import os                 # Importerar funktioner för att interagera med operativsystemet
import shutil             # Importerar funktioner för att hantera filer och mappar
import win32api           # Importerar funktioner för att interagera med Windows-API:et
import time               # Importerar funktioner för att hantera tid och vänta mellan operationer
import subprocess
import glob

#Funktionen move_files flyttar filer från en källmapp till en målmapp baserat på filtyp.

'''
Denna funktion flyttar filer från en källmapp till en destinationmapp baserat på filtypen. 
Funktionen räknar först antalet filer i källmappen, skapar sedan en destinationmapp och flyttar sedan filerna enligt deras filtyp.
För varje fil kontrolleras filtypen genom att kontrollera filändelsen med hjälp av os.path.splitext(). 
Om filen har en ".rar" eller ".zip" filändelse, flyttas den till en annan mapp med hjälp av en separat funktion move_zip_file().
Om filen har ".mf4" eller ".dat" filändelse flyttas den till en annan mapp med hjälp av move_mf4_file(). 
Alla andra filer flyttas till en annan mapp med hjälp av move_else_file().
För varje flyttad fil skrivs en beskrivning av filen till konsolen, t.ex. "Flyttade filen 1/10: filnamn.txt". 
När alla filer har flyttats, tas tomma mappar i källmappen bort och ett meddelande skrivs ut till konsolen för 
att informera användaren om att flyttningen är klar och enheten kan tas bort.
Detta är en användbar funktion för att organisera och flytta filer från en mapp till en annan baserat på filtyp. 
Funktionen kan användas för att flytta filer från en enhet till en annan eller för att organisera filer på en dator.
'''
def move_files(source_folder, dest_parent_folder):
    total_files = 0
    num_files = 0
    
    for root, dirs, files in os.walk(source_folder):
        total_files += len(files)
    
    dest_folder = os.path.join(dest_parent_folder)
    os.makedirs(dest_folder, exist_ok=True)

    for root, dirs, files in os.walk(source_folder):
        for item in files:
            source_item = os.path.join(root, item)
            extension = os.path.splitext(item)[1].lower()

            if extension in ('.rar', '.zip'):
                move_zip_file(source_item)
                
            elif extension in ('.mf4', '.dat'):
                move_mf4_file(source_item)

            else:
                move_else_file(source_item)

            num_files += 1
            if num_files != total_files + 1:
                print(f"{num_files}/{total_files} Ta inte bort {volume_info[0]}, Flyttade filen : {item[:20]}")

    
    remove_empty_folders(source_folder)

    if num_files + 1 == total_files + 1:
        print(f"\nAlla filer har nu flyttats från {volume_info[0]} till destinationmappen. \nDu kan nu tryggt ta bort  {volume_info[0]}  :) \n")
        remove_everything_from_folder(source_folder)

def move_zip_file(source_item):
    """
    Funktionen move_zip_file flyttar en zip-fil från källmappen till en zip-mapp i målmappen.
    zip_folder är sökvägen till zip-mappen där filen ska flyttas till.
    os.makedirs används för att skapa zip-mappen om den inte redan finns.
    dest_item är sökvägen för den nya filen i zip-mappen.
    shutil.move används för att flytta filen från källmappen till zip-mappen.
    Ingen utskrift görs i denna funktion.
    """

    folder_name_zip = os.path.splitext(os.path.basename(volume_info[0]))[0].split('_')[0]

    zip_folder = os.path.join(r"C:\Users\E9439007\OneDrive - Volvo Cars\Loggfiler\IHU\Automated IHU Logs - All Vehicles")
    #zip_folder = os.path.join(r"C:\Users\fakhe\Desktop\testing\zip", folder_name_zip)
    os.makedirs(zip_folder, exist_ok=True)
    dest_item = os.path.join(zip_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)


def move_mf4_file(source_item):
    """
    samma som förra men till mf4 och dat filerna
    """
    folder_name_mf4 = os.path.splitext(os.path.basename(volume_info[0]))[0].split('_')[0]

    mf4_folder = os.path.join(r"\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered\New folder", folder_name_mf4 , 'data')
    os.makedirs(mf4_folder, exist_ok=True)
    dest_item = os.path.join(mf4_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)


def move_else_file(source_item):
    """
    samma som förra men till alla filer som inte är mf4, dat, zip eller rar
    """
    else_folder = os.path.join(r"\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered\New folder\else", volume_info[0] , 'else')
    os.makedirs(else_folder, exist_ok=True)
    dest_item = os.path.join(else_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)

def remove_empty_folders(folder):
    """
    Tar bort tomma undermappar i en mapp.
    """
    if not os.path.exists(folder) or not os.path.isdir(folder):
        return

    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            full_dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(full_dir_path)
            except OSError:
                pass

    try:
        os.rmdir(folder)
        print(f"Removed empty directory: {folder}")
    except OSError:
        pass

def remove_everything_from_folder(source_folder):
    # remove all files in the directory
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print("kunde inte ta bort alla filer försöker igen om 1 sekund")
            time.sleep(1)
            remove_everything_from_folder(source_folder)

if __name__ == '__main__':
    # connected_drives är en mängd som innehåller enhetsbokstäverna för alla anslutna enheter.
    connected_drives = set()
    #En oändlig loop börjar som kontinuerligt söker efter nya anslutna enheter och borttagna enheter.

    while True:
        # new_drives är en lista som innehåller enhetsbokstäverna för nya anslutna enheter som inte redan finns i connected_drives.
        new_drives = [d for d in 'ABDEFGHIJKLMNOPQRSTUVXYZ' if d not in connected_drives and win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
        # Om det finns nya enheter, läggs de till i mängden "connected_drives"
        if new_drives:
            connected_drives.update(new_drives)
        # disconnected_drives är en lista som innehåller enhetsbokstäverna för borttagna enheter från mängden connected_drives.
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
                if '_VPT_PLOPP' in volume_info[0] or 'Info_Logs' in volume_info[0]:
                    # Sätter sökvägen till enheten och listar alla filer i sökvägen
                    source_folder = new_drive + ':\\'
                    items = os.listdir(source_folder)

                    if items:
                        #dest_parent_folder = r'\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered'
                        dest_parent_folder = volume_info[0]
                        drive_folder = os.path.join(dest_parent_folder)
        #                move_files(drive_folder, source_folder)
                        move_files(source_folder, drive_folder)
                    else:
                        # Om enheten inte innehåller "_Data" i volymnamnet, skrivs ett meddelande ut om det.
                        print("Inga filer att Flytta på enheten: " + new_drive)
                else: 
                    print(f"{volume_info[0]} innehåller inte '_VPT_PLOPP eller Info_Logs'.")

            except Exception as e:
                print(e)
