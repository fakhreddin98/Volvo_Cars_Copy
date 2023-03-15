import os
import shutil
import datetime
import filecmp
import win32api
import time

def copy_files(source_folder, dest_folder):
    # Skapa mappen i destinationen om den inte finns
    os.makedirs(dest_folder, exist_ok=True)

    # Gå igenom alla filer och mappar i källmappen
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        dest_item = os.path.join(dest_folder, item)

        if item.lower() in ('system volume information', 'recycler', '$txrajnl.dat'):
            # Hoppa över vissa filer och mappar
            continue

        if os.path.isdir(source_item):
            # Om det är en mapp, kör funktionen rekursivt för att kopiera mappen
            copy_files(source_item, dest_item)
        elif os.path.isfile(source_item):
            # Om det är en fil, kopiera filen om den inte redan finns i mappen med samma storlek och ändringsdatum
            if os.path.exists(dest_item) and filecmp.cmp(source_item, dest_item):
                print(f"Fil redan flyttad: {item}")
            else:
                try:
                    shutil.move(source_item, dest_folder)
                    print(f"Flyttade filen: {item}")
                except Exception as e:
                    print(f"Misslyckades med att kopiera filen: {item}")
                    print(e)
    #Ta bort de tomma mappar
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        if os.path.isdir(source_item) and not os.listdir(source_item):
            try:
                os.rmdir(source_item)
            except Exception as e:
                print(e)
connected_drives = set()
while True:
    new_drives = [d for d in 'DEFGHIJKLMNOPQRSTUVWXYZ' if d not in connected_drives and win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
    if new_drives:
        connected_drives.update(new_drives)

    disconnected_drives = connected_drives - {d for d in connected_drives if win32api.GetLogicalDrives() & (1 << ord(d) - 65)}
    if disconnected_drives:
        print("Usb(s) frånkopplad:", ", ".join(disconnected_drives))
        connected_drives -= disconnected_drives

    time.sleep(1)

    for new_drive in new_drives:
        try:
            volume_info = win32api.GetVolumeInformation(new_drive + ':\\')
            print(f"Hittade enhet: {volume_info[0]}")

            # Hitta alla filer och mappar på enheten
            source_folder = new_drive + ':\\'
            items = os.listdir(source_folder)

            if items:
                # Skapa en mapp på skrivbordet för kopierade filer
                now = datetime.datetime.now()
                time_str = now.strftime('%H')
                time_shift_str = now.strftime('%H')
                # If sats som är beronde av tiden och enligt tiden då ska data ligga på shiftens mapp.
                if  (0 <= int(time_shift_str)  < 8):
                    shift_str = "Natt"
                if  (8 <= int(time_shift_str)  < 16):
                    shift_str = "Dag"
                if  (16 <= int(time_shift_str)  < 23):
                    shift_str = "Kväll"
                date_str = now.strftime('%Y-%m-%d')

                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'testing')
                drive_folder = os.path.join(desktop_path, volume_info[0], shift_str, date_str, f"Kl {time_str}")
                os.makedirs(drive_folder, exist_ok=True)

                # Kopiera filerna och mapparna till mappen
                copy_files(source_folder, drive_folder)
            else:
                print("Inga filer att Flytta på enheten: " + new_drive)
        except Exception as e:
            print(f"Misslyckades med att hämta information från enheten {new_drive}: {e}")
