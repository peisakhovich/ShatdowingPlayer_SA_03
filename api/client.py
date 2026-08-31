import os

import httpx


class ApiError(Exception):
    """Ошибка API с HTTP status code и сообщением сервера."""

    def __init__(self, message: str, status_code: int | None = None):

        super().__init__(message)

        self.message = message
        self.status_code = status_code


class ApiClient:

    def __init__(self, base_url: str):

        self.base_url = base_url.rstrip("/")

        self.api_key = os.getenv("API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "API_KEY is not configured."
            )

    # ==================================================
    # LOGIN
    # ==================================================

    def login(
        self,
        nickname: str,
        password: str
    ):

        url = f"{self.base_url}/login"

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        try:

            response = httpx.post(
                url,
                headers=headers,
                json={
                    "nickname": nickname,
                    "password": password
                },
                timeout=10.0
            )

        except httpx.RequestError as e:

            raise ApiError(
                f"API connection error: {e}"
            ) from e

        # --------------------------------------------------
        # HTTP error
        # --------------------------------------------------

        if response.status_code >= 400:

            try:
                data = response.json()

                message = data.get(
                    "error",
                    "API error"
                )

            except (ValueError, AttributeError):

                message = (
                    f"HTTP {response.status_code}"
                )

            raise ApiError(
                message,
                response.status_code
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        try:

            return response.json()

        except ValueError as e:

            raise ApiError(
                "Invalid JSON response from API",
                response.status_code
            ) from e

    # ==================================================
    # REGISTER
    # ==================================================

    def register(
        self,
        nickname: str,
        password: str,
        first_name: str = "",
        last_name: str = ""
    ):

        url = f"{self.base_url}/register"

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        try:

            response = httpx.post(
                url,
                headers=headers,
                json={
                    "nickname": nickname,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name
                },
                timeout=10.0
            )

        except httpx.RequestError as e:

            raise ApiError(
                f"API connection error: {e}"
            ) from e

        # --------------------------------------------------
        # HTTP error
        # --------------------------------------------------

        if response.status_code >= 400:

            try:
                data = response.json()

                message = data.get(
                    "error",
                    "API error"
                )

            except (ValueError, AttributeError):

                message = (
                    f"HTTP {response.status_code}"
                )

            raise ApiError(
                message,
                response.status_code
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        try:

            return response.json()

        except ValueError as e:

            raise ApiError(
                "Invalid JSON response from API",
                response.status_code
            ) from e

    # ==================================================
    # GET SETS
    # ==================================================

    def get_sets(self, user_id: int):

        url = f"{self.base_url}/sets"

        headers = {
            "X-API-Key": self.api_key
        }

        response = httpx.get(
            url,
            params={
                "user_id": user_id
            },
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

        try:

            response = httpx.post(
                url,
                params={
                    "user_id": user_id
                },
                headers=headers,
                json=data,
                timeout=10.0
            )

        except httpx.RequestError as e:

            raise ApiError(
                f"API connection error: {e}"
            ) from e

        # --------------------------------------------------
        # HTTP error
        # --------------------------------------------------

        if response.status_code >= 400:

            try:
                error_data = response.json()

                message = error_data.get(
                    "error",
                    "API error"
                )

                # Если API дополнительно передал message,
                # добавляем его для диагностики.
                detail = error_data.get("message")

                if detail:
                    message = f"{message}: {detail}"

            except (ValueError, AttributeError):

                message = (
                    f"HTTP {response.status_code}: "
                    f"{response.text}"
                )

            raise ApiError(
                message,
                response.status_code
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        try:

            return response.json()

        except ValueError as e:

            raise ApiError(
                "Invalid JSON response from API",
                response.status_code
            ) from e