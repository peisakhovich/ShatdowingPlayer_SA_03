from dotenv import load_dotenv

load_dotenv()

from api.client import ApiClient
from core.config import Config


client = ApiClient(
    Config.API_BASE_URL
)


try:

    result = client.register(
        nickname="test_auth",
        password="123"
    )

    print("LOGIN SUCCESS")
    print(result)

except Exception as e:

    print("LOGIN FAILED")
    print(type(e).__name__)
    print(e)