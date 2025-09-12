from modules.DataBase import DataBase
from datetime import datetime
import zipfile
import shutil
import os


class BackupManager(DataBase):

    def __init__(self, logger, fileManager) -> None:
        super().__init__(logger, fileManager)
        self._log = logger
        self._file = fileManager

        self.__backupDir = "/home/ruimc/Projetos/PythonProjects/echoGabinnet/BackUps"
        self.__directoryDb = "/home/ruimc/Projetos/PythonProjects/echoGabinnet/Data/database.db"
        


    
    # Executa o backup da base de dados. Pode incluir a criação de um dump ou a cópia de ficheiros.
    def createBackup(self): 
        self.__backupDir = os.path.join(self.__backupDir, f"database_{datetime.now().month}_{datetime.now().year}.db")
        self._file.copyFile(self.__directoryDb, self.__backupDir)
        self.__compressBackup(self.__backupDir)


    def __compressBackup(self, backupFile):
        # Criando o arquivo ZIP
        zipFile = backupFile.replace(".db", ".zip")
        
        
        # Comprimindo o arquivo de backup em formato ZIP
        try:
            with zipfile.ZipFile(zipFile, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(backupFile, arcname=backupFile)
                
            self._file.deleteFile(self.__backupDir)

        except Exception as e:
            print(f"Erro ao tentar criar o arquivo ZIP: {e}")
            

    # Envia o backup para servidores remotos (FTP, S3, Google Drive)
    def transferBackupRemote(self):
        pass

    
    # Remove backups antigos com base num período de retenção.
    def deleteOldBackups(self, retentionDays):
        pass


    # Agenda backups automáticos.
    def automateBackup(self, interval):
        pass
