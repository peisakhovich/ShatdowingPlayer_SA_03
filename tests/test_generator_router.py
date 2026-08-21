from ai.generators.generator_router import GeneratorRouter
from ai.generators.dictation_generator import DictationGenerator
from ai.generators.shadowing_generator import ShadowingGenerator

from dotenv import load_dotenv

load_dotenv()
router = GeneratorRouter()


dictation = router.get_generator(
    "dictation"
)

shadowing = router.get_generator(
    "shadowing"
)


print(
    "dictation:",
    type(dictation).__name__
)

print(
    "shadowing:",
    type(shadowing).__name__
)