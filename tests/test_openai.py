from dotenv import load_dotenv

from ai.openai_client import OpenAIClient


load_dotenv()


client = OpenAIClient()

response = client.ask(
    "Say hello in one short sentence."
)

print(response)