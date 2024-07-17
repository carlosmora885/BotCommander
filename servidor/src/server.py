#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import socket
import threading
from colorama import Fore, init
from tools.ipinfo import ip_to_loc

# Inicializar colorama
init(autoreset=True)


def handle_client(conn, addr):
    # """Maneja la comunicación con un cliente conectado, con manejo de errores."""
    print(f"Conectado por {addr}")
    try:
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Recibido de {addr}: {data.decode()}")
                    conn.sendall(data)
                except ConnectionResetError:
                    print(f"Conexión reiniciada por {addr}")
                    break
                except Exception as e:
                    print(f"Error al manejar la conexión de {addr}: {e}")
                    break
    except Exception as e:
        print(f"Error en la conexión con {addr}: {e}")
    finally:
        print(f"Conexión cerrada por {addr}")


def start_server():
    # """Inicia un servidor que escucha en el host y puerto especificados por el usuario."""
    host = input("Introduce el host para el servidor (default '127.0.0.1'): ") or '127.0.0.1'
    port = int(input("Introduce el puerto para el servidor (default 65432): ") or 65432)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Servidor escuchando en {host}:{port}")

            while True:
                try:
                    conn, addr = s.accept()
                    thread = threading.Thread(target=handle_client, args=(conn, addr))
                    thread.start()
                    print(
                        f"Activo hilo para {addr}, Total de hilos: {threading.active_count() - 1}")
                except Exception as e:
                    print(f"Error al aceptar una conexión: {e}")
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")


if __name__ == "__main__":
    start_server()
