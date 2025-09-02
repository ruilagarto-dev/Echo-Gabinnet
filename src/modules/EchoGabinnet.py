from modules.SystemConfigurator import SystemConfigurator
from modules.DataBase import DataBase
from modules.LedController import LedController
from modules.Microphone import MicroPhone
#from modules.Button import Button
#from modules.Buzzer import Buzzer

from typing import Optional, Union, List, Dict, Any, Tuple
#import RPi.GPIO as GPIO
import difflib





class EchoGabinet:
    """
    Main controller class for the EchoGabinet system.
    
    Handles voice commands processing, LED control, and system operations.
    """
    def __init__(self, logger, file_manager) -> None:
        """
        Initialize the EchoGabinet system with all components.
        
        Args:
            logger: Logger instance for system logging
            file_manager: File manager instance for file operations
        """
        self._log = logger
        self._file_manager = file_manager
        self._system_config = SystemConfigurator(logger, file_manager)


        self._initialize_components()


    def _initialize_components(self) -> None:
        """Initialize all hardware and software components."""
        try:
            settings = self._system_config.settings
            

            self._led_controller = LedController(
                self._log,
                port = settings[0]["port"],
                baud_rate = int(settings[0]["baud_rate"]),
                timeout = float(settings[0]["timeout"]),
                rs_485_pin = int(settings[0]["rs_485_pin"]),
                data_size = int(settings[0]["data_size"]),
                led_quantity = int(settings[0]["led_quantity"]),
                box_quantity = int(settings[0]["box_quantity"])
            )
            
            # Initialize input/output devices
            # self._button = Button(self._log, settings[0]["button_pin"])
            # self._buzzer = Buzzer(self._log, settings[0]["buzzer_pin"])


            self._microphone = MicroPhone(
                self._log,
                self._file_manager,
                audio_path = settings[0]["audio_path"],
                audio_file = settings[0]["audio_file"],
                channels = int(settings[0]["channels"]),
                rate = int(settings[0]["rate"]),
                chunk = int(settings[0]["chunk"]),
                record_time = float(settings[0]["record_time"]),
                language = settings[0]["language"]
            )
            
            self._log.set_lan(settings[0]["language"])
        

            # Initialize database
            self._database = DataBase(self._log, self._file_manager)
        
        except Exception as e:
            self._log.write_log("./Logs/errorEvents.log", "ERROR", f"Component initialization failed: {str(e)}")
            raise


    def _find_best_command_match(self, command: str, all_commands: List[str]) -> Optional[Tuple[str, float]]:

        similarities = [
            (cmd, difflib.SequenceMatcher(None, command.lower(), cmd.lower()).ratio())
            for cmd in all_commands
        ]

        similarities = [(cmd, score) for cmd, score in similarities
                        if score >= self.SIMILARITY_THRESHOLD]
        similarities.sort(Key = lambda x: x[1], reverse = True)

        return similarities[0] if similarities else None
    

    def _processe_command(self, command: str) -> Optional[int]:
        try:
            all_commands = self._database.get_all_components()
            best_match = self._find_best_command_match(command, all_commands)

            if best_match:
                matched_command, score = best_match
                self._log.write_log("./Logs/command.log", "INFO", f"Command matched: '{command}' -> '{matched_command}' (score: {score:.2f})")
                return self._database.get_position(matched_command)
            
            self._log.write_log("./Logs/command.log", "WARNING", f"No match found for command: '{command}'")
            return None

        except Exception as e:
            self._log.write_log("./Logs/errorEvents.log", "ERROR", f"Command processing failed: {str(e)}")
            return None
        

    def run(self) -> None:
        """Main system loop to process voice commands and control LEDs."""
        try:
            while True:
                if self._button.is_pressed():
                    try:
                        self._buzzer.beep()
                        
                        # Record and process command
                        command = self._microphone.record_audio()
                        position = self._process_command(command)
                        
                        if position is not None:
                            self._led_controller.send_byte(position)
                        else:
                            self._buzzer.error_beep()  # Add this method to Buzzer class
                            
                    except Exception as e:
                        self._log.write_log("./Logs/errorEvents.log", "ERROR", f"Command cycle failed: {str(e)}")
                        self._buzzer.error_beep()
                else:
                    self._buzzer.turn_off()
                    
        except KeyboardInterrupt:
            self._log.write_log("./Logs/system.log", "INFO", "System shutdown by user")
        except Exception as e:
            self._log.write_log("./Logs/errorEvents.log", "CRITICAL", f"System crash: {str(e)}")
            raise
