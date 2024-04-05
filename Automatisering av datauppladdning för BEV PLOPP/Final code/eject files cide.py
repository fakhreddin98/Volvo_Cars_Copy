def eject_usb_drive(source_folder):
    try:
        logging.info(f"Ejecting USB drive: {source_folder[:2]}")
        os.system(f'powershell "$driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).ParseName(\\"{source_folder[:2]}\\").InvokeVerb(\\"Eject\\")"')
        print(f"device{source_folder[:2]} disconnected")
    except Exception as e:
        logging.error(f"An error occurred while ejecting USB drive: {e}")
        print(f"An error occurred while ejecting USB drive: {e}")


        eject_usb_drive(source_folder)




def eject_usb_drive(source_folder):
    try:
        logging.info(f"Ejecting USB drive: {source_folder[:2]}")
        os.system(f'powershell "$driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).ParseName(\\"{source_folder[:2]}\\").InvokeVerb(\\"Eject\\")"')
        print(f"device{source_folder[:2]} disconnected")
    except Exception as e:
        logging.error(f"An error occurred while ejecting USB drive: {e}")
        print(f"An error occurred while ejecting USB drive: {e}")
        eject_usb_drive(source_folder)
