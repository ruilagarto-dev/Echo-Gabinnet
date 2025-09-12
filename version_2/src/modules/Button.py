#import RPi.GPIO as GPIO
from modules.Logger import Logger

class Button:
    """
    @class Button
    @brief Represents a physical button connected to a GPIO pin.
    
    Provides methods for button state checking and resource cleanup.
    """
    def __init__(self, logger: Logger, pin: int) -> None:
        self.__log = logger
        self.__pin = pin
        #self.__configuratePin()


    """
    def __configuratePin(self) -> None:
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            self.__log.writeLog("Logs/buttonControl.log", "INFO", f"GPIO pin {self.__pin} configured successfully.")
        except Exception as e:
             self.__log.writeLog("Logs/buttonControl.log",  "ERROR", f"Failed to configure GPIO pin {self.__pin}: {e}")
    """

    def isPressed(self) -> bool:
        """
        @brief Checks if the button is currently pressed.
        @return True if pressed, False otherwise.
        """
        try:
            #return GPIO.input(self.__pin) == GPIO.LOW
            return True
        except Exception as e:
            self.__log.write_log("Logs/buttonControl.log", "ERROR", f"Failed to read GPIO pin {self.__pin}: {e}")
            return False
        

    def cleanup(self) -> None:
        """
        @brief Releases the GPIO resources for the button.
        """
        try:
            #GPIO.cleanup(self.__pin)
            self.__log.write_log("Logs/buttonControl.log", "INFO", f"GPIO pin {self.__pin} cleaned up successfully.")
        except Exception as e:
            self.__log.write_log("Logs/buttonControl.log", "ERROR", f"Failed to clean up GPIO pin {self.__pin}: {e}")
    
