"""
session.py

Рабочая сессия приложения SA_03.

Хранит:
    - данные набора (set)
    - элементы набора (items)
    - кэшируемое состояние (state)

Не хранит:
    - скорость воспроизведения
    - параметры Player
    - кэш аудио

Автор: SA_03
"""

from __future__ import annotations

import json
from pathlib import Path


class Session:
    """Рабочая сессия приложения."""

    # ==========================================================
    # Construction
    # ==========================================================

    def __init__(self):

        self._filename: Path | None = None

        # ---------- JSON sections ----------
        self._set: dict = {}
        self._items: list = []
        self._state: dict = {}

    # ==========================================================
    # Factory
    # ==========================================================

    @classmethod
    def load(cls, filename: str | Path) -> "Session":
        """
        Загрузить Session из JSON.
        """

        session = cls()

        session._filename = Path(filename)

        with open(session._filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        session._set = data.get("set", {})
        session._items = data.get("items", [])
        session._state = data.get("state", {})

        return session

    # ==========================================================
    # Save
    # ==========================================================

    def save(self, filename: str | Path | None = None):
        """
        Сохранить Session в JSON.
        """

        if filename is None:
            filename = self._filename

        data = {
            "set": self._set,
            "items": self._items,
            "state": self._state,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def id(self):
        return self._set.get("set_id")

    @property
    def name(self):
        return self._set.get("set_name", "")

    @property
    def description(self):
        return self._set.get("set_description", "")

    @property
    def items_count(self):
        return len(self._items)

    @property
    def current_index(self):
        return self._state.get("current_index", 0)

    @current_index.setter
    def current_index(self, value):
        self._state["current_index"] = value

    # ==========================================================
    # Navigation
    # ==========================================================

    def current(self):

        if self.is_empty():
            return None

        return self._items[self.current_index]

    def first(self):

        self.current_index = 0
        return self.current()

    def last(self):

        if not self.is_empty():
            self.current_index = len(self._items) - 1

        return self.current()

    def next(self):

        if self.current_index < len(self._items) - 1:
            self.current_index += 1

        return self.current()

    def prev(self):

        if self.current_index > 0:
            self.current_index -= 1

        return self.current()

    def goto(self, index: int):

        if 0 <= index < len(self._items):
            self.current_index = index

        return self.current()

    # ==========================================================
    # Helpers
    # ==========================================================

    def count(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def is_first(self):
        return self.current_index == 0

    def is_last(self):
        return self.current_index >= len(self._items) - 1

    # ==========================================================
    # Debug
    # ==========================================================

    def __len__(self):
        return len(self._items)

    def __repr__(self):

        return (
            f"Session("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"items={len(self)}, "
            f"index={self.current_index})"
        )