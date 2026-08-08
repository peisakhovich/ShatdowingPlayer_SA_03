"""
Player lifecycle and playback FSM
Player — центральный объект управления воспроизведением.
На данном этапе отвечает только за:
- хранение Session;
- состояние проигрывателя;
- навигацию по Session;
- публичный API.
"""

class PlayerState:

    #Состояния Player
    IDLE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3

class PlaybackPhase:

    #Этап воспроизведения одной фразы.
    PREPARE_ITEM = 0
    PLAY_TEXT = 1
    WAIT_TEXT_END = 2
    PAUSE = 3
    PLAY_TRANSLATION = 4
    WAIT_TRANSLATION_END = 5
    PAUSE_BETWEEN_SENTENCES = 6
    FINISH_ITEM = 7

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

        #print("PLAYER PLAY:", self._state)

        if self._session is None:
            return

        if self._state == PlayerState.PAUSED:

            self._state = PlayerState.PLAYING
            return


        self._state = PlayerState.PLAYING
        self._phase = PlaybackPhase.PREPARE_ITEM

    def pause(self):

        #print("PLAYER PAUSE:", self._state)

        if self._state == PlayerState.PLAYING:
            self._state = PlayerState.PAUSED

    def stop(self):

        #print("PLAYER STOP:", self._state)

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

    def first(self):
        self._session.first()

    def last(self):
        self._session.last()

    # ---------------------------------------------------------
    # Main update
    # ---------------------------------------------------------

    def update(self, dt: int):

    
        # if self._state != PlayerState.PLAYING:
        #     print("UPDATE SKIP:", self._state)
        #     return


        if self._state != PlayerState.PLAYING:
            return

        if self._phase == PlaybackPhase.PREPARE_ITEM:
            
            self._current_item = self.session.current_item
            self._phase = PlaybackPhase.PLAY_TEXT
            print("PREPARE_ITEM #" + str(self.session.current_index))

        elif self._phase == PlaybackPhase.PLAY_TEXT:

            print("PLAY_TEXT: " + self._current_item.get("phrase_text"))
            # позже здесь будет запуск TTS
            self._timer_ms = 1000
            self._phase = PlaybackPhase.WAIT_TEXT_END

        elif self._phase == PlaybackPhase.WAIT_TEXT_END:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("TEXT_END")
                self._timer_ms = self.pause_before_translation
                self._phase = PlaybackPhase.PAUSE

        elif self._phase == PlaybackPhase.PAUSE:

            self._timer_ms -= dt

            if self._timer_ms <= 0:

                print("PAUSE_END")
                self._phase = PlaybackPhase.PLAY_TRANSLATION                

        elif self._phase == PlaybackPhase.PLAY_TRANSLATION:

            print("PLAY_TRANSLATION: " + self._current_item.get("translate_text"))
            # позже здесь будет запуск TTS
            self._timer_ms = 1000
            self._phase = PlaybackPhase.WAIT_TRANSLATION_END

        elif self._phase == PlaybackPhase.WAIT_TRANSLATION_END:

            self._timer_ms -= dt

            if self._timer_ms <= 0:
                
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
