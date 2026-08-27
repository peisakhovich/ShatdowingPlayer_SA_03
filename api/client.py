import os

import httpx


class ApiClient:

    def __init__(self, base_url: str):

        self.base_url = base_url.rstrip("/")

        self.api_key = os.getenv("API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "API_KEY is not configured."
            )

    def get_sets(self):

        url = f"{self.base_url}/sets"

        headers = {
            "X-API-Key": self.api_key
        }

        response = httpx.get(
            url,
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()