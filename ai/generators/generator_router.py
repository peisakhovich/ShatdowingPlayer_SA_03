from __future__ import annotations

from ai.generators.dictation_generator import DictationGenerator


class GeneratorRouter:
    """Выбирает генератор в зависимости от сценария."""

    def __init__(self):

        self._generators = {
            "dictation": DictationGenerator(),
        }

    def get_generator(self, scenario):

        generator = self._generators.get(
            scenario
        )

        if generator is None:

            raise ValueError(
                f"Unsupported generator scenario: {scenario}"
            )

        return generator