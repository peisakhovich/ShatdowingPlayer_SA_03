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

    # ==================================================
    # GET SET JSON
    # ==================================================

    def get_set(self, set_id: int):

        url = f"{self.base_url}/sets/{set_id}/items"

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

    # ==================================================
    # SAVE SET JSON
    # ==================================================

    def save_set(self, user_id: int, data: dict):

        url = f"{self.base_url}/sets"

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        response = httpx.post(
            url,
            params={
                "user_id": user_id
            },
            headers=headers,
            json=data,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()