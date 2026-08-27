from dotenv import load_dotenv

from api.client import ApiClient
from core.config import Config
import os

load_dotenv()


def test_get_sets():

    print("API_KEY loaded:", bool(os.getenv("API_KEY")))
    client = ApiClient(Config.API_BASE_URL)

    sets = client.get_sets()

    assert isinstance(sets, list)
    assert len(sets) > 0

    print()
    print(f"Received {len(sets)} sets")

    for item in sets[:5]:
        print(item)