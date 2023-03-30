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

# win32api är inte installerad på alla datorer av sig själv och "pip install pypwin32" behöver köras
# Koden flyttar bort filerna om man vill att den ska kopiera filerna då ska man byta "shutil.move" till "shutil.copy2"
# Och ta bort koden som ta bort mapparna.


import os                 # Importerar funktioner för att interagera med operativsystemet
import shutil             # Importerar funktioner för att hantera filer och mappar
import win32api           # Importerar funktioner för att interagera med Windows-API:et
import time               # Importerar funktioner för att hantera tid och vänta mellan operationer
import subprocess

#Funktionen move_files flyttar filer från en källmapp till en målmapp baserat på filtyp.


def move_files(source_folder, dest_parent_folder):

    """
    Funktionen move_files flyttar filer från en källmapp till en målmapp baserat på filtyp.
    dest_folder_name är namnet på målmappen som ska skapas i den överordnade målmappen dest_parent_folder, baserat på namnet på källmappen.
    os.makedirs används för att skapa målmappen och dess överordnade mappar om de inte redan finns.
    os.listdir används för att hämta en lista över filer och mappar i källmappen.
    Om filen är en mapp, flyttas filerna i den mappen rekursivt till motsvarande målmapp baserat på filtyp.
    Om filen är en fil, används os.path.splitext för att få filtypen och lower för att göra filtypen i små bokstäver.
    Om filtypen är .rar eller .zip flyttas filen med funktionen move_zip_file.
    Om filtypen är .mf4 eller .mf4 flyttas filen med funktionen move_mf4_file.
    Annars flyttas filen med funktionen move_else_file.
    En utskrift sker för varje fil som flyttas.
    Funktionen remove_empty_folders används för att ta bort tomma mappar i källmappen efter att alla filer har flyttats.
    """

    dest_folder_name = os.path.splitext(os.path.basename(source_folder))[0].split('_')[0]
    dest_folder = os.path.join(dest_parent_folder, dest_folder_name)
    os.makedirs(dest_folder, exist_ok=True)

    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        if os.path.isdir(source_item):
            move_files(source_item, dest_folder)
        elif os.path.isfile(source_item):
            extension = os.path.splitext(item)[1].lower()

            if extension in ('.rar', '.zip'):
                move_zip_file(source_item)
                
            elif extension in ('.mf4', '.dat'):
                move_mf4_file(source_item)

            else:
                move_else_file(source_item)

            print(f"Filen flyttad: {item}")

    remove_empty_folders(source_folder)

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
    zip_folder = os.path.join(r"C:\Users\fakhe\Desktop\testing\zip", folder_name_zip , 'zzip')
    os.makedirs(zip_folder, exist_ok=True)
    dest_item = os.path.join(zip_folder, os.path.basename(source_item))
    shutil.move(source_item, dest_item)


def move_mf4_file(source_item):
    """
    samma som förra men till mf4 och dat filerna
    """
    folder_name_mf4 = os.path.splitext(os.path.basename(volume_info[0]))[0].split('_')[0]

    mf4_folder = os.path.join(r"C:\Users\fakhe\Desktop\testing\data", folder_name_mf4 , 'data')
    os.makedirs(mf4_folder, exist_ok=True)
    dest_item = os.path.join(mf4_folder, os.path.basename(source_item))
    shutil.move(source_item, dest_item)


def move_else_file(source_item):
    """
    samma som förra men till alla filer som inte är mf4, dat, zip eller rar
    """
    else_folder = os.path.join(r"C:\Users\fakhe\Desktop\testing\else", volume_info[0] , 'else')
    os.makedirs(else_folder, exist_ok=True)
    dest_item = os.path.join(else_folder, os.path.basename(source_item))
    shutil.move(source_item, dest_item)


def remove_empty_folders(folder):
    """
    Tar bort tomma undermappar i en mapp.
    """
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            try:
                os.rmdir(item_path)
            except Exception as e:
                print(e)



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
                if '_VPT_PLOPP' in volume_info[0] or '_ata' in volume_info[0]:
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
                    print(f"{volume_info[0]} innehåller inte '_VPT_PLOPP '.")

            except Exception as e:
                print()
