"""
Player — центральный объект управления воспроизведением.

На данном этапе отвечает только за:
- хранение Session;
- состояние проигрывателя;
- навигацию по Session;
- публичный API.

Воспроизведение звука будет добавлено позже.
"""


class PlayerState:
    """Состояния Player."""

    IDLE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Player:

    def __init__(self, session):

        self._session = session
        self._state = PlayerState.IDLE

        # Параметры воспроизведения
        self._voice_speed = 1.0
        self._pause_before_translation = 2000
        self._pause_between_sentences = 2000        


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
    # Playback control
    # ---------------------------------------------------------

    def play(self):
        self._state = PlayerState.PLAYING

    def pause(self):
        if self._state == PlayerState.PLAYING:
            self._state = PlayerState.PAUSED

    def stop(self):
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

    def next(self):
        self._session.next()

    def prev(self):
        self._session.prev()

    # ---------------------------------------------------------
    # Main update
    # ---------------------------------------------------------

    def update(self):
        """
        Вызывается один раз за кадр главным циклом приложения.
        Пока ничего не делает.
        """
        pass