from modules.BackupManager import BackupManager
from modules.ThreadManager import ThreadManager
from modules.FileManager import FileManager
from modules.EchoGabinet import EchoGabinet
from modules.Logger import Logger
from modules.WebServer import WebServer
from modules.WifiManager import WifiManager

    
if __name__ == "__main__":
    file = FileManager()
    log = Logger(file)

    bck = BackupManager(log, file)
    echo = EchoGabinet(log, file)
    wifi = WifiManager()
    ip = wifi.getLocalIP()
    
    server = WebServer(ip, 8080 ,log, file)

    th = ThreadManager(10, 1)
    th.createNewTask(echo.run)
    th.createNewTask(bck.automateBackup(30))
    th.createNewTask(server.run)
    th.runThreads()
