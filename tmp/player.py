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

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def session(self):
        return self._session

    @property
    def state(self):
        return self._state

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