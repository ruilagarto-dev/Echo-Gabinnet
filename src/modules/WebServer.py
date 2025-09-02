from flask import Flask, render_template, request, redirect, url_for
from modules.FileManager import FileManager
from modules.DataBase import DataBase

class WebServer:
    def __init__(self, host, port, logger, filemanager):
        self.app = Flask(__name__)
        self.__host = host
        self.__port = port

        self.__log = logger

        self.__db = DataBase(logger, filemanager)

        self.app.route('/')(self.index)
        self.app.route('/add', methods=['POST'])(self.addCommand)
        self.app.route('/delete/<int:index>', methods=['POST'])(self.removeCommand)
        self.app.route('/search', methods=['GET'])(self.searchCommand)


    def index(self):
        componentes = self.__db._getAllCommand()
        return render_template('index.html', components=componentes) 


    def addCommand(self):
        componentName = request.form['name']
        value = request.form['position']
        description = request.form['description']
        self.__db._insertCommand(componentName, value, description)
        self.__log.writeLog("Logs/webInterface.log","INFO", f"Command added: {componentName} with position {value}. Description: {description}")
        return redirect(url_for('index'))


    def removeCommand(self, index):
        componentName = request.form['name']


        self.__db._deleteCommand(componentName)
        self.__log.writeLog("Logs/webInterface.log", "INFO", f"Command removed: {componentName}")
        return redirect(url_for('index'))


    def searchCommand(self):
        command = request.args.get('search')
        
        self.__log.writeLog("Logs/webInterface.log", "INFO", f"Search command executed: '{command}'")

        components = self.__db._searchCommand(command)  # Faz a pesquisa no banco de dados
        return render_template('index.html', components=components) 
    
    
    def run(self):
        self.app.run(host=self.__host, port=self.__port, debug=True)
