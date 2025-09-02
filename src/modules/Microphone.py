from modules.FileManager import FileManager
import pyaudio
import wave
import speech_recognition as sr

class MicroPhone:

    def __init__(self, logger, filemanager, audio_path, audio_file, channels, rate, chunk, record_time, language):

        self.__log = logger
        self.__file = filemanager

        self.__audioFile = self.__prepareAudioFile(audio_path, audio_file)
        
        self.__channels = channels
        self.__rate = rate
        self.__chunk = chunk
        self.__recordTime = record_time
        self.__format = pyaudio.paInt16
        self.__language = language

        
        
    
    def __prepareAudioFile(self, audio_path, audio_file):
        if not self.__file.dir_exists(audio_path):
            self.__file.create_dir(audio_path)

        audio_file_with_extension = f"{audio_file}.wav" if  not audio_file.endswith('.wav') else audio_file
        if not self.__file.file_exists(audio_file_with_extension):
            self.__file.create_file(audio_file_with_extension)

        return audio_file_with_extension

        
        
    def __setupAudioInterface(self):
        audioInterface = pyaudio.PyAudio()

        stream = audioInterface.open(
            format = self.__format,
            channels = self.__channels,
            rate = self.__rate,
            input = True,
            frames_per_buffer = self.__chunk
        )
        return audioInterface, stream


    def recordAudio(self):
        """
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 4096
        
        """
        frames = []

        try:
            audioInterface, stream = self.__setupAudioInterface()

            for _ in range(int(self.__rate / self.__chunk * self.__recordTime)):
                data = stream.read(self.__chunk, exception_on_overflow = False)
                frames.append(data)

            self.__saveAudioFile(frames, audioInterface)

            stream.stop_stream()
            stream.close()
            audioInterface.terminate()

        except Exception as e:
            self.__log.writeLog("", "ERROR", f"Error during recording: {e}")


    def __saveAudioFile(self, frames, audioInterface):
        try:

            with wave.open(self.__audioFile,"wb") as wf:
                wf.setnchannels(self.__channels)
                wf.setsampwidth(audioInterface.get_sample_size(self.__format))
                wf.setframerate(self.__rate)
                wf.writeframes(b"".join(frames))
        
        except Exception as e:
            self.__log.writeLog("", "", "")


    def recognizeAudio(self):
        if not self.__file.fileExists(self.__audioFile):
            self.__log.writeLog("./Logs/errorEvents.log", "ERROR", "Audio file not found.")
            return None


        try:
            recognizer = sr.Reconizer()
            with sr.AudioFile(self.audioFile) as source:
                audio = recognizer.record(source)

                if audio.frame_data:
                    command = recognizer.recognize_google(audio, self.__language).lower()
                    return command
                
                return None
            
        except sr.UnknownValueError:
            self.logger.writeLog("./Logs/errorEvents.log", "ERROR", "Could not understand the audio.")
            return None
        except Exception as e:
            self.logger.writeLog("./Logs/errorEvents.log", "ERROR", f"Error recognizing the audio: {e}")
            return None

            
