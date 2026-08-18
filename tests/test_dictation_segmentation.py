from dotenv import load_dotenv

from ai.dictation_segmenter import DictationSegmenter


load_dotenv()


TEXT = (
    "Вчера утром я проснулся раньше обычного, потому что у меня была "
    "важная встреча на работе. Я быстро позавтракал, проверил электронную "
    "почту и вышел из дома около восьми часов. Погода была холодная и "
    "дождливая, поэтому я решил поехать на автобусе вместо того, чтобы "
    "идти пешком. Когда я приехал в офис, обнаружил, что встреча отменена."
)


segmenter = DictationSegmenter()

result = segmenter.segment(TEXT)

print(result.model_dump_json(indent=2, ensure_ascii=False))