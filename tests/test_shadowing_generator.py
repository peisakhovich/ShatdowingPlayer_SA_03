from dotenv import load_dotenv

from ai.generators.shadowing_generator import ShadowingGenerator


load_dotenv()


TEXT = (

    "Вчера утром я проснулся раньше обычного, потому что у меня была "

    "важная встреча на работе. Я быстро позавтракал, проверил электронную "

    "почту и вышел из дома около восьми часов. Погода была холодная и "

    "дождливая, поэтому я решил поехать на автобусе вместо того, чтобы "

    "идти пешком. Когда я приехал в офис, обнаружил, что встреча отменена."

)


generator = ShadowingGenerator()

plan = generator.generate(

    text=TEXT,

    source_language="Russian",
    target_language="Polish",

    phrase_code="ru",
    phrase_locale="ru-RU",
    phrase_voice="ru-RU-SvetlanaNeural",
    phrase_voice_gender="Female",

    translate_code="pl",
    translate_locale="pl-PL",
    translate_voice="pl-PL-MarekNeural",
    translate_voice_gender="Male",

    speed=1.0,
    repeat_count=3,

    pause_factor=1.0,

    set_name="Shadowing Test",
    set_description="Test shadowing session",
)


print()
print("==============================")
print("SHADOWING PLAN")
print("==============================")

print(
    plan["set"]
)

print("------------------------------")

for item in plan["items"]:

    print(
        item["item_order"],
        item["phrase_text"]
    )

    print(
        "   →",
        item["translate_text"]
    )

    print(
        "   pause:",
        item["pause_ms"],
        "ms"
    )

    print(
        "   repeat:",
        item["repeat_count"]
    )

print("==============================")
print()