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

        if item.lower() in ['system volume information', 'recycler']:
            # Hoppa över System Volume Information och Recycler mappar
            continue
        elif item.lower() == '$txrajnl.dat':
            # Hoppa över $TXRAJNL.dat filen
            continue
        elif os.path.isdir(source_item):
            # Om det är en mapp, kör funktionen rekursivt för att kopiera mappen
            copy_files(source_item, dest_item)
        elif os.path.isfile(source_item):
            # Om det är en fil, kopiera filen om den inte redan finns i mappen med samma storlek och ändringsdatum
            if os.path.exists(dest_item) and filecmp.cmp(source_item, dest_item):
                print(f"Fil redan kopierad: {item}")
            else:
                try:
                    shutil.copy2(source_item, dest_folder)
                    print(f"Kopierade filen: {item}")
                except Exception as e:
                    print(f"Misslyckades med att kopiera filen: {item}")
                    print(e)

connected_drives = []
while True:
    new_drives = [d for d in 'FGHIJKLMNOPQRSTUVWXYZ' if d not in connected_drives and win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
    if new_drives:
        print("Usb(s) hittades:", ", ".join(new_drives))
        connected_drives += new_drives
    for drive in connected_drives:
        drive_path = drive + ":\\"
        try:
            volume_info = win32api.GetVolumeInformation(drive_path)
        except win32api.error as e:
            if e.winerror == 21:  # "The device is not ready" error
                time.sleep(1)  # Wait for the drive to become ready

    disconnected_drives = [d for d in connected_drives if not win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
    if disconnected_drives:
        print("Usb(s) frånkopplad:", ", ".join(disconnected_drives))
        connected_drives = [d for d in connected_drives if d not in disconnected_drives]
    time.sleep(1)

    drives = [d for d in 'FGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(d + ':')]
    if drives:
        for drives in new_drives:
            print(f"Hittade enhet: {volume_info[0]}, " + drives)

            # Hitta alla filer och mappar på enheten
            source_folder = drives + ':\\'
            items = os.listdir(source_folder)

            if items:
                # Skapa en mapp på skrivbordet för kopierade filer
                now = datetime.datetime.now()
                date_str = now.strftime('%Y-%m-%d')

                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'testing')
                drive_folder = os.path.join(desktop_path, drives)
                os.makedirs(drive_folder, exist_ok=True)

                dest_folder = None

                # Kolla om en mapp för idag redan finns på enheten
                for folder in os.listdir(drive_folder):
                    if folder.startswith(date_str):
                        dest_folder = os.path.join(drive_folder, folder)
                        break

                if not dest_folder:
                    # Skapa en ny mapp för dagens filer
                    dest_folder = os.path.join(drive_folder, f"{volume_info[0]} {date_str}")
                # Kopiera filerna och mapparna till mappen
                copy_files(source_folder, dest_folder)
            else:
                print("Inga filer att kopiera på enheten: " + drive)