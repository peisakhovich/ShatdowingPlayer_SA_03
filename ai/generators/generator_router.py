"""
Sound Language Studio
---------------------

Module:
    ai.generators.generator_router

Purpose:
    Selects and creates the appropriate training-plan generator
    according to the selected learning scenario.

ru:
    Выбирает и создаёт соответствующий генератор учебного плана
    в зависимости от выбранного сценария обучения.
"""
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