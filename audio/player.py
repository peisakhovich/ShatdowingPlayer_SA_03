
"""
Player lifecycle and playback FSM.

Player — центральный объект управления воспроизведением.

Отвечает за:
- хранение Session;
- состояние проигрывателя;
- FSM воспроизведения;
- навигацию по Session;
- подготовку и запуск аудио;
- публичный API управления воспроизведением.
"""

import asyncio

from audio.cache import AudioCache
from audio.provider import AudioProvider
from audio.mixer import AudioMixer
from audio.tts import TTS
from audio.async_runner import AsyncRunner


class PlayerState:
    """Состояния жизненного цикла Player."""

    IDLE = 0       # Не воспроизводит; готов к запуску
    PLAYING = 1    # Воспроизведение активно
    PAUSED = 2     # Воспроизведение временно приостановлено
    STOPPED = 3    # Воспроизведение принудительно остановлено


class PlaybackPhase:
    """Этапы воспроизведения одной фразы."""

    PREPARE_ITEM = 0                  # Получение текущего item
    PREPARE_TEXT_AUDIO = 1            # Получение/генерация аудио текста
    WAIT_TEXT_END = 2                 # Ожидание окончания текста
    PAUSE = 3                         # Пауза перед переводом
    PREPARE_TRANSLATION_AUDIO = 4     # Получение/генерация аудио перевода
    WAIT_TRANSLATION_END = 5          # Ожидание окончания перевода
    PAUSE_BETWEEN_SENTENCES = 6       # Пауза перед следующей фразой
    FINISH_ITEM = 7                   # Завершение текущего item


class Player:

    def __init__(self, session):

        self._session = session

        # Состояние жизненного цикла Player.
        self._state = PlayerState.IDLE

        # Текущий этап FSM.
        self._phase = PlaybackPhase.PREPARE_ITEM

        # Параметры воспроизведения.
        self._voice_speed = 1.0
        self._pause_before_translation = 0
        self._factor_pause_before_translation = 1.0 
        self._pause_between_sentences = 2000

        # Таймер используется только для пауз FSM.
        # Окончание аудио определяется через AudioMixer.is_playing().
        self._timer_ms = 0

        # Текущий элемент Session.
        self._current_item = None

        # Повторы
        self._repeat_index = 0

        # Аудио-компоненты Player.
        self._audio_provider = AudioProvider(
            cache=AudioCache(),
            tts=TTS()
        )

        self._audio_mixer = AudioMixer()

        # Выполняет async-корутину в отдельном рабочем потоке.
        self._async_runner = AsyncRunner()

        # Текущая фоновая задача подготовки аудио.
        # Может быть отменена при навигации.
        self._audio_task = None

        # Опции воспроизведения.
        self._loop = False
        self._voice_text = True
        self._show_translation = True
        self._voice_translation = True

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

    @property    
    def factor_pause_before_translation(self):
        return self._factor_pause_before_translation

    @factor_pause_before_translation.setter
    def factor_pause_before_translation(self, value):
        self._factor_pause_before_translation = value

    

    # ---------------------------------------------------------
    # Async audio preparation
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

    # ---------------------------------------------------------
    # options
    # ---------------------------------------------------------

    def set_option(self, name, checked):
        setattr(self, "_" + name, checked)

    # ---------------------------------------------------------
    # Playback control
    # ---------------------------------------------------------

    def play(self):

        if self._session is None:
            return

        # После Pause продолжаем текущее аудио
        # с того же места.
        if self._state == PlayerState.PAUSED:

            self._audio_mixer.resume()
            self._state = PlayerState.PLAYING
            return

        self._state = PlayerState.PLAYING
        self._phase = PlaybackPhase.PREPARE_ITEM

    def pause(self):

        if self._state == PlayerState.PLAYING:

            self._audio_mixer.pause()
            self._state = PlayerState.PAUSED

    def stop(self):

        self._audio_mixer.stop()
        self._state = PlayerState.STOPPED

    # ---------------------------------------------------------
    # Playback parameters
    # ---------------------------------------------------------

    def set_speed(self, value: float):
        self.voice_speed = value

    def set_pause_before_translation(self, value: int):
        self.pause_before_translation = value*self._factor_pause_before_translation

    def set_factor_pause_before_translation(self, value: float):
        self._factor_pause_before_translation = value   

    def set_pause_between_sentences(self, value: int):
        self._pause_between_sentences = value


  

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def _navigate(self, action):

        # При навигации текущее аудио и незавершённая
        # подготовка аудио должны быть остановлены.
        self._cancel_audio_task()
        self._audio_mixer.stop()

        action()

        # Следующий update() начнёт подготовку нового item.
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
    # Main update / Playback FSM
    # ---------------------------------------------------------

    def update(self, dt: int):

        if self._state != PlayerState.PLAYING:
            return

        # -----------------------------------------------------
        # Получение текущего item
        # -----------------------------------------------------

        if self._phase == PlaybackPhase.PREPARE_ITEM:

            self._current_item = self.session.current_item
            self._repeat_index = 0

            self.set_pause_before_translation(
                self._current_item.get("pause_ms", 2000) 
            )


            print(
                "PAUSE_BEFORE_TRANSLATION = "
                + str(self.pause_before_translation)
            )

            print(
                "PAUSE_BETWEEN_SENTENCES = "
                      + str(self.pause_between_sentences)
            )

            print(
                "PREPARE_ITEM #"
                + str(self.session.current_index)
            )

            self._phase = PlaybackPhase.PREPARE_TEXT_AUDIO

        # -----------------------------------------------------
        # Подготовка аудио текста
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Ожидание окончания текста
        # -----------------------------------------------------

        elif self._phase == PlaybackPhase.WAIT_TEXT_END:

            if not self._audio_mixer.is_playing():

                print("TEXT_END")

                self._timer_ms = self.pause_before_translation
                self._phase = PlaybackPhase.PAUSE

        # -----------------------------------------------------
        # Пауза перед переводом
        # -----------------------------------------------------

        elif self._phase == PlaybackPhase.PAUSE:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("PAUSE_END")

                self._phase = PlaybackPhase.PREPARE_TRANSLATION_AUDIO

        # -----------------------------------------------------
        # Подготовка аудио перевода
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Ожидание окончания перевода
        # -----------------------------------------------------

        elif self._phase == PlaybackPhase.WAIT_TRANSLATION_END:

            if not self._audio_mixer.is_playing():

                print("TRANSLATION_END")

                self._timer_ms = self.pause_between_sentences
                self._phase = PlaybackPhase.PAUSE_BETWEEN_SENTENCES

        # -----------------------------------------------------
        # Пауза перед следующей фразой
        # -----------------------------------------------------

        elif self._phase == PlaybackPhase.PAUSE_BETWEEN_SENTENCES:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("PAUSE_BETWEEN_SENTENCES_END")

                self._phase = PlaybackPhase.FINISH_ITEM

        # -----------------------------------------------------
        # Завершение текущего item
        # -----------------------------------------------------

        elif self._phase == PlaybackPhase.FINISH_ITEM:

            if self._loop:
                print("LOOP: repeat current item")
                self._phase = PlaybackPhase.PREPARE_TEXT_AUDIO
                return

            repeat_count = self._current_item.get("repeat_count", 1)

            self._repeat_index += 1

            print(
                f"FINISH_ITEM: "
                f"repeat {self._repeat_index}/{repeat_count}"
            )

            if self._repeat_index < repeat_count:

                # Повторяем тот же item.
                self._phase = PlaybackPhase.PREPARE_TEXT_AUDIO

            elif self.session.is_last():

                print("PLAYBACK_FINISHED")
                self._state = PlayerState.IDLE

            else:

                self.session.next()
                self._phase = PlaybackPhase.PREPARE_ITEM

