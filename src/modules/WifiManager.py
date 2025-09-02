import socket
import wifi
import time
import subprocess
import platform

class WifiManager:
    def __init__(self):#, ssid, password
        pass
        #self.__connect(ssid, password)

    def try_connect(self, ssid, password):
        if platform.system() == "Linux" and "WSL" in platform.release():
            print("[Simulador] Conectando ao Wi-Fi usando nmcli...")
            return True
            


        # try:
        #     command = f"nmcli dev wifi connect '{ssid}' password '{password}'"
        #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
        #     return result.returncode == 0
        # except Exception as e:
        #     print(f"Erro ao tentar conectar ao Wi-Fi: {e}")
        #     return False


    def __connect(self, ssid, password):
        try:
            # Tente se conectar à rede usando nmcli
            command = f"nmcli dev wifi connect {ssid} password {password}"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Conectado à rede Wi-Fi: {ssid}")
            else:
                print(f"Erro ao tentar conectar: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao conectar à rede: {e.stderr}")


    def getLocalIP(self):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            soc.connect(('8.8.8.8', 80))

            localIp = soc.getsockname()[0]
            
            soc.close()
            return localIp
        except Exception as e:
            print(f"Erro ao obter endereço IP local : {e}")
            return None
