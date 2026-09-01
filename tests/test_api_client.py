from dotenv import load_dotenv

from api.client import ApiClient
from core.config import Config
import os


load_dotenv()


def test_update_set():

    print("API_KEY loaded:", bool(os.getenv("API_KEY")))

    client = ApiClient(Config.API_BASE_URL)

    result = client.update_set(
        set_id=36,
        set_name="Client Test",
        set_description="Updated from ApiClient"
    )

    print(result)

if __name__ == "__main__":
    test_update_set()