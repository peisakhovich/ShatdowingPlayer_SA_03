"""
Player lifecycle and playback FSM
Player — центральный объект управления воспроизведением.
На данном этапе отвечает только за:
- хранение Session;
- состояние проигрывателя;
- навигацию по Session;
- публичный API.
"""
import asyncio
from pathlib import Path

from audio.cache import AudioCache
from audio.provider import AudioProvider
from audio.mixer import AudioMixer
from audio.tts import TTS
from audio.async_runner import AsyncRunner

class PlayerState:

    #Состояния Player
    IDLE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3

class PlaybackPhase:

    #Этап воспроизведения одной фразы.
    PREPARE_ITEM = 0
    PREPARE_TEXT_AUDIO = 1
    PLAY_TEXT = 2
    WAIT_TEXT_END = 3
    PAUSE = 4
    PREPARE_TRANSLATION_AUDIO = 5
    PLAY_TRANSLATION = 6
    WAIT_TRANSLATION_END = 7
    PAUSE_BETWEEN_SENTENCES = 8
    FINISH_ITEM = 9

class Player:

    def __init__(self, session):

        self._session = session
        self._state = PlayerState.IDLE
        self._phase = PlaybackPhase.PREPARE_ITEM

        # Параметры воспроизведения
        self._voice_speed = 1.0
        self._pause_before_translation = 2000
        self._pause_between_sentences = 2000  

        self._timer_ms = 0
        self._current_item = None      

        self._audio_provider = AudioProvider(cache=AudioCache(), tts=TTS())
        self._audio_mixer = AudioMixer()
        self._async_runner = AsyncRunner()
        self._audio_task = None

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def session(self):
        return self._session

    @property
    def state(self):
        return self._state

    @property
    def voice_speed(self):
        return self._voice_speed

    @voice_speed.setter
    def voice_speed(self, value):
        self._voice_speed = value

    @property
    def pause_before_translation(self):
        return self._pause_before_translation

    @pause_before_translation.setter
    def pause_before_translation(self, value):
        self._pause_before_translation = value

    @property
    def pause_between_sentences(self):
        return self._pause_between_sentences

    @pause_between_sentences.setter
    def pause_between_sentences(self, value):
        self._pause_between_sentences = value


    # ---------------------------------------------------------    
    # Async audio controls preparation
    # ---------------------------------------------------------
    def _cancel_audio_task(self):

        if self._audio_task is not None:

            if not self._audio_task.done():
                self._audio_task.cancel()

            self._audio_task = None

    async def _prepare_text_audio(self):
        path = await self._audio_provider.get_audio(
            text=self._current_item["phrase_text"],
            voice=self._current_item["phrase_voice"],
            speed=self.voice_speed,
        )

        self._audio_mixer.load(path)

    async def _prepare_translation_audio(self):
        path = await self._audio_provider.get_audio(
            text=self._current_item["translate_text"],
            voice=self._current_item["translate_voice"],
            speed=self.voice_speed,
        )

        self._audio_mixer.load(path)


    async def _prepare_audio(self, text: str, voice: str) -> Path:

        return await self._audio_provider.get_audio(
            text=text,
            voice=voice,
            speed=self.voice_speed,
        )

    # tmp test method
    async def test_audio(self):

        item = self.session.current_item

        path = await self._prepare_audio(
            text=item["phrase_text"],
            voice=item["phrase_voice"],
        )
        self._audio_mixer.load(path)
        self._audio_mixer.play()
        while self._audio_mixer.is_playing():
            await asyncio.sleep(0.1)

        path = await self._prepare_audio(
            text=item["translate_text"],
            voice=item["translate_voice"],
        )
        self._audio_mixer.load(path)
        self._audio_mixer.play()



        print(f"Player audio: {path}")

    # ---------------------------------------------------------
    # Playback control
    # ---------------------------------------------------------

    def play(self):

        #print("PLAYER PLAY:", self._state)

        if self._session is None:
            return

        if self._state == PlayerState.PAUSED:

            self._audio_mixer.resume()    
            self._state = PlayerState.PLAYING
            return


        self._state = PlayerState.PLAYING
        self._phase = PlaybackPhase.PREPARE_ITEM

    def pause(self):

        #print("PLAYER PAUSE:", self._state)

        if self._state == PlayerState.PLAYING:
            self._audio_mixer.pause()
            self._state = PlayerState.PAUSED

    def stop(self):

        #print("PLAYER STOP:", self._state)
        self._audio_mixer.stop()
        self._state = PlayerState.STOPPED

    # --------------------------------------------------
    # Скорость воспроизведения, пауза между предложениями и перед переводом
    # --------------------------------------------------

    def set_speed(self, value: float):
        self.voice_speed = value

    def set_pause_before_translation(self, value: int):
        self.pause_before_translation = value

    def set_pause_between_sentences(self, value: int):
        self.pause_between_sentences = value



    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def _navigate(self, action):
        self._cancel_audio_task()
        self._audio_mixer.stop()
        action()
        self._phase = PlaybackPhase.PREPARE_ITEM

    def next(self):
        self._navigate(self._session.next)

    def prev(self):
        self._navigate(self._session.prev)

    def first(self):
        self._navigate(self._session.first)

    def last(self):
        self._navigate(self._session.last)

    # ---------------------------------------------------------
    # Main update
    # ---------------------------------------------------------

    def update(self, dt: int):

        if self._state != PlayerState.PLAYING:
            return

        if self._phase == PlaybackPhase.PREPARE_ITEM:

            self._current_item = self.session.current_item

            print(
                "PREPARE_ITEM #"
                + str(self.session.current_index)
            )

            self._phase = PlaybackPhase.PREPARE_TEXT_AUDIO

        elif self._phase == PlaybackPhase.PREPARE_TEXT_AUDIO:

            if self._audio_task is None:

                self._audio_task = self._async_runner.submit(
                    self._prepare_text_audio()
                )

            if self._audio_task.done():

                task = self._audio_task
                self._audio_task = None

                try:
                    task.result()

                except asyncio.CancelledError:
                    return

                self._audio_mixer.play()

                print("TEXT PLAY")

                self._phase = PlaybackPhase.WAIT_TEXT_END

        elif self._phase == PlaybackPhase.WAIT_TEXT_END:

            if not self._audio_mixer.is_playing():

                print("TEXT_END")

                self._timer_ms = self.pause_before_translation
                self._phase = PlaybackPhase.PAUSE

        elif self._phase == PlaybackPhase.PAUSE:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("PAUSE_END")
                self._phase = PlaybackPhase.PREPARE_TRANSLATION_AUDIO

        elif self._phase == PlaybackPhase.PREPARE_TRANSLATION_AUDIO:

            if self._audio_task is None:

                self._audio_task = self._async_runner.submit(
                    self._prepare_translation_audio()
                )

            if self._audio_task.done():

                task = self._audio_task
                self._audio_task = None

                try:
                    task.result()

                except asyncio.CancelledError:
                    return

                self._audio_mixer.play()

                print("TRANSLATION PLAY")

                self._phase = PlaybackPhase.WAIT_TRANSLATION_END
  

        elif self._phase == PlaybackPhase.WAIT_TRANSLATION_END:

            if not self._audio_mixer.is_playing():

                print("TRANSLATION_END")

                self._timer_ms = self.pause_between_sentences
                self._phase = PlaybackPhase.PAUSE_BETWEEN_SENTENCES

        elif self._phase == PlaybackPhase.PAUSE_BETWEEN_SENTENCES:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("PAUSE_BETWEEN_SENTENCES_END")
                self._phase = PlaybackPhase.FINISH_ITEM

        elif self._phase == PlaybackPhase.FINISH_ITEM:

            print("FINISH_ITEM")

            if self.session.is_last():

                print("PLAYBACK_FINISHED")
                self._state = PlayerState.IDLE

            else:

                self.session.next()
                self._phase = PlaybackPhase.PREPARE_ITEM