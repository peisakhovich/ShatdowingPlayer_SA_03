from dotenv import load_dotenv

from ai.shadowing_segmenter import ShadowingSegmenter


load_dotenv()


TEXT = (

    "Вчера утром я проснулся раньше обычного, потому что у меня была "

    "важная встреча на работе. Я быстро позавтракал, проверил электронную "

    "почту и вышел из дома около восьми часов. Погода была холодная и "

    "дождливая, поэтому я решил поехать на автобусе вместо того, чтобы "

    "идти пешком. Когда я приехал в офис, обнаружил, что встреча отменена."

)


segmenter = ShadowingSegmenter()

result = segmenter.segment(
    text=TEXT,
    source_language="Russian",
    target_language="Polish",
)

print(
    result.model_dump_json(
        indent=2,
        ensure_ascii=False
    )
)