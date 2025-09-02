import os
from enum import Enum
from datetime import datetime
from colorama import init, Fore
from typing import Union


init(autoreset=True)


class LogLevel(Enum):
    """@brief Enumeration for log severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """
    @class Logger
    @brief Provides structured logging to categorized log files.

    Responsible for writing timestamped messages to log files related to different system components or concerns.
    """
    
    def __init__(self, file_manager):
        """
        @brief Initializes the Logger with a FileManager instance and prepares log files.
        @param file_manager FileManager object for file operations.
        """
        self._file_manager  = file_manager
        self._log_directory = "Logs"
        self._log_files = [
            "systemActivity.log",
            "errorEvents.log",
            "audioTranscription.log",
            "RS485communication.log",
            "databaseOperations.log",
            "wifiStatus.log",
            "webInterface.log",
            "buzzerControl.log",
            "buttonControl.log"
        ]
        self._lan = None
        self._initialize_logs()

    def set_lan(self, lan):
        """
        @brief Sets the LAN instance for the Logger.
        @param lan LAN instance to be used for logging.
        """
        self._lan = lan

    def translate(self, key: str) -> str:
        pass

    def _initialize_logs(self) -> None:
        """
        @brief Creates the Logs directory and initializes all required log files.
        """
        self._file_manager.create_dir(self._log_directory)
        for filename in self._log_files:
            filepath = os.path.join(self._log_directory, filename)
            self._file_manager.create_file(filepath)

        

    def _get_current_timestamp(self) -> str:
        """
        @brief Returns the current date and time as a formatted string.
        @return String in the format DD-MM-YYYY HH:MM:SS
        """
        now = datetime.now()
        return now.strftime("%d-%m-%Y %H:%M:%S")


    def _format_log_entry(self, level: LogLevel, message: str) -> str:  
        """
        @brief Formats a log entry with level and timestamp.
        @param level LogLevel enum value.
        @param message Message content.
        @return Formatted string for logging.
        """   
        return f"[{level.value}] - {self._get_current_timestamp()}] {message}\n"
    



    def write_log(self, file_path: str, level:Union[LogLevel, str], message: str) -> None:
        """
        @brief Writes a formatted log message to a file.
        @param file_path Relative path to the log file.
        @param level LogLevel enum or equivalent string ("INFO", "ERROR", etc).
        @param message Message string to log.
        @throws ValueError If an invalid log level is provided.
        """

        if isinstance(level, str):
            try:
                level = LogLevel[level.upper()]
            except KeyError:
                raise ValueError(f"Invalid log level: {level}. Use one of {', '.join([e.value for e in LogLevel])}.")
            
        formatted_message = self._format_log_entry(level, message)
        self._file_manager.write_file(file_path, formatted_message)
    
    
