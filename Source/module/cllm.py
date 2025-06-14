from ollama import Client

from Source.env.config import Config

config = Config()

class ConnectLLM:

    def __init__(self):
        self.model = config.ollama_model
        self.client = Client(host=config.ollama_address)

    def get_reaction(self, img_b64: str) -> str|None:
        system_prompt = """
        You are an expert in outputting the most relevant Emoji from a given photo.
        You are an expert in outputting from one to a maximum of five most relevant Emoji for a given photo in one continuous line.
        Do not output any useless output other than Emoji.
        Output only Emoji.
            """
        chat_base = [
            {"role": "system", "content": system_prompt},
        ]

        try:
            response = self.client.chat(
                model=self.model,
                messages= chat_base + [{
                    "role": "user",
                    "content": "Please classify the given sentence into one of the following Emoji.",
                    "images": [img_b64],
                }],
            )
        except Exception as e:
            print(e)

        if response.done:
            return response.message.content
        return None

