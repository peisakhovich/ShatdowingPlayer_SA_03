from ai.models import DictationChunk, DictationSegmentation
from ai.dictation_validator import (
    DictationValidator,
    DictationValidationError,
)


TEXT = (
    "Вчера утром я проснулся раньше обычного, "
    "потому что у меня была важная встреча на работе."
)


def test_valid_result():

    result = DictationSegmentation(
        original_text=TEXT,
        chunks=[
            DictationChunk(
                text="Вчера утром я проснулся раньше обычного, ",
                ends_sentence=False,
            ),
            DictationChunk(
                text="потому что у меня была важная встреча на работе.",
                ends_sentence=True,
            ),
        ],
        total_chunks=2,
    )

    assert DictationValidator.validate(TEXT, result)


def test_changed_text():

    result = DictationSegmentation(
        original_text=TEXT,
        chunks=[
            DictationChunk(
                text="Вчера утром я проснулся раньше обычного, ",
                ends_sentence=False,
            ),
            DictationChunk(
                text="потому что у меня была очень важная встреча на работе.",
                ends_sentence=True,
            ),
        ],
        total_chunks=2,
    )

    try:
        DictationValidator.validate(TEXT, result)
        assert False, "Validation should have failed."

    except DictationValidationError:
        pass