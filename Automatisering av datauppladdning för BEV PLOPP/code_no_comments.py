import os                
import shutil             
import win32api         
import time            
import colorama
from colorama import Fore, Style

colorama.init()

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
                print(Fore.RED + f"Antal flyttade filer {num_files} av {total_files} Ta inte bort {volume_info[0]}, Flyttade filen : {item[:20]}")

    

    if num_files + 1 == total_files + 1:
        remove_everything_from_folder(volume_info)
        print(Fore.GREEN + f"\nAlla filer har nu flyttats från {volume_info[0]} till destinationmappen. \nDu kan nu tryggt ta bort  {volume_info[0]}  :) \n")

def move_zip_file(source_item):

    zip_folder = os.path.join(r"C:\Users\E9439007\OneDrive - Volvo Cars\Loggfiler\IHU\Automated IHU Logs - All Vehicles")
    os.makedirs(zip_folder, exist_ok=True)
    dest_item = os.path.join(zip_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)


def move_mf4_file(source_item):
   
    folder_name_mf4 = os.path.splitext(os.path.basename(volume_info[0]))[0].split('_')[0]

    mf4_folder = os.path.join(r"\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered\New folder", folder_name_mf4 , 'data')
    os.makedirs(mf4_folder, exist_ok=True)
    dest_item = os.path.join(mf4_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)


def move_else_file(source_item):
    else_folder = os.path.join(r"\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered\New folder\else", volume_info[0])
    os.makedirs(else_folder, exist_ok=True)
    dest_item = os.path.join(else_folder, os.path.basename(source_item))
    shutil.copy2(source_item, dest_item)


def remove_everything_from_folder(volume_info):
    for root, dirs, files in os.walk(source_folder, topdown=False):
            try:
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    os.remove(file_path)
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if not dir_name == 'System Volume Information':
                        shutil.rmtree(dir_path)
                        # remove top-level folder
                        shutil.rmtree(volume_info)
                        print(f"All contents of folder {volume_info} have been deleted.")

            except Exception as e:
                        print(Fore.WHITE + "kunde inte ta bort alla filer försöker igen om 1 sekund")
                        time.sleep(1)
                        remove_everything_from_folder(volume_info)
                        
if __name__ == '__main__':
    connected_drives = set()

    while True:
        new_drives = [d for d in 'ABDEFGHIJKLMNOPQRSTUVXYZ' if d not in connected_drives and win32api.GetLogicalDrives() & (1 << ord(d) - 65)]
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
                print(Fore.BLUE + f"Hittade enhet: {volume_info[0]}")
                if '_VPT_PLOPP' in volume_info[0] or 'INFO_LOGS' in volume_info[0]:
                    source_folder = new_drive + ':\\'
                    items = os.listdir(source_folder)

                    if items:
                        #dest_parent_folder = r'\\gbw9061109.got.volvocars.net\PROJ2\9413-SHR-VCC127500\MEP2\Hällered'
                        dest_parent_folder = volume_info[0]
                        drive_folder = os.path.join(dest_parent_folder)
        #                move_files(drive_folder, source_folder)
                        move_files(source_folder, drive_folder)
                    else:
                        print("Inga filer att Flytta på enheten: " + new_drive)
                else: 
                    print(Fore.BLUE + f"{volume_info[0]} innehåller inte '_VPT_PLOPP eller INFO_LOGS, inget flyttning kommer att ske'.")

            except Exception as e:
                print(e)
