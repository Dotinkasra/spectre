import configparser
import os

class Config():
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(path, 'UTF-8')

    @property
    def token(self) -> str:
        return str(self.config['TOKEN']['TOKEN'])

    @property
    def guilds(self) -> list[int]:
        return list(map(int, self.config['GUILDS'].values()))

    @property
    def admin(self) -> list[int]:
        return list(map(int, self.config['ADMIN'].values()))

    @property
    def notification(self) -> list[int]:
        return list(map(int, self.config['NOTIFICATION'].values()))

    @property
    def speaker(self) -> dict:
        return dict(self.config['SPEAKER'])

    @property
    def notice_channel(self, key: str) -> int:
        return str(self.config['NOTICE_CHANNEL'][key])

    @property
    def ignore_voice_channel_log(self) -> list[int]:
        return list(map(int, eval(self.config['CHANNEL']["IGNORE_VOICE_CHANNEL_LOG"])))
    
    @property
    def llm_target_channel(self) -> list[int]:
        return list(map(int, eval(self.config['CHANNEL']["LLM_TARGET_CHANNEL"])))
    
    @property
    def ollama_address(self) -> str:
        return str(self.config['OLLAMA']["ADDRESS"])
    
    @property
    def ollama_model(self) -> str:
        return str(self.config['OLLAMA']["MODEL"])