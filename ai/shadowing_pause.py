def calculate_shadowing_pause(
    text: str,
    factor: float = 1.0,
    min_pause: int = 500,
    max_pause: int = 5000,
) -> int:

    text = (text or "").strip()

    if not text:
        return min_pause

    words = len(text.split())

    chars = len(text)

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

    pause = (
        300
        + words * 80
        + chars * 2
        + comma_count * 80
        + sentence_end_count * 300
        + dash_count * 150
    )

    pause = int(
        pause * factor
    )

    pause = max(
        min_pause,
        pause
    )

    pause = min(
        max_pause,
        pause
    )

    return pause