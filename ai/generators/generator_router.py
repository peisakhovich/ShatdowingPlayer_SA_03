from __future__ import annotations

from ai.generators.dictation_generator import DictationGenerator
from ai.generators.shadowing_generator import ShadowingGenerator


class GeneratorRouter:
    """Выбирает генератор в зависимости от сценария."""

    def __init__(self):

        self._generators = {
            "dictation": DictationGenerator,
            "shadowing": ShadowingGenerator,
        }

    def get_generator(self, scenario):

        generator_class = self._generators.get(
            scenario
        )

        if generator_class is None:

            raise ValueError(
                f"Unsupported generator scenario: {scenario}"
            )

        return generator_class()