from modules.Logger import Logger

#import RPi.GPIO as GPIO

import time


class Buzzer:
    """
    @class Buzzer
    @brief Represents a GPIO-controlled buzzer for signaling events.

    Provides methods to activate, deactivate and beep the buzzer.
    """

    def __init__(self, pin: int, logger: Logger) -> None:
        self._pin = pin
        self._log = logger
        #self.__configuratePin()
        self._off()


    # ------- Private Methods -------
    def __configuratePin(self) -> None:
        """
        @brief Configures the GPIO pin for output use with the buzzer.
        """

        try:
            #GPIO.setwarnings(False)
            #GPIO.setmode(GPIO.BCM)
            #GPIO.setup(self.__pin, GPIO.OUT)
            self._log.write_log("Logs/buzzerControl.log", "INFO", "Pin configured successfully.")
        except Exception as e:
            self._log.write_log("Logs/buzzerControl.log", "ERROR", f"Error configuring pin: {str(e)}")


    def _on(self) -> None:
        """
        @brief Turns the buzzer on.
        """
        try:
            #GPIO.output(self.__pin, GPIO.HIGH)
            self._log.write_log("Logs/buzzerControl.log", "INFO", "Buzzer turned on.")
        except Exception as e:
            self._log.write_log("Logs/buzzerControl.log", "ERROR", f"Error turning buzzer on: {str(e)}")


    def _off(self) -> None:
        """
        @brief Turns the buzzer off.
        """
        try:
            #GPIO.output(self.__pin, GPIO.LOW)
            self._log.write_log("Logs/buzzerControl.log", "INFO", "Buzzer turned off.")
        except Exception as e:
            self._log.write_log("Logs/buzzerControl.log", "ERROR", f"Error turning buzzer off: {str(e)}")
        

    # ------- Public Methods -------
    def beep(self, duration:float = 0.5) -> None:
        """
        @brief Activates the buzzer for a short period.
        @param duration Duration of the beep in seconds (default: 0.5s).
        """
        self._on()
        time.sleep(duration)
        self._off()

    """
    def cleanup(self) -> None:
        try:
            GPIO.cleanup(self.__pin)
            self.__log.writeLog("Logs/buzzerControl.log", "INFO", f"GPIO pin {self.__pin} cleaned up successfully.")
        except Exception as e:
            self.__log.writeLog("Logs/buzzerControl.log", "ERROR", f"Failed to clean up GPIO pin {self.__pin}: {e}")
    """    
