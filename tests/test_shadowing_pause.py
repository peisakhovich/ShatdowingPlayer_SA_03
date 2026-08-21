from ai.shadowing_pause import calculate_shadowing_pause


TESTS = [
    "Hello.",
    "Hello, how are you?",
    "Yesterday I went to work.",
    "Yesterday morning I went to work by bus.",
    "Yesterday morning I went to work by bus because the weather was very cold.",
    "When I arrived at the office, I discovered that the meeting had been cancelled.",
]


for text in TESTS:

    pause = calculate_shadowing_pause(
        text=text,
        factor=1.0,
    )

    print(
        f"{pause:4} ms | {text}"
    )