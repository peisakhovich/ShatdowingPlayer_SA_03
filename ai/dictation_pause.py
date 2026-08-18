def calculate_dictation_pause(
    text: str,
    factor: float = 2.0,
    min_pause: int = 300,
    max_pause: int = 10000,
) -> int:

    text = (text or "").strip()

    # Empty text
    if not text:
        return min_pause

    # Number of words
    words = len(text.split())

    # Number of characters
    chars = len(text)

    # Punctuation
    comma_count = sum(
        text.count(ch)
        for ch in ",;:"
    )

    sentence_end_count = sum(
        text.count(ch)
        for ch in ".?!"
    )

    dash_count = (
        text.count("—")
        + text.count("-")
    )

    # Base pause — same algorithm as SQL fn_calculate_pause()
    base_pause = (
        300
        + words * 200
        + chars * 5
        + comma_count * 150
        + sentence_end_count * 500
        + dash_count * 300
    )

    # Dictation requires more time than shadowing
    pause = int(base_pause * factor)

    # Limits
    pause = max(min_pause, pause)
    pause = min(max_pause, pause)

    return pause