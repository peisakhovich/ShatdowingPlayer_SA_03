import time
import pygame

from audio.mixer import AudioMixer


def test_mixer():

    mixer = AudioMixer()

    path = "data\\audio_cache\\19ee8b061f0b2d2ed6a09450bd2e87cceb0a7754198575cbadefa0f10a64011f.mp3"

    mixer.load(path)
    mixer.play()

    print("Playing...")

    while mixer.is_playing():
        time.sleep(0.1)

    print("Playback finished")


if __name__ == "__main__":
    pygame.init()
    test_mixer()
    pygame.quit()