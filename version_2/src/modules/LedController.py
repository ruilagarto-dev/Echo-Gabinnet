from typing import List, Dict, Any, Optional
#import RPi.GPIO as GPIO
import serial
import time


class LedController:
    """
    @class LedController
    @brief Controls LEDs through RS-485 communication using a serial interface.
    """

    def __init__(self, logger, port: str, baud_rate: int, timeout: float, rs_485_pin: int, data_size: int, led_quantity: int, box_quantity: int) -> None:

        """
        @brief Initializes the LED controller with serial communication and configuration data.
        @param logger Logger instance for writing logs.
        @param port Serial port to communicate with.
        @param baud_rate Baud rate for the serial communication.
        @param timeout Timeout for serial reading.
        @param pin GPIO pin used for controlling transmission.
        @param data_size Size of the data array used to turn off LEDs.
        @param leds_per_box Number of LEDs per box.
        @param box_count Number of boxes.
        """

        self._log = logger
        self._log.write_log("Logs/RS485communication.log", "INFO", "Initializing LedController")
        try:
            """
            self.__serialConnection = serial.Serial(
                port = port,
                baudrate = baud_rate, 
                timeout = timeout
            )
            """
            self._log.write_log("Logs/RS485communication.log", "INFO", "Serial connection established.")
        except Exception as e:
            self._log.write_log("Logs/RS485communication.log", "ERROR", f"Failed to establish serial connection: {e}")
            raise ConnectionError(f"Serial connection failed: {e}")
        
        self._pin = rs_485_pin
        self._data_size = data_size
        self._leds_per_box = led_quantity
        self._box_count = box_quantity

        self._clear_data = [0x00] * self._data_size
        self._byte_buffer: List[bytes] = []

        self._boxes = self._initialize_boxes()
        self._log.write_log("Logs/RS485communication.log", "INFO", "Boxes initialized.")


        #self._configure_gpio_pin()
        #self._turn_off_leds()
        
        

    """"
    def _configure_gpio_pin(self) -> None:
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self._pin, GPIO.OUT)
            self.__log.write_log("Logs/RS485communication.log", "INFO", f"Pin {self.__pin} configured as OUTPUT.")

        except Exception as e:
            self.__log.write_log("Logs/RS485communication.log", "ERROR", f"Failed to configure pin {self.__pin}: {e}")
    """

    def _initialize_boxes(self) -> List[Dict[str, Any]]:
        """
        @brief Initializes data structures representing each LED box.
        @return List of box dictionaries containing ID, position range and LED patterns.
        """
        boxes = []
        for i in range(self._box_count):
            box_id = i + 1
            start_pos = (i * self._leds_per_box) + 1
            end_pos = start_pos + self._leds_per_box
            boxes.append({
                "Id":box_id,
                "Position": list(range(start_pos, end_pos)),
                "all_leds": self._generate_led_patterns()
            })
        return boxes


    def _generate_led_patterns(self) -> List[List[int]]:
        """
        @brief Generates bit-shifted RGB LED patterns.
        @return List of [R, G, B] arrays for each bit position.
        """
        return [
            [0b00000001 << i, 0b00000000, 0b00000000] for i in range(8)
        ] + [
            [0b00000000, 0b00000001 << i, 0b00000000] for i in range(8)
        ] + [
            [0b00000000, 0b00000000, 0b00000001 << i] for i in range(8)
        ]
    
    
    def _set_transmitter(self, state: bool) -> None:
        """
        @brief Sets the transmitter state (RS-485 direction).
        @param state True for HIGH, False for LOW.
        """
        try:
            #GPIO.output(self.__pin, GPIO.HIGH if state else GPIO.LOW)
            self._log.write_log("Logs/RS485communication.log", "INFO", f"Transmitter set to {'HIGH' if state else 'LOW'}.")
        except ImportError:
            self._log.write_log("Logs/RS485communication.log", "ERROR", "GPIO not available! Make sure you are running on a Raspberry Pi")
            
            

    def cleanArray(self):
        self.__byteList.clear()


    def _turn_off_leds(self) -> None:
        self._log.write_log("Logs/RS485communication.log", "INFO", "Turning off LEDs.")
        self._set_transmitter(True)
        self.__serialConnection.write(self.__clearLeds)
        time.sleep(0.2)
        self._set_transmitter(False)
        

    def _sendByte(self, position):
        byte = self.__positionToBytes(position)
        
        self._turn_off_leds()
        self._log.write_log("Logs/RS485communication.log", "INFO", f"Sending byte: {byte}")
        self._set_transmitter(True)
        self.__serialConnection.write(byte)
        time.sleep(1)
        self._set_transmitter(False)
        self._log.write_log("Logs/RS485communication.log", "INFO", "Byte sent successfully.")
        


    def __positionToBytes(self, value):
        self._log.write_log("Logs/RS485communication.log", "INFO", f"Converting value: {value}")
        for box in self.__boxes:
            if value in box["Position"]:
                if box["Id"] > 1:
                    value -= (box["Id"]) * self.__ledQuantity
                arrayBytes = bytes([box["Id"]] + box["all_leds"][value - 1])
                self._log.write_log("Logs/RS485communication.log", "INFO", f"Conversion successful. Box ID: {box['Id']}")
                return arrayBytes

        self._log.write_log("Logs/RS485communication.log", "ERROR", "Conversion failed: value not found.")
        return None

