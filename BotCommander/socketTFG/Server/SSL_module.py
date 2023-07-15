
import socket 
import ssl

#este modulo recibe un objeto socket y lo tuneliza a una conexion ssl
#seria interesante crear un archivo de configuracion donde coja los parametros 
#de la comunicacion ssl (propuesta de mejora)

def create_SSL_conection(client_socket):
    
    conection = ssl.wrap_socket(client_socket, server_side=True,
                                certfile="./certificados/server.crt", keyfile="./certificados/server.key", 
                                ssl_version=ssl.PROTOCOL_TLS_SERVER)
    return conection