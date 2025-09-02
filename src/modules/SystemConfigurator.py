"""
@file SystemConfigurator.py
@brief Módulo responsável pela configuração inicial do sistema EchoGabinet.

Este módulo permite ao usuário configurar conexão Wi-Fi, parâmetros seriais e idioma,
salvando tudo em um arquivo JSON para uso futuro.
"""
from modules.FileManager import FileManager
from modules.Logger import Logger
from modules.WifiManager import WifiManager
from questionary import text, password, select
from pyfiglet import Figlet
from termcolor import colored
from prompt_toolkit.styles import Style 
import sys
import os
import time


class SystemConfigurator:
    """
    @class SystemConfigurator
    @brief Classe responsável por guiar o usuário na configuração do sistema.

    Realiza a conexão Wi-Fi, configurações seriais e salva os parâmetros em arquivo.
    """
    def __init__(self, logger:Logger, filemanager: FileManager):
        """
        @brief Construtor da classe SystemConfigurator.
        @param logger Instância do logger para registrar eventos.
        @param filemanager Instância para operações com arquivos.
        """
        self._log = logger
        self._file = filemanager
        self._wifi = WifiManager()

        self.__settings_file = "Config/settings.json"
        self.settings = None

        try:
            self.run()
        except KeyboardInterrupt:
            print("\n" + colored("🚫 Operação cancelada pelo usuário.", 'red'))
            sys.exit(0)
        except ImportError as e:
            print("\n" + colored(f"⚠️ Erro de importação: {e}", 'red'))
            sys.exit(1)
        except Exception as e:
            # Usa fallback caso não haja método `error`
            if hasattr(self._log, 'error'):
                self._log.error(f"Erro ao configurar o sistema: {e}")
            else:
                self._log.log("ERROR", f"Erro ao configurar o sistema: {e}")

            print(colored("❌ Erro inesperado durante a configuração.", "red"))
            sys.exit(1)

    def run(self) -> None:
        """
        @brief Executa o fluxo principal de configuração.
        """
        if self._file.file_exists(self.__settings_file):
            self.settings = self._file.read_file(self.__settings_file)
        else:
            self.configure_wifi()
            self.configure_system()
            self.save_settings()
    
    def configure_wifi(self) -> None:
        """
        @brief Realiza o processo de conexão Wi-Fi interativa.
        """
        while True:
            self.display_header()
            print(colored("📡 Vamos configurar a conexão Wi-Fi.\n", "cyan"))
            wifi_config = self.get_wifi_config()

            print(colored("🔄 Tentando conectar ao Wi-Fi...", "yellow"))
            time.sleep(1)

            if self._wifi.try_connect(wifi_config["ssid"], wifi_config["password"]):
                print(colored("✅ Conectado ao Wi-Fi com sucesso!\n", 'green', attrs=['bold']))
                self.settings = wifi_config
                break
            else:
                print(colored("❌ Falha ao conectar ao Wi-Fi. Tente novamente.\n", 'red'))
                time.sleep(1)

    def configure_system(self) -> None:
        """
        @brief Solicita as demais configurações do sistema (porta, baudrate, idioma).
        """
        print(colored("🛠️  Agora vamos configurar os parâmetros do dispositivo.\n", "cyan"))
        rest_config = self.get_other_config()
        self.settings.update(rest_config)
        self.display_summary(self.settings)

    def save_settings(self) -> None:
        """
        @brief Salva as configurações em um arquivo JSON.
        """
        self._file.create_dir("Config")
        self._file.create_file(self.__settings_file)
        self._file.write_file(self.__settings_file, self.settings)
        print(colored("\n✅ Configuração salva com sucesso!", "green", attrs=["bold"]))

    def display_header(self):
        """
        @brief Exibe o cabeçalho ASCII art na tela.
        """
        os.system('clear')
        
        try:
            width = os.get_terminal_size().columns
        except OSError:
            width = 80  # fallback padrão se não for possível obter
        
        custom_fig = Figlet(font="dos_rebel", width=width)
        ascii_art = custom_fig.renderText('EchoGabinet')
            

        # Centralizar cada linha do logo
        centered_art = '\n'.join(line.center(width) for line in ascii_art.splitlines())

        print(colored(centered_art, 'cyan'))
        print(colored("=" * width, 'blue'))
        print(colored("🛠️  Bem-vindo à Configuração do EchoGabinet".center(width), 'yellow'))
        print(colored("=" * width, 'blue'))
        print()

    def get_style(self):
        """
        @brief Define o estilo visual dos prompts do Questionary.
        @return Estilo personalizado para entrada de dados.
        """
        return Style([
            ('question', 'fg:#00bfa6 bold'),   # Verde água
            ('selected', 'fg:#5F819D'),
        ])

    def get_wifi_config(self):
        """
        @brief Solicita os dados de conexão Wi-Fi ao usuário.
        @return Dicionário contendo SSID e senha.
        """
        style = self.get_style()
        ssid = text("📶 Nome da Rede Wi-Fi (SSID):", style=style).ask()
        wifi_pass = password("🔑 Senha da Rede:", style=style).ask()
        return {'ssid': ssid, 'password': wifi_pass}

    def get_other_config(self):
        """
        Solicita os parâmetros adicionais do sistema.
        """
        style = self.get_style()
        config = {}

        config["port"] = text("🖥️ Porta RS485 (ex: /dev/ttyUSB0):", style=style).ask()
        config["baud_rate"] = text("⚙️ Baud Rate:", style=style, validate=lambda t: t.isdigit() or "Deve ser um número.").ask()
        config["timeout"] = text("⏱️ Timeout (segundos):", style=style, validate=lambda t: t.isdigit() or "Deve ser um número.").ask()
        config["rs_485_pin"] = text("🔌 Pino RS485:", style=style).ask()
        config["data_size"] = text("📦 Tamanho dos Dados:", style=style).ask()
        config["led_quantity"] = text("💡 Quantidade de LEDs:", style=style).ask()
        config["box_quantity"] = text("📦 Quantidade de Caixas:", style=style).ask()
        config["audio_path"] = text("🎙️ Caminho do Áudio:", style=style).ask()
        config["audio_file"] = text("📁 Nome do Arquivo de Áudio:", style=style).ask()
        config["channels"] = text("🎚️ Canais de Áudio:", style=style).ask()
        config["rate"] = text("📈 Taxa de Amostragem:", style=style).ask()
        config["chunk"] = text("📦 Tamanho do Chunk:", style=style).ask()
        config["record_time"] = text("⏺️ Tempo de Gravação (segundos):", style=style).ask()
        config["language"] = select("🌍 Escolha o idioma:", choices=["en-US", "pt-PT", "es-ES", "fr-FR", "de-DE"], style=style).ask()
        config["button_pin"] = text("🔘 Pino do Botão:", style=style).ask()
        config["buzzer_pin"] = text("📢 Pino do Buzzer:", style=style).ask()

        return config

    def display_summary(self, answers):
        """
        @brief Exibe um resumo das configurações inseridas.
        @param answers Dicionário com os parâmetros de configuração.
        """
        print("\n" + colored("📋 Resumo da Configuração:", 'magenta', attrs=['bold']))
        print(colored("-" * 40, 'blue'))
        for key, value in answers.items():
            label = key.capitalize().replace('_', ' ')
            print(colored(f"🔹 {label:<12}:", 'yellow') + f" {value}")
        print(colored("-" * 40, 'blue'))
