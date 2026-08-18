from ai.dictation_pause import calculate_dictation_pause


chunks = [
    "Вчера утром я проснулся раньше обычного,",
    "потому что у меня была важная встреча на работе.",
    "Я быстро позавтракал, проверил электронную почту",
    "и вышел из дома около восьми часов.",
    "Погода была холодная и дождливая,",
    "поэтому я решил поехать на автобусе",
    "вместо того, чтобы идти пешком.",
    "Когда я приехал в офис, обнаружил, что встреча отменена.",
]


def test_dictation_pause():

    print()
    print("Dictation pause calculation")
    print("-" * 70)

    for index, text in enumerate(chunks, start=1):

        pause = calculate_dictation_pause(text)

        print(
            f"{index:2}. "
            f"{pause:5} ms | "
            f"{text}"
        )


if __name__ == "__main__":
    test_dictation_pause()